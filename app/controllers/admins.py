from app import app
from flask import render_template, redirect, request, session, flash
from app.models.topping import Topping

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/toppings")
def toppings():
    return render_template('toppings.html')

@app.route("/create_topping", methods=["POST"])
def create_topping():
    Topping.save(request.form)
    return redirect("/toppings")

