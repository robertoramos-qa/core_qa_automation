#!/usr/bin/env python3
"""
Playwright BDD — Test Runner CLI

Uso:
  python run_tests.py                              # Todos los tests (env: qa)
  python run_tests.py --env qa --browser chromium
  python run_tests.py --env dev --headed           # Con interfaz gráfica
  python run_tests.py --tags smoke                 # Solo smoke tests
  python run_tests.py --feature homepage           # Solo homepage
  python run_tests.py --tags smoke --allure        # Abrir reporte Allure al final
"""

import argparse
import os
import subprocess
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Playwright BDD — Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--env", "-e",
        default="qa",
        choices=["dev", "qa", "prod"],
        help="Ambiente de ejecución (default: qa)",
    )
    parser.add_argument(
        "--browser", "-b",
        default=None,
        choices=["chromium", "firefox", "webkit"],
        help="Navegador (default: el definido en el properties file)",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Ejecutar con interfaz gráfica (headed mode)",
    )
    parser.add_argument(
        "--tags", "-t",
        default=None,
        help='Tags de pytest a ejecutar. Ej: "smoke", "regression", "smoke and not regression"',
    )
    parser.add_argument(
        "--feature", "-f",
        default=None,
        choices=["homepage", "search"],
        help="Ejecutar solo el feature especificado",
    )
    parser.add_argument(
        "--allure",
        action="store_true",
        help="Generar y abrir el reporte de Allure al finalizar",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Salida detallada de pytest",
    )
    return parser.parse_args()


def configure_env(args: argparse.Namespace) -> None:
    os.environ["TEST_ENV"] = args.env
    if args.browser:
        os.environ["TEST_BROWSER"] = args.browser
    os.environ["TEST_HEADLESS"] = "false" if args.headed else "true"


def build_command(args: argparse.Namespace) -> list:
    cmd = ["python", "-m", "pytest"]

    if args.feature:
        cmd.append(f"steps/test_{args.feature}.py")
    else:
        cmd.append("steps/")

    if args.tags:
        cmd.extend(["-m", args.tags])

    cmd.extend(["--alluredir=allure-results", "--clean-alluredir", "--tb=short"])

    if args.verbose:
        cmd.append("-v")

    return cmd


def open_allure_report() -> None:
    print("\nGenerando reporte de Allure...")
    result = subprocess.run(
        ["allure", "generate", "allure-results", "--clean", "-o", "allure-report"],
        capture_output=True,
    )
    if result.returncode != 0:
        print("  allure generate falló — intentando con 'allure serve'...")
        subprocess.run(["allure", "serve", "allure-results"])
        return
    print("Abriendo reporte...")
    subprocess.run(["allure", "open", "allure-report"])


def main() -> None:
    args = parse_args()

    print("=" * 58)
    print(" Playwright BDD — Framework de Pruebas")
    print("=" * 58)
    print(f"  Ambiente  : {args.env.upper()}")
    print(f"  Navegador : {args.browser or 'desde properties file'}")
    print(f"  Modo      : {'Headed (visible)' if args.headed else 'Headless'}")
    print(f"  Tags      : {args.tags or 'todos'}")
    print(f"  Feature   : {args.feature or 'todos'}")
    print("=" * 58)

    configure_env(args)
    cmd = build_command(args)

    print(f"\nEjecutando: {' '.join(cmd)}\n")

    result = subprocess.run(cmd)

    print("\n" + "=" * 58)
    status = "PASSED" if result.returncode == 0 else "FAILED"
    print(f"  Resultado final: {status}")
    print("=" * 58)

    if args.allure:
        open_allure_report()
    else:
        print("\nPara ver el reporte Allure ejecuta:")
        print("  allure serve allure-results")

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
