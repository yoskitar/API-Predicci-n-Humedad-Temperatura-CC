#Imagen y versión que usaremos de base para la 
#construcción del contenedor.
FROM python:3.7
#Indicamos a modo informativo, el responsable encargado de 
#mantener el repositorio, con la etiqueta LABEL, ya que 
#MAINTAINER se encuentra [deprecated]
LABEL maintainer="osc9718@gmail.com"
#Establecemos el directorio de trabajo.
WORKDIR /usr/
#Copiamos el requirements.txt donde 
#hemos especificado las dependencias de nuestro microservicio.
COPY requirements.txt ./
#Instalamos las dependencias indicadas
RUN pip install -r requirements.txt
RUN pip install coverage
#Copiamos el contenido del código de la aplicación 
#al directorio de trabajo definido dentro del contenedor.
#El segundo argumento hace referencia a la dirección donde se copiará
#el contenido. Si se usa el punto, estamos indicando que se escoja
#la ruta definida en el WORKDIR.
COPY v1/src/ src/
#Indicamos a modo informativo el puerto interno
#de nuestro microservicio. 
EXPOSE 3000
#Definimos la acción a ejecutar. Esta acción se ejecutará
#automáticamente al ejecutar el contenedor.
CMD coverage run -m unittest src/test/app_test.py