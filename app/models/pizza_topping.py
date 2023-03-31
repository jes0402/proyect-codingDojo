from app.config.mysqlconnection import connectToMySQL
from app.models import topping
from app.models import pizza
from flask import flash


# modelar la clase después de la tabla friend de nuestra base de datos
class Pizza_topping:
    def __init__( self , data ):
        self.id = data['id']
        self.toppings = data['pizza_id']
        self.toppings = data['toppings_id']
        self.updated_at = data['created_at']
        self.updated_at = data['updated_at']
    # ahora usamos métodos de clase para consultar nuestra base de datos
    
