param(
    [string]$Browser = (Join-Path ([Environment]::GetEnvironmentVariable('ProgramFiles(x86)')) 'Microsoft\Edge\Application\msedge.exe'),
    [switch]$NoSandbox
)
$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'porovnanie.html'
$pdf = Join-Path $PSScriptRoot 'porovnanie_datasetov.pdf'
$profile = Join-Path $PSScriptRoot ('_tlac_' + [guid]::NewGuid().ToString('N'))
$localSource = [uri]::new($source).AbsoluteUri
$cli = @(
    '--headless=new', '--disable-gpu', '--disable-background-networking', '--disable-extensions',
    '--no-first-run', '--no-pdf-header-footer', ('--user-data-dir="{0}"' -f $profile),
    ('--print-to-pdf="{0}"' -f $pdf), ('"{0}"' -f $localSource)
)
if ($NoSandbox) { $cli = @('--no-sandbox') + $cli }
try {
    $started = [DateTime]::UtcNow
    $process = Start-Process -FilePath $Browser -ArgumentList $cli -WindowStyle Hidden -PassThru -Wait
    $result = Get-Item -LiteralPath $pdf
    if ($process.ExitCode -ne 0 -or $result.Length -eq 0 -or $result.LastWriteTimeUtc -lt $started) {
        throw "Export PDF zlyhal."
    }
    $result
} finally {
    if (Test-Path -LiteralPath $profile) {
        $resolved = (Resolve-Path -LiteralPath $profile).Path
        $parent = (Resolve-Path -LiteralPath $PSScriptRoot).Path
        if ((Split-Path -Parent $resolved) -eq $parent -and (Split-Path -Leaf $resolved) -like '_tlac_*') {
            Remove-Item -LiteralPath $resolved -Recurse -Force
        }
    }
}
