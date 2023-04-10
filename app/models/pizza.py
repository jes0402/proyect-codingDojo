from app.config.mysqlconnection import connectToMySQL
from app.models import topping
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
        self.updated_at = data['created_at']
        self.updated_at = data['updated_at']
        self.toppings = []
    # ahora usamos métodos de clase para consultar nuestra base de datos
    
    def calcular_precio(data):
        precio = 0
        size = data['size']
        QTY = data['QTY']
        toppings = data['toppings']

        # calcular el precio segun el tamaño
        if size == "Medium":
            precio += 16.99
        if size == "Large":
            precio += 20.99
        if size == "Small":
            precio += 11.99

        # calcular el precio segun la cantidad de pizzas
        precio = precio * float(QTY)

        # calcular el precio segun los toppings
        precio += len(toppings)

        data["precio"] = precio
        return data

    @classmethod
    def save(cls, data):
        data = cls.calcular_precio(data)
        query = "INSERT INTO pizza (orders_id, precio, method, size, crust, QTY, created_at, updated_at) VALUES (%(order_id)s, %(precio)s, %(method)s, %(size)s, %(crust)s, %(QTY)s, NOW(), NOW())"
        connectToMySQL('pizzabd').query_db(query, data)
        return data
    
    @classmethod
    def get_pizza_id(cls, data):
        query = "SELECT id from pizza where orders_id = %(order_id)s"
        results = connectToMySQL('pizzabd').query_db(query,data)
        return results

    @staticmethod
    def validate_pizza(data):
        is_valid = True
        if not data.get('method'):
            is_valid = False
            flash("Method is required" ,"craft")
        if not data.get('size'):
            is_valid = False
            flash("Size is required","craft")
        if not data.get('crust'):
            is_valid = False
            flash("Crust is required","craft")
        if not data.get('QTY'):
            is_valid = False
            flash("QTY is required","craft")

        return is_valid