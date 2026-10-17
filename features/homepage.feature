@homepage # tag para identificar las features o suite de pruebas
Feature: Homepage
  Como usuario de prometeo
  Quiero acceder a la página principal

  Background: # este paso siempre se va ejecutar en todos los scenarios, precondición
    Given que el usuario abre la página principal de prometeo
  @regression # tags para identificar los escenarios que forman parte de la regresión 
  Scenario: La página principal carga correctamente
    When el usuario introduce usuario "1234" y contraseña "1234"
    Then la página principal debe estar cargada
    And el título de la página debe contener "Prometeo"



