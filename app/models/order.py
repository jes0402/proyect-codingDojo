from app.config.mysqlconnection import connectToMySQL
from flask import flash


# modelar la clase después de la tabla friend de nuestra base de datos
class Order:
    def __init__( self , data ):
        self.id = data['id']
        self.pizza_id = data['pizza_id']
        self.users_id = data['users_id']
        self.updated_at = data['created_at']
        self.updated_at = data['updated_at']
    # ahora usamos métodos de clase para consultar nuestra base de datos
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO orders ( pizza_id , users_id ,created_at, updated_at ) VALUES (%(pizza_id)s,%(users_id)s,NOW(),NOW())"
        # data es un diccionario que se pasará al método de guardar desde server.py
        result = connectToMySQL('pizzabd').query_db( query, data )
        return result

    
    @classmethod
    def get_all_orders(cls):
        query = "select method, QTY, size, crust, toppings from users JOIN orders on orders.users_id = %(id)s  JOIN pizza on pizza.id = orders.pizza_id JOIN pizza_toppings on pizza_toppings.pizza_id = pizza.id JOIN toppings on toppings.id = pizza_toppings.toppings_id"
        results = connectToMySQL('pizzabd').query_db(query)
        return results
        
    @classmethod
    def get_order_id(cls, data):
        query = "select orders.id, precio, method, QTY, size, crust, toppings from users JOIN orders on orders.users_id = users.id  JOIN pizza on pizza.id = orders.pizza_id WHERE orders.id = %(order_id)s"
        results = connectToMySQL('pizzabd').query_db(query,data)
        return results
    
    @classmethod
    def delete_order(cls, data):
        query = "DELETE from orders WHERE id = %(id)s"
        results = connectToMySQL('pizzabd').query_db(query, data)
        return results
