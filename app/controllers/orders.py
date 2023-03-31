from app import app
from flask import render_template,redirect,request,session,flash
from app.models.order import Order
from app.models.pizza import Pizza
from app.models.topping import Topping
from app.models.user import Users
from app.models.pizzaTopping import PizzaToppings


@app.route("/craft")
def craft():
    if 'user_id' not in session:
        return redirect('/')
    data = {
    "id": session['user_id']
    }
    user = Users.get_one(data)
    toppings = Topping.get_all()
    return render_template('craft.html', all_topping = toppings,user = user)

@app.route("/order",methods=['POST'])
def create_pizza():
    print(request.form)
    data = {
        "users_id": request.form["userSession"]
    }
    dataToppings = {
        "toppings" : request.form["toppings"]
    }
    Order.save(data["users_id"])
    order_id = Order.get_order_id_2(data["users_id"])
    print(order_id)
    data_pizza = {
        "method": request.form["method"],
        "size": request.form["size"],
        "crust": request.form["crust"],
        "QTY": request.form["QTY"],
        "order_id": order_id,
        'toppings': request.form["toppings"]
    }
    Pizza.save(data_pizza)
    pizza_id = Pizza.get_pizza_id(data_pizza['order_id'])
    toppings_id = Topping.getId(dataToppings)
    data_pizza_toppings = {
        "pizza_id": pizza_id,
        "toppings_id": toppings_id
    }
    PizzaToppings.save(data_pizza_toppings)
    orders = Order.get_all()
    toppings = [1,2,3]
    return render_template('order.html', all_orders = orders, toppings = toppings)


@app.route("/order")
def account_order():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('order.html')

@app.route("/delete/<int:id>")
def delete_order(id):
    data = {
        'id': id
    }
    orders = Order.delete_order(data)
    return redirect('/home')
