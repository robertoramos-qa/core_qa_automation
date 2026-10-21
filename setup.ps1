# Playwright BDD — Script de instalacion para Windows
# Ejecutar en PowerShell como Administrador (solo la primera vez para instalar Allure)
#
# Uso:
#   .\setup.ps1
#
# Si PowerShell bloquea la ejecucion de scripts, ejecuta primero:
#   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ── Colores helpers ────────────────────────────────────────────────────────────
function Write-Header  { param($msg) Write-Host "`n$msg" -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "  [OK]  $msg" -ForegroundColor Green }
function Write-Info    { param($msg) Write-Host "  [..] $msg" -ForegroundColor White }
function Write-Warn    { param($msg) Write-Host "  [!!] $msg" -ForegroundColor Yellow }
function Write-Fail    { param($msg) Write-Host "  [XX] $msg" -ForegroundColor Red }

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Playwright BDD - Instalacion de Dependencias" -ForegroundColor Cyan
Write-Host "  (Windows / PowerShell)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# ── 1. Validar Python 3.8+ ─────────────────────────────────────────────────────
Write-Header "1/6 Validando Python..."

$pythonCmd = $null
foreach ($cmd in @("python", "python3")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python (\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -gt 3 -or ($major -eq 3 -and $minor -ge 8)) {
                $pythonCmd = $cmd
                Write-Success "Python encontrado: $ver"
                break
            } else {
                Write-Fail "Python $major.$minor encontrado, se requiere 3.8 o superior."
                exit 1
            }
        }
    } catch { }
}

if (-not $pythonCmd) {
    Write-Fail "Python no encontrado en el PATH."
    Write-Warn "Descargalo desde: https://www.python.org/downloads/"
    Write-Warn "Asegurate de marcar 'Add Python to PATH' durante la instalacion."
    exit 1
}

# ── 2. Crear entorno virtual ───────────────────────────────────────────────────
Write-Header "2/6 Configurando entorno virtual..."

if (-not (Test-Path "venv")) {
    Write-Info "Creando entorno virtual en .\venv ..."
    & $pythonCmd -m venv venv
    Write-Success "Entorno virtual creado"
} else {
    Write-Success "Entorno virtual ya existe"
}

# Activar entorno virtual
$activateScript = ".\venv\Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Fail "No se encontro el script de activacion: $activateScript"
    exit 1
}
Write-Info "Activando entorno virtual..."
& $activateScript
Write-Success "Entorno virtual activado"

# ── 3. Instalar dependencias Python ───────────────────────────────────────────
Write-Header "3/6 Instalando dependencias Python (PyPI)..."

Write-Info "Actualizando pip..."
& python -m pip install --upgrade pip --quiet

Write-Info "Instalando paquetes desde requirements.txt..."
& python -m pip install -r requirements.txt

Write-Success "Dependencias Python instaladas"

# ── 4. Instalar navegadores Playwright ────────────────────────────────────────
Write-Header "4/6 Instalando navegadores de Playwright..."

Write-Info "Instalando Chromium, Firefox y WebKit..."
& python -m playwright install chromium firefox webkit

Write-Success "Navegadores instalados"

# ── 5. Instalar Allure CLI ─────────────────────────────────────────────────────
Write-Header "5/6 Instalando Allure CLI..."

if (Get-Command allure -ErrorAction SilentlyContinue) {
    $allureVer = & allure --version
    Write-Success "Allure CLI ya instalado: $allureVer"
} elseif (Get-Command scoop -ErrorAction SilentlyContinue) {
    Write-Info "Instalando Allure via Scoop..."
    & scoop install allure
    Write-Success "Allure instalado via Scoop"
} elseif (Get-Command choco -ErrorAction SilentlyContinue) {
    Write-Info "Instalando Allure via Chocolatey..."
    & choco install allure --yes
    Write-Success "Allure instalado via Chocolatey"
} elseif (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Info "Instalando Allure via npm..."
    & npm install -g allure-commandline --save-dev
    Write-Success "Allure instalado via npm"
} else {
    Write-Warn "No se encontro Scoop, Chocolatey ni npm para instalar Allure CLI."
    Write-Warn "Opciones de instalacion manual:"
    Write-Warn "  Scoop      : scoop install allure"
    Write-Warn "  Chocolatey : choco install allure"
    Write-Warn "  npm        : npm install -g allure-commandline"
    Write-Warn "  Manual     : https://allurereport.org/docs/gettingstarted-installation/"
}

# ── 6. Crear directorios de trabajo ───────────────────────────────────────────
Write-Header "6/6 Creando directorios de trabajo..."

foreach ($dir in @("screenshots", "allure-results", "allure-report", "logs")) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Success "Creado: $dir\"
    } else {
        Write-Info "Ya existe: $dir\"
    }
}

# ── Resumen final ──────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "  Instalacion completada exitosamente!" -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "  Para ejecutar las pruebas:" -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "    # Activar el entorno virtual (cada sesion nueva)" -ForegroundColor White
Write-Host "    .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "" -ForegroundColor White
Write-Host "    # Runner Python (recomendado):" -ForegroundColor White
Write-Host "    python run_tests.py --env qa" -ForegroundColor Yellow
Write-Host "    python run_tests.py --env dev --headed --tags smoke" -ForegroundColor Yellow
Write-Host "    python run_tests.py --feature search --allure" -ForegroundColor Yellow
Write-Host "" -ForegroundColor White
Write-Host "    # Ver reporte Allure:" -ForegroundColor White
Write-Host "    allure serve allure-results" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Green
