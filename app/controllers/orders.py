from app import app
from flask import render_template,redirect,request,session,flash
from app.models.order import Order
from app.models.pizza import Pizza
from app.models.topping import Topping
from app.models.user import Users


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
    data = {
        "method": request.form["method"],
        "size": request.form["size"],
        "crust": request.form["crust"],
        "QTY": request.form["QTY"],
        "toppings" : ','.join(request.form.getlist('toppings[]')),
        "users_id": request.form["userSession"]
    }
    order = Order.save(data)
    data["orders_id"] = order
    pizza = Pizza.save(data)
    data["pizza_id"] = pizza
    orders = Order.get_order_id(data)
    data["list_toppings"] = data["toppings"].split(",")
    toppings = Topping.getId(data)
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
