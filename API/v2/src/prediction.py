# -*- coding: utf-8 -*-
import falcon
import json
import sys
import logging
import requests
from falcon_cors import CORS
from bson import ObjectId
from datetime import datetime
from falcon import HTTP_400, HTTP_501, HTTP_404, HTTP_200

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
    def __init__(self, api_key):
        #Inyección de dependencia
        #self.dbManager = dbManager
        self.api_key = api_key
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
        n_periods = 1
        if(method == '24'):
            n_periods = 8
        elif(method == '48'):
            n_periods = 16
        elif(method == '72'):
            n_periods = 32
        elif(method == 'ok'):
            res['status'] = HTTP_200 
            res['data'] = 'OK!' 
            res['msg'] = 'OK'
            return res
        #Manejar error en cado de llamar a un método no definido
        else:
            res['status'] = HTTP_501 #Método no implementado
            res['msg'] = 'Error: method not implemented'
            return res

        res = self.getPrediction(n_periods)
        #Devolvemos la respuesta
        return res

    def getPrediction(self, times):
        #Estrutura de respuesta por defecto
        res = {
            "status": HTTP_200, #Ok
            "data": None,
            "msg": "Default"
        }
        #Predicciones 
        params = {
            'appid': self.api_key,
            'q': 'San Francisco'
        }
        api_result = requests.get('http://api.openweathermap.org/data/2.5/forecast', params)
        api_response = api_result.json()
        logging.warning(self.api_key)
        logging.warning(api_response)
        res['data'] = self.format_json(times, api_response['list'])
        return res

    def format_json(self, n_periods, fc):
        resp_data = []
        for i in range(n_periods):
            resp_data.append(dict(hour=fc[i]['dt_txt'],temperature=str(fc[i]['main']['temp']),humidity=str(fc[i]['main']['humidity'])))
        return resp_data

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

