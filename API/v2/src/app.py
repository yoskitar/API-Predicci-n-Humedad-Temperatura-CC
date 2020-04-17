# -*- coding: utf-8 -*-
import falcon
import os
from prediction import Prediction
from dotenv import load_dotenv
import logging

#Creamos una instancia de la API proporcionada por el framework
#falcon, ejecutable con WSGI.
api = falcon.API()
#Leemos las variables de entorno necesarias para establecer la 
#conexión con la base de datos.
load_dotenv()
#Creamos una instancia del manejador de la base de datos, para
#la BD y colección indicadas como parámetros.
API_KEY = os.getenv("API_KEY")
logging.warning(API_KEY)
#dbPredictionsManager = DbManager(os.getenv("DB_Predictions"),'PredictionsDB','predictions_v2')
#Creamos la instancia del recurso para la gestión de recetas, pasándole
#como parámetro la instancia del manejador de la BD con el objetivo
#de respetar la 'single source of truth' con la inyección de dependencias.
predictions = Prediction(API_KEY)#dbPredictionsManager)
#Definimos la ruta 'receipes', sobre la que se ejecutarán los request
#definidos en el recurso de la clase 'Receipe' creado.
api.add_route('/servicio/v2/prediccion', predictions)



