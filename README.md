# Framework de pruebas automatizadas
Instalar dependencias por medio de pip install
- pytest==7.4.3
- pytest-bdd==7.1.2
- pytest-playwright==0.4.4
- playwright==1.40.0
- allure-pytest==2.13.2
- configparser==6.0.0
Instalas allure mediante npm o gestor de paquetes
- npm install allure

## Para ejecutar mediante linea de comando

python run_tests.py --env qa --headed --allure

este comando esta parametrizado donde elejimos ambiente, interfaz y que se muestre el reporte de allure al finalizar
tambien podemos ingresar los tags para scenearios, features, etc.
