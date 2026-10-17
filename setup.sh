#!/usr/bin/env bash
# Instalador de dependencias — Script de instalación de dependencias
# Ejecutar UNA sola vez antes del primer run.

set -euo pipefail

echo "=========================================================="
echo "  Automation framework IES — Instalación de Dependencias"
echo "=========================================================="

# ── Validar Python 3.8+ ────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 no está instalado."
    echo "       Descárgalo desde https://www.python.org/downloads/"
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PY_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')

echo "Python encontrado: $PY_VERSION"

if [[ $PY_MAJOR -lt 3 ]] || [[ $PY_MAJOR -eq 3 && $PY_MINOR -lt 8 ]]; then
    echo "ERROR: Se requiere Python 3.8 o superior."
    exit 1
fi

# ── Entorno virtual ────────────────────────────────────────────────────────────
if [[ ! -d "venv" ]]; then
    echo ""
    echo "Creando entorno virtual en ./venv ..."
    python3 -m venv venv
fi

echo "Activando entorno virtual..."
# shellcheck source=/dev/null
source venv/bin/activate

# ── Dependencias Python (PyPI) ─────────────────────────────────────────────────
echo ""
echo "Actualizando pip..."
pip install --upgrade pip --quiet

echo "Instalando dependencias Python (requirements.txt)..."
pip install -r requirements.txt

# ── Navegadores de Playwright ──────────────────────────────────────────────────
echo ""
echo "Instalando navegadores de Playwright (chromium, firefox, webkit)..."
playwright install chromium firefox webkit

echo "Instalando dependencias del sistema para Playwright..."
playwright install-deps || echo "  (install-deps puede requerir sudo en Linux)"

# ── Allure CLI ─────────────────────────────────────────────────────────────────
echo ""
if command -v allure &>/dev/null; then
    echo "Allure CLI ya instalado: $(allure --version)"
elif command -v brew &>/dev/null; then
    echo "Instalando Allure CLI via Homebrew..."
    brew install allure
elif command -v npm &>/dev/null; then
    echo "Instalando Allure CLI via npm..."
    npm install -g allure-commandline --save-dev
else
    echo "AVISO: Allure CLI no instalado automáticamente."
    echo "       Opciones de instalación:"
    echo "         macOS : brew install allure"
    echo "         npm   : npm install -g allure-commandline"
    echo "         Manual: https://allurereport.org/docs/gettingstarted-installation/"
fi

# ── Directorios de trabajo ─────────────────────────────────────────────────────
mkdir -p screenshots allure-results allure-report logs

# ── Permisos del runner bash ───────────────────────────────────────────────────
chmod +x run_tests.sh

echo ""
echo "=========================================================="
echo "  Instalación completada exitosamente!"
echo ""
echo "  Para ejecutar las pruebas:"
echo ""
echo "    source venv/bin/activate"
echo ""
echo "    # Con el runner Python:"
echo "    python run_tests.py --env qa"
echo "    python run_tests.py --env dev --headed --tags smoke"
echo "    python run_tests.py --allure"
echo ""
echo "    # Con el runner bash:"
echo "    bash run_tests.sh --env qa"
echo "    bash run_tests.sh --env dev --headed --tags smoke --allure"
echo "=========================================================="
