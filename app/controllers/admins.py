from app import app
from flask import render_template, redirect, request, session, flash
from app.models.topping import Topping
from app.models.user import Users
from app.models.order import Order


@app.route("/dashboard")
def check_admin():
    user_id = session['user_id']
    if 'user_id' not in session:
            return redirect("/login")
    data = {
    "id": session['user_id']
    }
    user = Users.get_one(data)
    if user[0]["admin"] != 1:
        return render_template('home.html')
    else:
        return render_template('dashboard.html')

@app.route("/orders")
def orders_admin():
    orders = Order.get_all_orders()
    for order in orders:
        if order["completo"] == 1:
            order["estado"] = "completo"
        if order["pendiente"] == 1:
            order["estado"] = "pendiente"
        if order["cancelado"] == 1:
            order["estado"] = "cancelado"
    print("hola",orders )       
    return render_template('orders_admin.html', all_orders = orders )

@app.route("/toppings")
def toppings():
    return render_template('toppings.html')

@app.route("/create_topping", methods=["POST"])
def create_topping():
    Topping.save(request.form)
## Poner alerta de que se creó el topping
    return redirect("/toppings")

