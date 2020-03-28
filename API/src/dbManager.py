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
    def get(self,param='all',value='all',k=10):
        #Definción de respuesta por defecto.
        resp = {
            "status": HTTP_200, 
            "data": None,
            "msg": "Success"
        }

        lista = True
        try:
            #Obtener todos los documentos de la colección.
            if(param == 'all'):
                res = self.collection.find()
            elif(param == 'films'):
                res = self.collection.aggregate([
                                                 {'$sample': {'size': int(value)}}
                                                ])
            #Obtener un documento dado un identificador de usuario.
            elif(param == 'user_id'):
                res = self.collection.find_one({'user_id': value})
                lista=False
            #Obtener un documento dado un identificador de película.
            elif(param == 'film_id'):
                res = self.collection.find_one({'film_id': value})
                lista=False
            #Obtener todas las recomendaciones dada para un usuario
            elif(param == 'user_recommendations'):
                res = self.collection.aggregate([
                                                {'$match': {'user_id': value}},
                                                {'$lookup': {
                                                    'from': "films",
                                                    'localField': "recommendations_items",
                                                    'foreignField': "film_id",
                                                    'as': "recommendations_films"
                                                    }
                                                }
                                                ])
            #Obtener un vecindario aleatorio de tamaño k para un usuario dado
            elif(param == 'neighborhood'):
                res = self.collection.aggregate([
                                                 {'$match': {'user_id': { '$ne': value }}},
                                                 {'$sample': {'size': k}}
                                                ])
            #Obtener un documento dado otro parámetro.
            else: 
                res = self.collection.find({param:value})
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

    #Método para la inserción de docs en la colección establecida.
    def insert(self,document):
        #Definición de respuesta por defecto.
        resp = {
            "status": HTTP_201, 
            "data": None,
            "msg": "Success"
        }

        #Insertamos en la colección el documento recibido y preparamos 
        #la respuesta.
        try:
            res = self.collection.insert_one(document).inserted_id
        except Exception as ex:
            self.logger.error(ex)

        #Modificamos el estado y el mensaje en caso de producirse un error
        #en la inserción.
        if(res == None):
            resp['msg']="Error"
            resp['status']=HTTP_400
        else:
            #Devolvemos el identificador de la receta insertada como 
            #campo data de la respuesta.
            resp['data']=res

        return resp

    #Método para la inserción de docs en la colección establecida.
    def update(self,document, field, value):
        #Definición de respuesta por defecto.
        resp = {
            "status": HTTP_201, 
            "data": None,
            "msg": "Success"
        }

        #Insertamos en la colección el documento recibido y preparamos 
        #la respuesta.
        try:
            if(field == 'ratings'):
                item = self.collection.find_one({
                    '_id': document['_id'],
                    'items': value[0] 
                })
                
                if (item != None):
                    index = item['items'].index(value[0])
                    res = self.collection.update(
                        {'_id': document['_id']},
                        { '$set': {'ratings.'+str(index): value[1],
                                    'items.'+str(index): value[0],
                                    'items_ratings.'+str(index): value}}
                        )
                else:
                    res = self.collection.update(
                        {'_id': document['_id']},
                        { '$push': {'ratings': value[1],
                                    'items': value[0],
                                    'items_ratings': value}}
                        )
            else:
                res = self.collection.update_one(
                    {'_id': document['_id']},
                    { '$set': { field: value}}
                )

        except Exception as ex:
            self.logger.error(ex)

        #Modificamos el estado y el mensaje en caso de producirse un error
        #en la inserción.
        if(res == None):
            resp['msg']="Error"
            resp['status']=HTTP_400
        else:
            #Devolvemos el identificador de la receta insertada como 
            #campo data de la respuesta.
            resp['data']=res

        return resp
       
            
    