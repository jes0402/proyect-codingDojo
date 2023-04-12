from app.config.mysqlconnection import connectToMySQL
from app.models import topping
from flask import flash


# modelar la clase después de la tabla friend de nuestra base de datos
class PizzaToppings:
    def __init__( self , data ):
        self.id = data['id']
        self.pizza_id = data['pizza_id']
        self.toppings_id = data['toppings_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pizza = []
    # ahora usamos métodos de clase para consultar nuestra base de datos
    
    @classmethod
    def save(cls, data ):
        print(data)
        query = "INSERT INTO pizza_toppings ( pizza_id, toppings_id, created_at, updated_at) VALUES"
        # data es un diccionario que se pasará al método de guardar desde server.py
        values = []
        for toppings_id in data['toppings_id']:
            values.append("(%(pizza_id)s, %(toppings_id)s, NOW(), NOW())")
        query += ", ".join(values)
        result = connectToMySQL('pizzabd').query_db(query, data)
        print("checkpoint",result)
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
    
    @classmethod
    def get_pizza_toppings_by_pizza_id(cls, data):
        query = "select * from pizza_toppings where pizza_id = %(pizza_id)s"
        results = connectToMySQL('pizzabd').query_db( query, data )
        pizza_toppings = []
        for pizza_topping in results:
            pizza_toppings.append(pizza_topping)
        return pizza_toppings