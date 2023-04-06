from app.config.mysqlconnection import connectToMySQL
from flask import flash


# modelar la clase después de la tabla friend de nuestra base de datos
class Order:
    def __init__( self , data ):
        self.id = data['id']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.completo = data['completo']
        self.pendiente = data['pendiente']
        self.cancelado = data['cancelado']

    # ahora usamos métodos de clase para consultar nuestra base de datos
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO orders (users_id ,created_at, updated_at, completo, pendiente, cancelado ) VALUES (%(users_id)s,NOW(),NOW(), false, true, false)"
        # data es un diccionario que se pasará al método de guardar desde server.py
        result = connectToMySQL('pizzabd').query_db( query, data )
        return result

    
    @classmethod
    def get_all_orders_info(cls, data = {}):
        query = "SELECT * FROM orders LEFT JOIN pizza ON pizza.orders_id = orders.id JOIN pizza_toppings ON pizza_toppings.pizza_id = pizza.id JOIN toppings ON toppings.id = pizza_toppings.toppings_id"
        results = connectToMySQL('pizzabd').query_db(query, data)
        return results

    @classmethod
    def get_order_info(cls, data):
        query = "SELECT orders.id, precio, method, QTY, size, crust FROM users JOIN orders ON orders.users_id = users.id JOIN pizza ON pizza.orders_id = orders.id WHERE orders.id = %(order_id)s"
        results = connectToMySQL('pizzabd').query_db(query, data)
        return results
    
    @classmethod
    def get_info_for_dashboard(cls, data):
        query = "SELECT * FROM orders where id = %(order_id)s"
        results = connectToMySQL('pizzabd').query_db(query, data)
        return results
    

    @classmethod
    def get_order_id(cls):
        query = "select orders.id, precio, method, QTY, size, crust, toppings from users JOIN orders on orders.users_id = users.id  JOIN pizza on pizza.id = orders.pizza_id WHERE orders.id = %(order_id)s"
        results = connectToMySQL('pizzabd').query_db(query)
        return results
    
    @classmethod    
    def get_order_id_2(cls, data):
        query= "SELECT id from orders where users_id = %(id)s"
        results = connectToMySQL('pizzabd').query_db(query,data)
        return results
    
    @classmethod
    def delete_order(cls, data):
        query = "DELETE from orders WHERE id = %(id)s"
        results = connectToMySQL('pizzabd').query_db(query, data)
        return results
    
    @classmethod
    def cancel_order(cls, data):
        query = "UPDATE orders SET completo = false, pendiente = false, cancelado = true WHERE id = %(id)s"
        results = connectToMySQL('pizzabd').query_db(query, data)
        return results
    
    @classmethod
    def finish_order(cls, data):
        query = "UPDATE orders SET completo = true, pendiente = false, cancelado = false WHERE id = %(id)s"
        results = connectToMySQL('pizzabd').query_db(query, data)
        return results



    
