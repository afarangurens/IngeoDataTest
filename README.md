#  Ingeodata Test Aranguren
## Andrés Fernando Aranguren Silva
- --
## Diseño e Implementación de una librería para un sistema de análisis de datos.

### Descripción del Problema:

Se debe desarrollar una librería en Python que contenga al menos la implementación de 3 cálculos básicos de la estadística, por ejemplo, la media y al menos 1 gráfica que muestre los datos.

Esta librería debe ser luego usada en un proyecto Django que permita:
- Subir un archivo tipo .csv o xls
- Usar los cálculos de la librería implementada
- Mostrar el dataset y los resultados de los calculos y la grafica en una vista web.

### Solución: 
A continuación se encuentran los endpoints a los archivos más importantes para la solución.
<h3>Archivos Importantes</h3>

- <a href="https://github.com/afarangurens/ingeodata-test-aranguren/blob/main/ingeodataproy/modules/ingeodatanalysis.py">Librería Customizada con Cálculos de Análisis Estadísticos</a></h5>

- <a href="https://github.com/afarangurens/ingeodata-test-aranguren/blob/main/ingeodataproy/datanalysis/middleware.py">Middleware para el Caching del CSV</a></h5>

- <a href="https://github.com/afarangurens/ingeodata-test-aranguren/blob/main/ingeodataproy/datanalysis/views.py">Vistas</a></h5>

- <a href="https://github.com/afarangurens/ingeodata-test-aranguren/blob/main/ingeodataproy/datanalysis/urls.py">Endpoints</a></h5>

- <a href="https://github.com/afarangurens/ingeodata-test-aranguren/blob/main/ingeodataproy/datanalysis/models.py">Modelos</a></h5>



# Instrucciones de despliegue.

1. Primero se debe clonar el repositorio utilizando el comando:

        git clone https://github.com/afarangurens/ingeodata-test-aranguren.git
        cd ingeodata-test-aranguren

2. Debido a que Django varía en sus versiones tanto de Python como de Framework lo más recomendable en la práctica es realizar un entorno de ecosistema para poder instalar los requerimientos necesarios y que no comprometan las variables de entorno del sistema operativo, para esto se crea un entorno utilizando:

        python -m venv .venv
    Y se activa con el comando (windows):
         
        .venv\Scripts\Activate
    
3. Se deben instalar los requerimientos del archivo requirements.txt para poder correr el programa utilizando el comando:

        pip install requirements.txt

4. Acceder a la carpeta que contenga el archivo 'manage.py' el cual es el archivo utilizado para correr todas las funcionalidades.
        
        cd ingeodataproy

5. Se debe correr los siguientes comandos para crear la tabla de la clase CsvFile

        python manage.py makemigrations
        python manage.py migrate


7. Por último para correr la aplicación se debe utilizar el comando:

        python manage.py runserver

# Flujo de la Aplicación.

1. El home de la aplicación se encuentra alojado en el localhost.

        http://127.0.0.1:8000/

2. Se entrará a un menú el cuál tiene las distintas funcionalidades de la aplicación.
   Lo primero a hacer será descargar el dataset de la opción que dice "Link al Enlace"
   
3. Luego se le da click a la opción upload file para así poder cargar el archivo al cache usando el middleware.

4. Una vez subido el archivo, puede ir a home y ver los diferentes análisis estadísticos realizados.


# Tests

<h3>Colección de Postman para los Tests</h3>

- <a href="">Colección Postman</a></h5>

# Documentación

La documentación puede ser consultada en el siguiente enlace:

      http://127.0.0.1:8000/admin/doc

# Referencias


- <a href="https://www.kaggle.com/datasets/mruanova/us-gasoline-and-diesel-retail-prices-19952021">Dataset de Gasolina y Diesel por el Gobierno de los Estados Unidos. </a>