# wx-agent auto Python provisioning (no user install needed):
#  1) system Python >= 3.10 (py launcher or python)  -> use it
#  2) else portable Python: unpack offline\python\python-3.10.11-embed-amd64.zip (or download from mirror)
#  3) bootstrap pip for the portable build (offline wheels pip, else get-pip.py)
# Writes the resolved command to logs\python_path.txt (ASCII). Exit 0 = ok.
$ErrorActionPreference = 'Continue'

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$logDir = Join-Path $root 'logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir 'onestart.log'
$pathTxt = Join-Path $logDir 'python_path.txt'

function Log($m) {
    try { Add-Content -Path $log -Value ("[{0}] {1}" -f (Get-Date -Format 'HH:mm:ss'), $m) -Encoding UTF8 } catch {}
}

function Set-PyPath($cmd) {
    try { Set-Content -Path $pathTxt -Value $cmd -Encoding ascii } catch {}
}

# --- 1) system python ---
if (-not $env:WX_FORCE_PORTABLE) {
    foreach ($c in @('py -3', 'py', 'python')) {
        $ok = $false
        try {
            & cmd /c "$c -c `"import sys; raise SystemExit(0 if sys.version_info>=(3,10) else 1)`" 2>nul" | Out-Null
            if ($LASTEXITCODE -eq 0) { $ok = $true }
        } catch {}
        if ($ok) {
            Log "using system python: $c"
            Set-PyPath $c
            exit 0
        }
    }
    Log "no system python >=3.10 found; trying portable green python (no install required)..."
} else {
    Log "WX_FORCE_PORTABLE=1: skip system python check (test mode)"
}

# --- 2) portable python ---
$runtime = Join-Path $root 'runtime\python'
$zipDir  = Join-Path $root 'offline\python'
$zip     = Join-Path $zipDir 'python-3.10.11-embed-amd64.zip'
$pyExe   = Join-Path $runtime 'python.exe'
$urls = @(
    'https://mirrors.huaweicloud.com/python/3.10.11/python-3.10.11-embed-amd64.zip',
    'https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip'
)

function Ensure-Runtime {
    if (Test-Path $pyExe) { return $true }
    New-Item -ItemType Directory -Force -Path $runtime | Out-Null
    if (-not (Test-Path $zip)) {
        Log "downloading portable python (~8MB)..."
        $down = $false
        foreach ($u in $urls) {
            try {
                Invoke-WebRequest -Uri $u -OutFile $zip -UseBasicParsing -TimeoutSec 120
                Log "download ok: $u"
                $down = $true
                break
            } catch {
                Log "download failed: $u ($($_.Exception.Message))"
            }
        }
        if (-not $down) { return $false }
    }
    Log "unpacking portable python to runtime\python ..."
    Expand-Archive -Path $zip -DestinationPath $runtime -Force
    if (-not (Test-Path $pyExe)) { return $false }
    $pth = Get-ChildItem $runtime -Filter 'python*._pth' | Select-Object -First 1
    if ($pth) {
        $c = Get-Content $pth.FullName -Raw
        $c = $c -replace '#\s*import site', 'import site'
        Set-Content -Path $pth.FullName -Value $c -Encoding ascii
        Log "enabled site (pip support): $($pth.Name)"
    }
    return $true
}

if (-not (Ensure-Runtime)) {
    Log "[FAIL] no python and auto-download failed (need network or offline\python in package)."
    exit 1
}

# --- 3) pip bootstrap ---
$pipOk = $false
try {
    $pv = & $pyExe -m pip --version 2>&1
    if ($LASTEXITCODE -eq 0 -and ("$pv" -match 'pip \d')) { $pipOk = $true }
} catch {}
if (-not $pipOk) {
    Log "portable python lacks pip; bootstrapping..."
    # offline-first: unpack pip wheel (and setuptools) straight into site-packages
    $sitePkgs = Join-Path $runtime 'Lib\site-packages'
    $pipWheel = Get-ChildItem (Join-Path $root 'offline\wheels') -Filter 'pip-*-py3-none-any.whl' -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($pipWheel) {
        Log "pip unpack from offline wheel: $($pipWheel.Name)"
        try {
            New-Item -ItemType Directory -Force -Path $sitePkgs | Out-Null
            Expand-Archive -Path $pipWheel.FullName -DestinationPath $sitePkgs -Force
            $setWheel = Get-ChildItem (Join-Path $root 'offline\wheels') -Filter 'setuptools-*-py3-none-any.whl' -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($setWheel) { Expand-Archive -Path $setWheel.FullName -DestinationPath $sitePkgs -Force }
            $pv = & $pyExe -m pip --version 2>&1
            if ($LASTEXITCODE -eq 0 -and ("$pv" -match 'pip \d')) { $pipOk = $true }
        } catch {}
    }
    if (-not $pipOk) {
        Log "trying online get-pip.py..."
        $gp = Join-Path $logDir 'get-pip.py'
        try {
            Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile $gp -UseBasicParsing -TimeoutSec 90
            & $pyExe $gp --no-warn-script-location 2>$null | Out-Null
            $pv = & $pyExe -m pip --version 2>&1
            if ($LASTEXITCODE -eq 0 -and ("$pv" -match 'pip \d')) { $pipOk = $true }
        } catch {
            Log "get-pip failed: $($_.Exception.Message)"
        }
    }
    if (-not $pipOk) {
        Log "[FAIL] pip bootstrap failed (offline pip wheel missing and no network)."
        exit 1
    }
    Log "pip ready"
}

Log "python ready: $pyExe"
Set-PyPath $pyExe
exit 0
