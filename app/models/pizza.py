from app.config.mysqlconnection import connectToMySQL
from flask import flash


# modelar la clase después de la tabla friend de nuestra base de datos
class Pizza:
    def __init__( self , data ):
        self.id = data['id']
        self.precio = data['precio']
        self.method = data['method']
        self.size = data['size']
        self.crust = data['crust']
        self.QTY = data['QTY']
        self.toppings = data['toppings']
        self.updated_at = data['created_at']
        self.updated_at = data['updated_at']
        self.toppings = []
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
        query = "INSERT INTO pizza ( precio, method , size , crust , QTY, toppings, created_at, updated_at ) VALUES (%(precio)s,%(method)s,%(size)s,%(crust)s,%(QTY)s, %(toppings)s,NOW(),NOW())"
        # data es un diccionario que se pasará al método de guardar desde server.py
        result = connectToMySQL('pizzabd').query_db( query, data )
        return result

