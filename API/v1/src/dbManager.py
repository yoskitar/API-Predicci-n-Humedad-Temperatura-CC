# -*- coding: utf-8 -*-
import pymongo
from bson.objectid import ObjectId
from falcon import HTTP_200, HTTP_201, HTTP_404, HTTP_400

#Definición de la clase para la gestión de la BD.
class DbManager:
    #Inicializamos la instancia estableciendo la BD y 
    #colección sobre la que trabajaremos.
    def __init__(self,URI,db,collection):
        myclient = pymongo.MongoClient(URI)
        mydb = myclient[db]
        self.collection = mydb[collection]

    #Método para la obtención de documentos de la colección
    #establecida, atendiendo al valor de 'param' en el que se
    #especifica qué metodo de consulta ejecutar, y con que valor,
    #indicado en el parámetro 'value'. Con el parámetro 'k' 
    #obtenemos obtenemos solo un vecindario de 'k' vecinos.
    def get(self,param='all',value='all'):
        #Definción de respuesta por defecto.
        resp = {
            "status": HTTP_200, 
            "data": None,
            "msg": "Success"
        }

        lista = True 
        res = None
        try:
            #Obtener todos los documentos de la colección.
            if(param == 'all'):
                res = self.collection.find()
        except Exception as ex:
            self.logger.error(ex)
        
        #Gestionar errores en la consulta.
        if(res == None):
            resp['msg']="Error"
            resp['status']=HTTP_404
        else:
            #Componemos la respuesta de forma adecuada
            if(lista):
                docs=[]
                for doc in res:
                    docs.append(doc)
                resp['data']=docs
            else:
                resp['data']=res

        return resp

    