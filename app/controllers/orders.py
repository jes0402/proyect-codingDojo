from app import app
from flask import render_template,redirect,request,session,flash
from app.models.order import Order
from app.models.pizza import Pizza
from app.models.topping import Topping
from app.models.user import Users
from app.models.pizzaTopping import PizzaToppings
from app.controllers.stripe import stripe_keys


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
        return redirect("/craft")
    if request.form.get('toppings') == None:
        flash("Please select at least one topping","craft")
        return redirect('/craft')
    dataOrderSave = {
        "users_id": request.form["userSession"]
    }
    toppings_list = request.form.getlist('toppings')
    order_id = Order.save(dataOrderSave)
    dataOrderID = {"order_id": order_id}
    data_pizza = {
        "method": request.form["method"],
        "size": request.form["size"],
        "crust": request.form["crust"],
        "QTY": request.form["QTY"],
        "order_id": dataOrderID['order_id'],
        'toppings': toppings_list
    }
    pizza = Pizza.save(data_pizza)
    pizzaId = Pizza.get_pizza_id(data_pizza)
    for topping in toppings_list:
        data_pizza_toppings = {
            "pizza_id": pizzaId[0]['id'],
            "toppings_id": topping
        }
        PizzaToppings.save(data_pizza_toppings)
    toppings = Topping.get_toppings_by_id(toppings_list)
    orders = Order.get_order_info(dataOrderID)
    toppingsPrice = len(toppings) * 1.5
    print(orders[0])
    totalPrice = orders[0]['precio'] + toppingsPrice
    return render_template('order.html', all_orders = orders, toppings = toppings, key=stripe_keys['publishable_key'], toppingsPrice = toppingsPrice, totalPrice = totalPrice)


# @app.route("/orders")
# def account_order():
#     if 'user_id' not in session:
#         return redirect('/')
#     orders = Order.get_all_orders_info()
    
#     return render_template('order.html', all_orders = orders, toppings = [1,2,3])

@app.route("/delete/<int:id>")
def delete_order(id):
    data = {
        'id': id
    }
    orders = Order.delete_order(data)
    return redirect('/home')

@app.route("/cancel/<int:id>")
def cancel_order(id):
    data = {
        'id': id
    }
    orders = Order.cancel_order(data)
    return redirect('/home')

