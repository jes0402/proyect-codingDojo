from app import app
from flask import render_template, redirect, request, session, flash
from app.models.topping import Topping
from app.models.user import Users
from app.models.order import Order
from app.models.pizza import Pizza
from app.models.pizzaTopping import PizzaToppings

import decimal

from app.api.GrosseryStore import get_price
from app.api.VariablePrices import getPriceSize, getPriceCrust, usd

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
    data = []
    pizzaTopping = {}
    pizzas = {}
    pizzaTopping["cost"] = 0
    pizzas["toppings"] = []
    pizzas["QTY"] = 0
    pizzas["precio"] = 0
    pizzas["precioTotal"] = 0
    all_orders = {
        'cantidad': 0,
        'completadas': 0,
        'pendientes': 0,
        'canceladas': 0,
        'ganacia': 0,
        'costos': 0,
        'ventas': 0,

    }

    all_orders["cantidad"] = len(orders)
    for order in orders:
        data1 = {}
        if order["completo"] == 1:
            all_orders["completadas"] += 1
        if order["pendiente"] == 1:
            all_orders["pendientes"] += 1
        if order["cancelado"] == 1:
            all_orders["canceladas"] += 1
        dataPizza = {
            "order_id": order["id"]
        }     
        data1['order_id'] = order["id"]
        data1['created_at'] = order["created_at"]
        pizzas = Pizza.get_pizza_by_order_id(dataPizza)
        order["pizzas"] = pizzas

        for pizza in pizzas:
            dataPizzaToppings = {
                "pizza_id": pizza["id"]
            }
            pizzaToppings = PizzaToppings.get_pizza_toppings_by_pizza_id(dataPizzaToppings)
            data1["precio"] = pizza["precio"] * pizza["QTY"]
            all_orders["ventas"] += data1["precio"]
            medida = pizza["size"]
            costSum = 0
            for pizzaTopping in pizzaToppings:
                dataToppings = {
                    "id": pizzaTopping["toppings_id"]
                }
                toppings = Topping.get_toppings_by_id(dataToppings)
                for topping in toppings:
                    cost = topping['price']
                    costSum += cost
                    totalCostSize = getPriceSize(medida)
                    totalCostCrust = getPriceCrust(pizza["crust"])
                    totalCostUsd = (costSum + totalCostSize + totalCostCrust) * pizza["QTY"]
                    totalCost = 0
                    totalCost += totalCostUsd
                    roundTotalCost = round(totalCost)
                data1['costoTotal'] = int(roundTotalCost)
                all_orders["costos"] += data1['costoTotal']
                data1['ganacia'] = data1['precio'] - data1['costoTotal']
                all_orders["ganacia"] += data1['ganacia']

            print("daaaatataaa", data)

        data.append(data1)
            
    return render_template('dashboard.html', all_orders = all_orders )


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
    data = []
    pizzaTopping = {}
    pizzas = {}
    pizzaTopping["cost"] = 0
    pizzas["toppings"] = []
    pizzas["QTY"] = 0
    pizzas["precio"] = 0
    pizzas["precioTotal"] = 0
    for order in orders:
        data1 = {}
        if order["completo"] == 1:
            data1["estado"] = "completo"
        if order["pendiente"] == 1:
            data1["estado"] = "pendiente"
        if order["cancelado"] == 1:
            data1["estado"] = "cancelado"
        dataPizza = {
            "order_id": order["id"]
        }     
        data1['order_id'] = order["id"]
        data1['created_at'] = order["created_at"]
        pizzas = Pizza.get_pizza_by_order_id(dataPizza)
        order["pizzas"] = pizzas

        for pizza in pizzas:
            dataPizzaToppings = {
                "pizza_id": pizza["id"]
            }
            pizzaToppings = PizzaToppings.get_pizza_toppings_by_pizza_id(dataPizzaToppings)
            data1["precio"] = pizza["precio"] * pizza["QTY"]
            medida = pizza["size"]
            costSum = 0
            for pizzaTopping in pizzaToppings:
                dataToppings = {
                    "id": pizzaTopping["toppings_id"]
                }
                toppings = Topping.get_toppings_by_id(dataToppings)
                for topping in toppings:
                    cost = topping['price']
                    costSum += cost
                    totalCostSize = getPriceSize(medida)
                    totalCostCrust = getPriceCrust(pizza["crust"])
                    totalCostUsd = (costSum + totalCostSize + totalCostCrust) * pizza["QTY"]
                    totalCost = 0
                    totalCost += totalCostUsd
                    roundTotalCost = round(totalCost)
                data1['costoTotal'] = int(roundTotalCost)
                data1['ganacia'] = data1['precio'] - data1['costoTotal']
        data.append(data1)
    return render_template('orders_admin.html', all_orders = data )

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
        dataTopping["cost"] = dataTopping["price"]
        dataTopping['medida'] = (dataTopping['medida'])
    
    if user[0]["admin"] != 1:
        return render_template('home.html')
    else:
        return render_template('toppings.html', dataToppings = dataToppings, usd = usd)

@app.route("/create_topping", methods=["POST"])
def create_topping():
    Topping.save(request.form)
    price = get_price(request.form['url'])
    dataTopping = Topping.get_all()[0]
    data = {
            "id": dataTopping["id"],
            "price": price / usd
        }
    Topping.updateCost(data)
    if request.form.get('toppings') != None:
        flash("your topping has been created successfully!")
        return redirect('/toppings')

@app.route("/update/prices")
def updateCost():
    dataToppings = Topping.get_all()
    for dataTopping in dataToppings:
        dataTopping["price"] = get_price(dataTopping["url"])
        data = {
            "id": dataTopping["id"],
            "price": dataTopping["price"] / usd
        }
        Topping.updateCost(data)
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
        "url": request.form['url'],
        "medida": request.form['medida'],
        "price": get_price(request.form['url']) / usd
    }
    Topping.update(data)
    return redirect("/toppings")
