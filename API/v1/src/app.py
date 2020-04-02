# -*- coding: utf-8 -*-
import falcon
import os
from prediction import Prediction
from dbManager import DbManager
from dotenv import load_dotenv

#Creamos una instancia de la API proporcionada por el framework
#falcon, ejecutable con WSGI.
api = falcon.API()
#Leemos las variables de entorno necesarias para establecer la 
#conexión con la base de datos.
load_dotenv()
#Creamos una instancia del manejador de la base de datos, para
#la BD y colección indicadas como parámetros.
dbPredictionsManager = DbManager(os.getenv("DB_Predictions"),'PredictionsDB','predictions')
#Creamos la instancia del recurso para la gestión de recetas, pasándole
#como parámetro la instancia del manejador de la BD con el objetivo
#de respetar la 'single source of truth' con la inyección de dependencias.
predictions = Prediction(dbPredictionsManager)
predictions.get_models()
#Definimos la ruta 'receipes', sobre la que se ejecutarán los request
#definidos en el recurso de la clase 'Receipe' creado.
api.add_route('/servicio/v1/prediccion', predictions)



