from app import app
from flask import render_template,redirect,request,session,flash
from app.models.order import Order
from app.models.pizza import Pizzas
from app.models.topping import Toppings
from app.models.user import Users
from app.models.pizza_topping import Pizza_topping


@app.route("/craft")
def craft():
    if 'user_id' not in session:
        return redirect('/')
    data = {
    "id": session['user_id']
    }
    user = Users.get_one(data)
    toppings = Toppings.get_all()
    return render_template('craft.html', all_topping = toppings,user = user)

@app.route("/order",methods=['POST'])
def create_pizza():
    data = {
        "method": request.form["method"],
        "size": request.form["size"],
        "crust": request.form["crust"],
        "QTY": request.form["QTY"],
        "toppings" : ','.join(request.form.getlist('toppings[]')),
        "user_id": request.form["userSession"]
    }
    order = Order.save(data)
    data["order_id"] = order
    pizza = Pizzas.save(data)
    data["pizza_id"] = pizza
    print("hola", pizza)
    pizza_toppings = Pizzas.add_topping(data)
    data["topping_id"] = pizza_toppings
    orders = Order.get_order_id(data)
    data["list_toppings"] = data["toppings"].split(",")
    toppings = Toppings.getId(data)
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
