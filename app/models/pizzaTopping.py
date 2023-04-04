from app.config.mysqlconnection import connectToMySQL
from flask import flash


# modelar la clase después de la tabla friend de nuestra base de datos
class PizzaToppings:
    def __init__( self , data ):
        self.id = data['id']
        self.updated_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pizza = []
    # ahora usamos métodos de clase para consultar nuestra base de datos
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO pizza_toppings ( created_at, updated_at, pizza_id, toppings_id ) VALUES (NOW(),NOW(), %(pizza_id)s, %(toppings_id)s )"
        # data es un diccionario que se pasará al método de guardar desde server.py
        result = connectToMySQL('pizzabd').query_db( query, data )
        return result
        
    @classmethod
    def getId(cls, data ):
        query = "select id from pizza_toppings where pizza_id = %(pizza_id)s and toppings_id = %(toppings_id)s"
        # data es un diccionario que se pasará al método de guardar desde server.py
        results = connectToMySQL('pizzabd').query_db( query, data )
        return results
    
    @classmethod
    def get_all(data):
        query = "SELECT * FROM pizza_toppings"
        results = connectToMySQL('pizzabd').query_db(query)
        toppings = []
        for topping in results:
            toppings.append(topping)
        return toppings