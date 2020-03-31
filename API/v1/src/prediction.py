# -*- coding: utf-8 -*-
import falcon
import json
import sys
import pandas as pd
import pmdarima as pm
from falcon_cors import CORS
from bson import ObjectId
from falcon import HTTP_400, HTTP_501, HTTP_404

#Clase creada para procesar el campo 'data' que será devuelto
#como parte del 'body' en la respuesta al request realizado.
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        #Si es del tipo ObjectID, es necesario pasar la respuesta
        #a String para evitar errores.
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#Clase para la definición del recurso 'Receipe', encargado de
#gestionar las peticiones al endpoint '/receipes'.
class Prediction(object):
    #Establecemos el manejador de la BD para respetar la
    #'Single source of truth'.
    def __init__(self, dbManager):
        #Inyección de dependencia
        self.dbManager = dbManager
        cors = CORS(allow_all_origins=True)
        
    #Método para procesar un petición Get.
    def get(self, method):
        #Estrutura de respuesta por defecto
        res = {
            "status": HTTP_400, #Bad request
            "data": method,
            "msg": "Default"
        }
        #Discriminamos el método indicado como parámetro
        #para realizar el get atendiendo al atributo deseado
        #del documento.
        n_periods = 0
        if(method == '24hours'):
            n_periods = 24
        elif(method == '48hours'):
            n_periods = 48
        elif(method == '72hours'):
            n_periods = 72
        #Manejar error en cado de llamar a un método no definido
        else:
            res['status'] = HTTP_501 #Método no implementado
            res['msg'] = 'Error: method not implemented'
            return res

        res = self.getPrediction(n_periods)
        #Devolvemos la respuesta
        return res


    def getPrediction(self, nperiods):
        #Estrutura de respuesta por defecto
        res = {
            "status": HTTP_400, #Bad request
            "data": None,
            "msg": "Default"
        }
        #Obtener datos de temperatura y humedad de la BD
        res = self.dbManager.get()
        #Convertir datos a dataframe
        df = pd.DataFrame(data=res['data'])
        #Predicciones 
        predictionsTemperature = self.predict(df.temperature, nperiods)
        predictionsHumidity = self.predict(df.humidity, nperiods)
        res['data'] = predictionsTemperature

        return res

    def predict(self, df_column, n_periods_param):
        model = pm.auto_arima(df_column, start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)
        # Forecast
        fc, confint = model.predict(n_periods=n_periods_param, return_conf_int=True)
        return fc

    def post(self, data):
        #Estrutura de respuesta por defecto
        res = {
            "status": HTTP_501, #Bad request
            "data": None,
            "msg": "Error: method POST not implemented"
        }
        #Devolvemos la respuesta
        return res

    #Método que será llamado cuando se ejecute una petición
    #get sobre el el recurso para el API.
    def on_get(self, req, resp):
        #Obtenemos los parámetros como queryParams en el URL
        methodParam = req.params['hours'] or ""
        #Procesamos la petición
        res = self.get(method=methodParam)
        #Establecemos la respuesta
        resp.status = res['status']
        resp.body = JSONEncoder().encode(res['data'])

    #Método que será llamado cuando se ejecute una petición
    #post sobre el el recurso para el API.
    def on_post(self, req, resp):
        #Obtenemos los parámetros como json en el body de la petición
        data = json.loads(req.stream.read(sys.maxsize).decode('utf-8'))
        #Procesamos la petición
        res = self.post(data=data)
        #Establecemos la respuesta
        resp.status = res['status']
        resp.body = JSONEncoder().encode(res['data'])

