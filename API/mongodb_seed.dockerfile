#Imagen y versión que usaremos de base para la 
#construcción del contenedor.
FROM mongo:latest
#Indicamos a modo informativo, el responsable encargado de 
#mantener el repositorio, con la etiqueta LABEL, ya que 
#MAINTAINER se encuentra [deprecated]
LABEL maintainer="osc9718@gmail.com"
#Establecemos el directorio de trabajo.
WORKDIR /usr/
COPY data.csv datos/
#Definimos la acción a ejecutar, que en nuestro caso,
#será el comando start definido en los scripts del 
#package.json de nuestro microservicio, encargado de 
#iniciar el microservicio. Esta acción se ejecutará
#automáticamente al ejecutar el contenedor.
CMD mongoimport --host mongodb_container --db PredictionsDB --collection predictions --headerline --file /usr/datos/data.csv --type csv