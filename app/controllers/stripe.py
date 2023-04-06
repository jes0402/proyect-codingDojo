from app import app
import os
from flask import Flask, render_template, request
import stripe
from app.models.order import Order

stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']


@app.route('/test')
def test():
    return render_template('pruebastripe.html', )


@app.route('/charge', methods=['POST', 'GET'])
def charge():
    amount = request.form["totalPrice"]
    dataOrderID = {"order_id": request.form["order_id"]}

    # customer = stripe.Customer.create(
    #     email='customer@example.com',
    #     source=request.form['stripeToken']
    # )

    # charge = stripe.Charge.create(
    #     customer=customer.id,
    #     amount=amount,
    #     currency='usd',
    #     description='Flask Charge'
    # )

    orders = Order.get_info_for_dashboard(dataOrderID)
    estado = ""
    if orders[0]['completo'] == 1:
        estado = "completo"
    elif orders[0]["pendiente"] == 1:
        estado = "pendiente"
    elif orders[0]["cancelado"] == 1:
        estado = "cancelado"
    return render_template('charge.html', amount=amount, orders = orders, estado = estado)
