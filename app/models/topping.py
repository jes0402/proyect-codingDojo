from app.config.mysqlconnection import connectToMySQL
from app.models import pizza
from flask import flash


# modelar la clase después de la tabla friend de nuestra base de datos
class Topping:
    def __init__( self , data ):
        self.id = data['id']
        self.toppings = data['toppings']
        self.url = data['url']
        self.price = data['price']
        self.medida = data['medida']
        self.updated_at = data['created_at']
        self.updated_at = data['updated_at']
        
    # ahora usamos métodos de clase para consultar nuestra base de datos
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO toppings ( toppings , url, medida, price, created_at, updated_at ) VALUES (%(toppings)s, %(url)s, %(medida)s, %(price)s, NOW(),NOW())"
        # data es un diccionario que se pasará al método de guardar desde server.py
        result = connectToMySQL('pizzabd').query_db( query, data )
        return result
    
    @classmethod
    def updateCost(cls, data):
        query = "UPDATE toppings SET price = %(price)s where id = %(id)s"
        results = connectToMySQL('pizzabd').query_db(query,data)
        return results
        
    @classmethod
    def get_toppings_by_id(cls, data):
        query = "SELECT * FROM toppings WHERE id = %(id)s"
        results = connectToMySQL('pizzabd').query_db(query, data)
        print("resulllllts", results)
        return results

    @classmethod
    def get_toppings_by_i2(cls, toppings):
        toppings_id = ",".join(toppings)
        query = "select * from toppings where id in ({})".format(toppings_id)
        # data es un diccionario que se pasará al método de guardar desde server.py
        results = connectToMySQL('pizzabd').query_db( query, {} )
        print(results)
        toppings = []
        for topping in results:
            toppings.append(topping)
        return toppings

    @classmethod
    def get_url_by_id(cls, data ):
        query = "SELECT url FROM toppings WHERE id = %(id)s"
        results = connectToMySQL('pizzabd').query_db(query, data)
        return results
    
    def get_toppings_by_pizza_id(data):       
        query = "select * from toppings where id in (select toppings_id from pizza_toppings where pizza_id = %(pizza_id)s )"
        # data es un diccionario que se pasará al método de guardar desde server.py
        results = connectToMySQL('pizzabd').query_db( query )

        toppings = []
        for topping in results:
            toppings.append(topping)
        return toppings

    @classmethod
    def get_all(data):
        query = "SELECT * FROM toppings"
        results = connectToMySQL('pizzabd').query_db(query)
        toppings = []
        for topping in results:
            toppings.append(topping)
        return toppings
    
    @classmethod
    def get_toppings(cls, data):
        query = "select * from toppings where id = %(toppings_id)s"
        results = connectToMySQL('pizzabd').query_db(query,data)
        return results
    
    @classmethod
    def update(cls, data):
        query = "UPDATE toppings SET toppings = %(toppings)s, url = %(url)s, medida = %(medida)s, updated_at = NOW() WHERE id = %(toppings_id)s"
        results = connectToMySQL('pizzabd').query_db(query,data)
        return results

