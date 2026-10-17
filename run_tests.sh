#!/usr/bin/env bash
# Playwright BDD — Test Runner (Bash)
# Requiere: source venv/bin/activate antes de ejecutar

set -euo pipefail

ENV="qa"
BROWSER=""
HEADLESS="true"
TAGS=""
FEATURE=""
ALLURE=false
VERBOSE=false

usage() {
    cat <<EOF
Uso: $0 [opciones]

Opciones:
  -e, --env ENV          Ambiente: dev | qa | prod  (default: qa)
  -b, --browser BROWSER  Navegador: chromium | firefox | webkit
      --headed           Ejecutar con interfaz gráfica
  -t, --tags TAGS        Marks de pytest (ej: smoke, "smoke and not regression")
  -f, --feature FEATURE  Solo un feature: 
      --allure           Generar y abrir reporte Allure al finalizar
  -v, --verbose          Salida detallada
  -h, --help             Mostrar esta ayuda

Ejemplos:
  $0
  $0 --env dev --headed
  $0 --env qa --browser firefox --tags smoke
  $0 --feature search --allure
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -e|--env)      ENV="$2";     shift 2 ;;
        -b|--browser)  BROWSER="$2"; shift 2 ;;
        --headed)      HEADLESS="false"; shift ;;
        -t|--tags)     TAGS="$2";    shift 2 ;;
        -f|--feature)  FEATURE="$2"; shift 2 ;;
        --allure)      ALLURE=true;  shift ;;
        -v|--verbose)  VERBOSE=true; shift ;;
        -h|--help)     usage; exit 0 ;;
        *) echo "Opción desconocida: $1"; usage; exit 1 ;;
    esac
done

export TEST_ENV="$ENV"
export TEST_HEADLESS="$HEADLESS"
[[ -n "$BROWSER" ]] && export TEST_BROWSER="$BROWSER"

echo "=========================================================="
echo "  Playwright BDD — Framework de Pruebas"
echo "=========================================================="
printf "  Ambiente  : %s\n"  "${ENV^^}"
printf "  Navegador : %s\n"  "${BROWSER:-desde properties file}"
printf "  Headless  : %s\n"  "$HEADLESS"
printf "  Tags      : %s\n"  "${TAGS:-todos}"
printf "  Feature   : %s\n"  "${FEATURE:-todos}"
echo "=========================================================="

# Build pytest command
if [[ -n "$FEATURE" ]]; then
    TARGET="steps/test_${FEATURE}.py"
else
    TARGET="steps/"
fi

CMD="python -m pytest $TARGET --alluredir=allure-results --clean-alluredir --tb=short"
[[ -n "$TAGS" ]]   && CMD="$CMD -m '$TAGS'"
[[ "$VERBOSE" == true ]] && CMD="$CMD -v"

echo ""
echo "Ejecutando: $CMD"
echo ""

eval "$CMD"
EXIT_CODE=$?

echo ""
echo "=========================================================="
[[ $EXIT_CODE -eq 0 ]] && echo "  Resultado: PASSED" || echo "  Resultado: FAILED"
echo "=========================================================="

if [[ "$ALLURE" == true ]]; then
    echo ""
    echo "Generando reporte de Allure..."
    allure generate allure-results --clean -o allure-report
    allure open allure-report
else
    echo ""
    echo "Para ver el reporte Allure ejecuta:"
    echo "  allure serve allure-results"
fi

exit $EXIT_CODE
