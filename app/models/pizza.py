from app.config.mysqlconnection import connectToMySQL
from flask import flash
from app.models import topping
from app.models import pizza_topping


# modelar la clase después de la tabla friend de nuestra base de datos
class Pizzas:
    def __init__( self , data ):
        self.id = data['id']
        self.orders_id = data['order_id']
        self.precio = data['precio']
        self.method = data['method']
        self.size = data['size']
        self.crust = data['crust']
        self.QTY = data['QTY']
        self.updated_at = data['created_at']
        self.updated_at = data['updated_at']

    # ahora usamos métodos de clase para consultar nuestra base de datos
    
    def calcular_precio(data):
        precio = 0
        size = data['size']
        QTY = data['QTY']
        toppings = data['toppings']
        
        #calcular el precio segun el tamaño
        if size == "Medium":
            precio += 16.99
        if size == "Large":
            precio += 20.99
        if size == "Small":
            precio += 11.99
            
        #calcular el precio segun la cantidad de pizzas   
        
        precio = precio * float(QTY)
        
        #calcular el precio segun los toppings 
        precio += len(toppings)
        
        data["precio"] = precio
        
    @classmethod
    def save(cls, data ):
        cls.calcular_precio(data)
        query = "INSERT INTO pizzas ( order_id, precio, method , size , crust , QTY,created_at, updated_at ) VALUES (%(order_id)s,%(precio)s,%(method)s,%(size)s,%(crust)s,%(QTY)s,NOW(),NOW())"
        # data es un diccionario que se pasará al método de guardar desde server.py
        result = connectToMySQL('pizzabd').query_db( query, data )
        return result
    
    @classmethod
    def add_topping(cls,data): # add relationship in burgers_toppings table
        query = "INSERT INTO pizza_toppings (pizza_id, toppings_id,created_at,updated_at) VALUES (%(pizza_id)s,%(topping_id)s,NOW(),NOW());"
        return connectToMySQL('pizzabd').query_db(query,data)

