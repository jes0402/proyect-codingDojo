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
        query = "select id from pizza where orders_id = %(order_id)s"
        results = connectToMySQL('pizzabd').query_db(query,data)
        return results
    
    @classmethod
    def get_one_with_toppings( cls , data ):
        query = "SELECT * FROM pizza LEFT JOIN pizza_toppings ON pizza_toppings.pizza_id = pizza.id LEFT JOIN toppings ON pizza_toppings.toppings_id = toppings.id WHERE pizza.id = %(pizza_id)s;"
        results = connectToMySQL('pizzabd').query_db( query , data )
        print(results)
        pizza = cls( results[0] )
        for row in results:
            if not row["toppings.id"]:
                break
            topping_data = {
                "id" : row["toppings.id"],
                "toppings" : row["toppings.toppings"],
                "created_at" : row["toppings.created_at"],
                "updated_at" : row["toppings.updated_at"]
            }
            pizza.toppings.append( topping.Topping( topping_data ) )
        return pizza

    @staticmethod
    def validate_pizza(data):
        is_valid = True
        if len(data['method']) < 1:
            flash("Method is required")
            is_valid = False
        if len(data['size']) < 1:
            flash("Size is required")
            is_valid = False
        if len(data['crust']) < 1:
            flash("Crust is required")
            is_valid = False
        if len(data['QTY']) < 1:
            flash("QTY is required")
            is_valid = False
        
        return is_valid