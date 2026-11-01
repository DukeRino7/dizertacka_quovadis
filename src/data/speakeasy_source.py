"""Čítanie Speakeasy reportov z data/quovadis-speakeasy (iba čítanie, nič sa nemení).

Overený formát (docs/01_audit_dat.md, kontrola na testovacej časti):
- train `<sha256>.json`, test `<sha256>.dat.json`; train report_backdoor a report_clean majú podpriečinky,
- report = JSON ZOZNAM vstupných bodov (README datasetu uvádza iný tvar, ktorý v dátach nie je),
- vstupný bod: ep_type (module_entry | thread | tls_callback_N), start_addr, ep_args, apihash,
  apis [{pc, api_name, args[str], ret_val}], ret_val, error {} alebo {type, pc, ...}, dynamic_code_segments,
  voliteľne registry_access, file_access, network_events, process_events, dropped_files, handled_exceptions,
- report_windows_syswow64 je pomenovaný podľa programu (nie SHA-256) -> nedá sa spárovať, preskakuje sa.

Jedna vzorka = jeden súbor; všetky jej vstupné body a vlákna patria spolu (v poradí, v akom sú v reporte).
"""
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from src.common.paths import SPEAKEASY_DIR
from .speakeasy_listing import family_from_folder

try:
    import orjson
    _loads = orjson.loads
except ImportError:  # pragma: no cover
    _loads = json.loads

_SHA = re.compile(r"^[0-9a-f]{64}$")
EVENT_KEYS = ["registry_access", "file_access", "network_events", "process_events", "dropped_files", "handled_exceptions"]


def find_reports(root: Path = SPEAKEASY_DIR) -> pd.DataFrame:
    """Nájde reporty na disku: sha256, original_split, family, path (relatívne k root), bytes."""
    rows = []
    for split_dir, split in [("windows_emulation_trainset", "train"), ("windows_emulation_testset", "test")]:
        base = root / split_dir
        if not base.exists():
            continue
        for p in base.rglob("*.json"):
            sha = p.name.split(".")[0]
            if not _SHA.match(sha):
                continue
            folder = p.relative_to(base).parts[0]
            rows.append((sha, split, family_from_folder(folder), p.relative_to(root).as_posix(), p.stat().st_size))
    return pd.DataFrame(rows, columns=["sha256", "original_split", "family", "path", "bytes"])


@dataclass
class EntryPoint:
    ep_type: str
    api_names: list[str]
    api_args: list[list[str]]
    api_ret: list[str | None]
    error_type: str | None          # None = bez chyby
    events: list[str]               # napr. "file_access:create", "registry_access:open_key"
    n_dynamic_code_segments: int


@dataclass
class Report:
    sha256: str
    status: str                     # ok | empty_file | invalid_json | not_list | no_entry_points
    entry_points: list[EntryPoint] = field(default_factory=list)
    detail: str = ""

    @property
    def api_names(self) -> list[str]:
        """Postupnosť API volaní celej vzorky: vstupné body za sebou v poradí reportu."""
        return [a for ep in self.entry_points for a in ep.api_names]


def _event_tokens(ep: dict) -> list[str]:
    out = []
    for k in EVENT_KEYS:
        for e in ep.get(k) or []:
            kind = e.get("event") if isinstance(e, dict) else None
            out.append(f"{k}:{kind}" if kind else k)
    return out


def parse_report(path: Path, sha256: str = "") -> Report:
    """Robustné načítanie jedného reportu; poškodené súbory nevyhodia výnimku, ale vrátia status."""
    raw = path.read_bytes()
    if not raw.strip():
        return Report(sha256, "empty_file")
    try:
        d = _loads(raw)
    except Exception as e:
        return Report(sha256, "invalid_json", detail=str(e)[:200])
    if not isinstance(d, list):
        return Report(sha256, "not_list", detail=type(d).__name__)
    if not d:
        return Report(sha256, "no_entry_points")
    eps = []
    for ep in d:
        if not isinstance(ep, dict):
            continue
        apis = ep.get("apis") or []
        err = ep.get("error") or {}
        eps.append(EntryPoint(
            ep_type=str(ep.get("ep_type")),
            api_names=[str(a.get("api_name")) for a in apis],
            api_args=[[str(x) for x in (a.get("args") or [])] for a in apis],
            api_ret=[None if a.get("ret_val") is None else str(a.get("ret_val")) for a in apis],
            error_type=str(err.get("type")) if err else None,
            events=_event_tokens(ep),
            n_dynamic_code_segments=len(ep.get("dynamic_code_segments") or []),
        ))
    if not eps:
        return Report(sha256, "no_entry_points")
    return Report(sha256, "ok", eps)


def summarize(r: Report) -> dict:
    """Súhrn jedného reportu (na audit a štatistiky)."""
    eps = r.entry_points
    names = r.api_names
    return {
        "sha256": r.sha256, "status": r.status, "detail": r.detail,
        "n_entry_points": len(eps),
        "n_threads": sum(ep.ep_type == "thread" for ep in eps),
        "n_api_calls": len(names),
        "n_api_unique": len(set(n.lower() for n in names)),
        "n_api_module_entry": sum(len(ep.api_names) for ep in eps if ep.ep_type == "module_entry"),
        "max_api_per_ep": max((len(ep.api_names) for ep in eps), default=0),
        "n_ep_errors": sum(ep.error_type is not None for ep in eps),
        "module_entry_error": next((ep.error_type for ep in eps if ep.ep_type == "module_entry"), None),
        "n_events": sum(len(ep.events) for ep in eps),
        "n_dynamic_code_segments": sum(ep.n_dynamic_code_segments for ep in eps),
        "first_api": names[0].lower() if names else None,
    }
