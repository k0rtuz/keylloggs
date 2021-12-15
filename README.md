# Keylloggs

Este proyecto consiste en un programa que muestra una serie de opciones,
siendo la primera de ellas la ejecución de un keylogger que captura eventos
de pulsaciones de teclas a nivel global del sistema operativo.

Otras opciones permiten ver los *logs* generados y credenciales obtenidas,
las cuales se basan en la búsqueda de direcciones de correo electrónico con
el dominio **eiposgrados.edu.es**.

### Requisitos

Se ha comprobado su funcionamiento en distribuciones Linux (concretamente Debian 11),
por lo que los requisitos necesarios para sistemas con gestores de paquetes de tipo DEB
son los siguientes:

- python3-virtualenv
- python3-pip

La versión de Python con la que se han hecho las pruebas es la 3.9, por lo que cualquiera
igual o superior a ésta no debería dar problemas.

### Uso

El archivo *keylloggs* tiene por defecto permisos de ejecución, escritura y lectura únicamente para
el usuario con el que se descargue este repositorio (700 en octal).

Se trata de un script en Bash que en el mismo directorio donde está, comprueba que exista un entorno
virtual de Python llamado *venv*, creándolo si no es así y descargando las dependencias especificadas
en el archivo de texto *requirements.txt*.

A continuación, ejecuta el script de Python *main.py*, que también tiene permisos de ejecución y llama
al intérprete del entorno virtual mediante la primera línea (*shebang* **#!/usr/bin/env python**);
ejecutándose toda la lógica programada.