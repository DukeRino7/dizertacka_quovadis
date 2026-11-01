"""Rozloženie 2381 EMBER príznakov (verzia príznakov 2, Anderson & Roth 2018, `ember/features.py`).

Skupiny a ich šírky sú overené na dátach: súčet šírok = 2381, histogramy bajtov a entropie
majú v každom riadku súčet 1 (normalizované). Názvy v rámci skupín zodpovedajú poradiu
v pôvodnej implementácii EMBER; hašované bloky (FeatureHasher) nemajú význam jednotlivých
stĺpcov, preto sú pomenované iba číslom koša.
"""
from dataclasses import dataclass

import pandas as pd

EMBER_DIM = 2381


@dataclass(frozen=True)
class Group:
    name: str
    width: int
    description: str
    kind: str  # "distribution" | "count" | "hashed" | "mixed"


GROUPS = [
    Group("histogram", 256, "normalizovaný histogram hodnôt bajtov", "distribution"),
    Group("byteentropy", 256, "normalizovaný 2D histogram bajt × lokálna entropia", "distribution"),
    Group("strings", 104, "štatistiky tlačiteľných reťazcov", "mixed"),
    Group("general", 10, "všeobecné vlastnosti súboru", "mixed"),
    Group("header", 62, "COFF a optional hlavička", "mixed"),
    Group("section", 255, "sekcie PE (súhrn + hašované vlastnosti)", "mixed"),
    Group("imports", 1280, "importované knižnice a funkcie (hašované)", "hashed"),
    Group("exports", 128, "exportované funkcie (hašované)", "hashed"),
    Group("datadirectories", 30, "veľkosti a adresy dátových adresárov", "count"),
]

_HEADER_NUMERIC = [
    "major_image_version", "minor_image_version", "major_linker_version", "minor_linker_version",
    "major_operating_system_version", "minor_operating_system_version", "major_subsystem_version",
    "minor_subsystem_version", "sizeof_code", "sizeof_headers", "sizeof_heap_commit",
]
_DATA_DIRECTORIES = [
    "EXPORT_TABLE", "IMPORT_TABLE", "RESOURCE_TABLE", "EXCEPTION_TABLE", "CERTIFICATE_TABLE",
    "BASE_RELOCATION_TABLE", "DEBUG", "ARCHITECTURE", "GLOBAL_PTR", "TLS_TABLE", "LOAD_CONFIG_TABLE",
    "BOUND_IMPORT", "IAT", "DELAY_IMPORT_DESCRIPTOR", "CLR_RUNTIME_HEADER",
]


def _names(group: str) -> list[str]:
    if group == "histogram":
        return [f"histogram_{i:03d}" for i in range(256)]
    if group == "byteentropy":
        return [f"byteentropy_{i:03d}" for i in range(256)]
    if group == "strings":
        return (["strings_numstrings", "strings_avlength"]
                + [f"strings_printabledist_{i:02d}" for i in range(96)]
                + ["strings_printables", "strings_entropy", "strings_paths", "strings_urls",
                   "strings_registry", "strings_MZ"])
    if group == "general":
        return [f"general_{n}" for n in ["size", "vsize", "has_debug", "exports", "imports",
                                         "has_relocations", "has_resources", "has_signature",
                                         "has_tls", "symbols"]]
    if group == "header":
        return (["header_coff_timestamp"]
                + [f"header_coff_machine_hash_{i}" for i in range(10)]
                + [f"header_coff_characteristics_hash_{i}" for i in range(10)]
                + [f"header_opt_subsystem_hash_{i}" for i in range(10)]
                + [f"header_opt_dll_characteristics_hash_{i}" for i in range(10)]
                + [f"header_opt_magic_hash_{i}" for i in range(10)]
                + [f"header_opt_{n}" for n in _HEADER_NUMERIC])
    if group == "section":
        return (["section_num", "section_num_zero_size", "section_num_empty_name",
                 "section_num_rx", "section_num_w"]
                + [f"section_size_hash_{i:02d}" for i in range(50)]
                + [f"section_entropy_hash_{i:02d}" for i in range(50)]
                + [f"section_vsize_hash_{i:02d}" for i in range(50)]
                + [f"section_entry_name_hash_{i:02d}" for i in range(50)]
                + [f"section_entry_characteristics_hash_{i:02d}" for i in range(50)])
    if group == "imports":
        return ([f"imports_library_hash_{i:03d}" for i in range(256)]
                + [f"imports_function_hash_{i:04d}" for i in range(1024)])
    if group == "exports":
        return [f"exports_hash_{i:03d}" for i in range(128)]
    if group == "datadirectories":
        return [f"datadir_{d}_{p}" for d in _DATA_DIRECTORIES for p in ("size", "virtual_address")]
    raise KeyError(group)


def feature_table() -> pd.DataFrame:
    """Tabuľka príznakov: index stĺpca, názov, skupina."""
    rows = []
    for g in GROUPS:
        names = _names(g.name)
        assert len(names) == g.width, (g.name, len(names), g.width)
        rows += [(g.name, n) for n in names]
    assert len(rows) == EMBER_DIM
    df = pd.DataFrame(rows, columns=["group", "name"])
    df.insert(0, "column", range(EMBER_DIM))
    return df


def group_slices() -> dict[str, slice]:
    out, start = {}, 0
    for g in GROUPS:
        out[g.name] = slice(start, start + g.width)
        start += g.width
    return out
