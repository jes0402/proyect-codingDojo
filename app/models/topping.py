from app.config.mysqlconnection import connectToMySQL
from app.models import pizza
from flask import flash


# modelar la clase después de la tabla friend de nuestra base de datos
class Topping:
    def __init__( self , data ):
        self.id = data['id']
        self.toppings = data['toppings']
        self.updated_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pizza = []
    # ahora usamos métodos de clase para consultar nuestra base de datos
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO toppings ( toppings , created_at, updated_at ) VALUES (%()s, NOW(),NOW())"
        # data es un diccionario que se pasará al método de guardar desde server.py
        result = connectToMySQL('pizzabd').query_db( query, data )
        return result
        
    @classmethod
    def getId(cls, data ):
        query = "select toppings from toppings where id in ({})".format(data["toppings"])
        # data es un diccionario que se pasará al método de guardar desde server.py
        results = connectToMySQL('pizzabd').query_db( query, data )
        toppings_list = [item['toppings'] for item in results]
        return toppings_list
    
    @classmethod
    def get_all(data):
        query = "SELECT * FROM toppings"
        results = connectToMySQL('pizzabd').query_db(query)
        toppings = []
        for topping in results:
            toppings.append(topping)
        return toppings

