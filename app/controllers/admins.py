from app import app
from flask import render_template, redirect, request, session, flash
from app.models.topping import Topping
from app.models.user import Users
from app.models.order import Order

import decimal

from app.api.GrosseryStore import get_price
from app.api.VariablePrices import getPriceSize, getPriceCrust


@app.route("/dashboard")
def dashboard():
    user_id = session['user_id']
    if 'user_id' not in session:
            return redirect("/login")
    data = {
    "id": session['user_id']
    }
    user = Users.get_one(data)
    if user[0]["admin"] != 1:
        return render_template('home.html')
    orders = Order.get_all_orders_info()
    print("hola", orders)
    ordenes = []
    ordenes[0]["completadas"] = []
    ordenes["pendientes"] = 0
    ordenes["canceladas"] = 0
    # ordenes["qty"] = len(orders)
    for order in orders:
        if order["completo"] == 1:
            ordenes["completadas"] += 1
        if order["pendiente"] == 1:
            ordenes["pendientes"] += 1
        if order["cancelado"] == 1:
            ordenes["canceladas"] += 1
    ordenes["ventas"] = 0
    ordenes["costos"] = 0
    for order in orders:
        ordenes["ventas"] += order["precio"]
        cost = get_price(order["url"])
        qty = order["QTY"]
        medida = order["medida"]
        totalCostUsd = qty * ((cost * medida) /800)
        order["toppingCost"] = totalCostUsd
        sizePrice = getPriceSize(order["size"])
        crustPrice = getPriceCrust(order["crust"])
        order["structureCost"] = sizePrice + crustPrice
        order["costoTotal"] = totalCostUsd + sizePrice + crustPrice
        ordenes["costos"] += order["costoTotal"]
    return render_template('orders_admin.html', all_orders = ordenes )


@app.route("/orders")
def orders_admin():
    user_id = session['user_id']
    if 'user_id' not in session:
            return redirect("/login")
    data = {
    "id": session['user_id']
    }
    user = Users.get_one(data)
    if user[0]["admin"] != 1:
        return render_template('home.html')
    orders = Order.get_all_orders_info()
    for order in orders:
        if order["completo"] == 1:
            order["estado"] = "completo"
        if order["pendiente"] == 1:
            order["estado"] = "pendiente"
        if order["cancelado"] == 1:
            order["estado"] = "cancelado"
    print("hola", orders)
    for order in orders:
        cost = get_price(order["url"])
        qty = order["QTY"]
        medida = order["medida"]
        totalCostUsd = qty * ((cost * medida) /800)
        order["toppingCost"] = totalCostUsd
        sizePrice = getPriceSize(order["size"])
        crustPrice = getPriceCrust(order["crust"])
        order["structureCost"] = sizePrice + crustPrice
    return render_template('orders_admin.html', all_orders = orders )

@app.route("/toppings")
def toppings():
    user_id = session['user_id']
    if 'user_id' not in session:
        return redirect("/login")
    data = {
    "id": session['user_id']
    }
    user = Users.get_one(data)
    dataToppings = Topping.get_all()
    for dataTopping in dataToppings:
        cost = get_price(dataTopping["url"])
        dataTopping["cost"] = cost
    
    if user[0]["admin"] != 1:
        return render_template('home.html')
    else:
        return render_template('toppings.html', dataToppings = dataToppings, usd = 800)

@app.route("/create_topping", methods=["POST"])
def create_topping():
    Topping.save(request.form)
    if request.form.get('toppings') != None:
        flash("your topping has been created successfully!")
        return redirect('/toppings')
    
    
@app.route('/logout')
def logoutAdmin():
    session.clear()
    return redirect('/')

@app.route("/edit/<int:id>")
def edit_topping(id):
    topping = Topping.get_toppings({"toppings_id": id})
    print(topping)
    return render_template("edit_toppings.html", topping = topping[0])

@app.route("/update_toppings/<int:id>", methods=["POST"])
def update_topping(id):
    data = {
        "toppings_id": id,
        "toppings": request.form['toppings'],
        "url": request.form['url']
    }
    Topping.update(data)
    return redirect("/toppings")
