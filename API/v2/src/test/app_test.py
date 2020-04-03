from falcon import testing, HTTP_200, HTTP_201, HTTP_400, HTTP_501
import sys
#Testeamos desde la ruta principal, donde está alojado el tasks.py
sys.path.append("src/")
from app import api

#Testeamos el micro-servicio de análisis de recetas con el módulo
#testing del framework falcon.
class Tester(testing.TestCase):
    def setUp(self):
        super(Tester,self).setUp()
        #Asignamos el módulo api importado de la clase donde
        #hemos instanciado el APIrest con falcon.
        self.app = api
    
#Definimos las funciones de test sobre los diferentes recursos y métodos
#definidos para cada uno de ellos.
class TestApp(Tester):
    #Función para testear que la ruta está disponible
    def test_get_ok(self):
        result = self.simulate_get('/servicio/v2/prediccion?hours=ok')
        print(result)
        self.assertEqual(result.status, HTTP_200)

    #Función para testear la llamada de un método no definido sobre el recurso get
    def test_get_notDefined(self):
        result = self.simulate_get('/servicio/v2/prediccion?hours=20')
        self.assertEqual(result.status, HTTP_501)

    

