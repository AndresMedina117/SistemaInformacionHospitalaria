# SistemaInformacionHospitalaria

Este proyecto consiste en un programa en Python que permite la lectura de archivos en diferentes formatos (CSV, JSON, TXT) proporcionados por equipos médicos. Estos archivos contienen información de pacientes y el programa proporciona una interfaz gráfica que permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre estos datos. Los archivos son ingresados a una base de datos no relacional MongoDB Atlas.

# A TENER EN CUENTA ANTES DE EJECUTAR:

- Asegúrate de tener instalada las librerías unidecode, pyqt5 mediante el comando pip install. Esta librería es fundamental para el funcionamiento correcto del programa.

- Al seleccionar los archivos mediante el botón de agregar, asegúrate de seleccionar la carpeta que los contiene, y no solo el archivo individual.

- El archivo principal a ejecutar es main.py. Los demás archivos contienen las funciones necesarias para realizar el CRUD y se recomienda no modificarlos ni moverlos.

# Funcionalidades:

1. Crear: Permite ingresar archivos en formatos CSV, JSON o TXT a la base de datos MongoDB Atlas.

2. Leer: Recupera la información de los pacientes almacenada en la base de datos. Al realizar esta función, se genera un archivo TXT en una carpeta llamada data que contiene la información del paciente en formato HL7, si el paciente fue encontrado.

3. Actualizar/Añadir campos: Permite actualizar o añadir campos a la información de cada paciente en la base de datos.

4. Eliminar: Permite eliminar pacientes de la base de datos MongoDB Atlas.

# Uso:
Para ejecutar el programa, simplemente corre el archivo main.py. A partir de ahí, podrás utilizar la interfaz gráfica para realizar las operaciones mencionadas anteriormente.
