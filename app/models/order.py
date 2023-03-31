from app.config.mysqlconnection import connectToMySQL
from flask import flash


# modelar la clase después de la tabla friend de nuestra base de datos
class Order:
    def __init__( self , data ):
        self.id = data['id']
        self.users_id = data['user_id']
        self.updated_at = data['created_at']
        self.updated_at = data['updated_at']
        self.completo = data['completo']
        self.pendiente = data['pendiente']
        self.cancelado = data['cancelado']
    # ahora usamos métodos de clase para consultar nuestra base de datos
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO orders (user_id,completo,pendiente, cancelado, created_at, updated_at ) VALUES (%(user_id)s,0,0,0,NOW(),NOW())"
        # data es un diccionario que se pasará al método de guardar desde server.py
        result = connectToMySQL('pizzabd').query_db( query, data )
        return result
    

    
    @classmethod
    def get_all_orders(cls, data):
        query = "select orders.created_at,QTY,size,toppings from users JOIN orders on orders.user_id = users.id JOIN pizzas on pizzas.id = orders.pizza_id WHERE user.id = %(user_id)s"
        results = connectToMySQL('pizzabd').query_db(query, data)
        print("hola", results)
        
    @classmethod
    def get_order_id(cls, data):
        query = "select orders.id, precio, method, QTY, size, crust, pizza_toppings.toppings_id from users JOIN orders on orders.user_id = users.id JOIN pizzas on pizzas.orders_id = orders.id JOIN pizza_toppings on pizza_toppings.pizza_id = pizzas.id WHERE orders.id = %(order_id)s"
        results = connectToMySQL('pizzabd').query_db(query,data)
        return results
    
    @classmethod
    def delete_order(cls, data):
        query = "DELETE from orders WHERE id = %(id)s"
        results = connectToMySQL('pizzabd').query_db(query, data)
        return results
