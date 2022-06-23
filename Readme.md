
# Challenge de Data Analytics con Python

## Instrucciones para deployar el proyecto

- Es requisito tener instalado Python para correr el proyecto. El proyecto fue realizado con la versión 3.8.10 de Python.

1. Clonar el repositorio utilizando `git clone https://github.com/brunococitto/aklemy-da-python.git` o descargarlo como ZIP y extraerlo en una carpeta.
2. Utilizando una terminal, dentro de la carpeta del repositorio, crear un entorno virtual de Python con el comando
`python -m venv venv`
3. Activar el entorno virtual de Python con el comando
`source venv/bin/activate`
4. Instalar las dependencias del proyecto con el comando
`pip install -r requirements.txt`
5. Establecer la configuración en el archivo .env según corresponda con un editor de texto.
6. Inicializar la base de datos con el comando
`python scripts/db-init.py`
7. Ejecutar el proyecto utilizando el comando
`python scripts/main.py`

Nota: en el archivo .env se puede configurar la variable LOCALE, que sirve para establecer el idioma en el cual generar las carpetas donde se guardan las fuentes de datos, esta variable se debe establecer una única vez antes de ejecutar el programa y para cambiarla requiere eliminar las carpetas de datos ya descargados.
El lenguaje en el cual se desee utilizar el proyecto debe estar instalado en el sistema, lo que en Linux se puede realizar con los siguientes comandos:
`sudo locale-gen es_ES.UTF-8` donde "es_ES.UTF-8" es el lenguaje.
`sudo dpkg-reconfigure locales`