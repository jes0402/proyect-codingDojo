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
    is_valid = Pizza.validate_pizza(request.form)
    if not is_valid:
        return redirect("/")
    if request.form.get('toppings') == None:
        flash("Please select at least one topping","craft")
        return redirect('/craft')
    print(request.form['toppings'])
    dataOrderSave = {
        "users_id": request.form["userSession"]
    }
    order_id = Order.save(dataOrderSave)
    dataOrderID = {"order_id": order_id}
    data_pizza = {
        "method": request.form["method"],
        "size": request.form["size"],
        "crust": request.form["crust"],
        "QTY": request.form["QTY"],
        "order_id": dataOrderID['order_id'],
        'toppings': request.form["toppings"]
    }
    pizza = Pizza.save(data_pizza)
    pizza_id = Pizza.get_pizza_id(data_pizza)
    data_pizza_toppings = {
        "pizza_id": pizza_id[0]['id'],
        "toppings_id": request.form["toppings"]
    }
    pizza_toppings = PizzaToppings.save(data_pizza_toppings )
    toppings = Topping.get_toppings(data_pizza_toppings)
    print(toppings)
    orders = Order.get_all_orders()
    return render_template('order.html', all_orders = orders, toppings = toppings )


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
