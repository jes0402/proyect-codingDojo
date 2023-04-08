from app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# modelar la clase después de la tabla friend de nuestra base de datos
class Users:
    def __init__( self , data ):
        self.id = data['id']
        self.admin= data['admin']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # ahora usamos métodos de clase para consultar nuestra base de datos
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('pizzabd').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( admin, first_name , last_name , email , address, city, state, password,created_at, updated_at ) VALUES (%(admin)s, %(first_name)s,%(last_name)s,%(email)s,%(address)s,%(city)s,%(state)s,%(password)s, NOW(),NOW())"
        # data es un diccionario que se pasará al método de guardar desde server.py
        return connectToMySQL('pizzabd').query_db( query, data )
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        return connectToMySQL('pizzabd').query_db(query,data)
    
    @classmethod
    def get_admin(cls,data):
        query = "SELECT id FROM users WHERE admin = true;"
        result = connectToMySQL('pizzabd').query_db(query)
        if result:
            return cls(result[0])
        else:
            return None
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('pizzabd').query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        user = cls(results[0])
        return user
    
    @classmethod
    def edit(cls, data ):
        query = "UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s,address=%(address)s,city=%(city)s,state=%(state)s, updated_at=NOW() WHERE id = %(id)s"
        # data es un diccionario que se pasará al método de guardar desde server.py
        return connectToMySQL('pizzabd').query_db( query, data )
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            is_valid = False
            flash("First name must be at least 3 characters.","register")
        if len(user['last_name']) < 3:
            is_valid = False
            flash("last_name must be at least 3 characters.","register")
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid Email Address.","register")
        if len(user['address']) < 3:
            is_valid = False
            flash("Address must be at least 3 characters.","register")
        if len(user['city']) < 3:
            is_valid = False
            flash("city must be at least 3 characters.","register")
        if len(user['state']) < 1:
            is_valid = False
            flash("state must be at least 1 characters.","register")
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters.","register")
        if user['password'] != user['confirm']:
            is_valid = False
            flash("Passwords do not match!","register")

        return is_valid