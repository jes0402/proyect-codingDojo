from app import app
from flask import render_template, redirect, request, session, flash
from app.models.topping import Topping
from app.models.user import Users
from app.models.order import Order

import time 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager

# start by defining the options 
options = webdriver.ChromeOptions() 
# we don't need it as the page also populated with the running javascript code. 
options.page_load_strategy = 'none' 
# this returns the path web driver downloaded 
chrome_path = ChromeDriverManager().install() 
chrome_service = Service(chrome_path) 
# pass the defined options and service objects to initialize the web driver 
driver = Chrome(options=options, service=chrome_service) 
driver.implicitly_wait(5)


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
    for order in orders:
        print(order['url'])
    #     order['cost'] = driver.get(order['url'])
    #     time.sleep(5)
    #     price = driver.find_element(By.CSS_SELECTOR, "div[class*='price-per-um__pdp']")
    # if price:
    #     price = price.text
    #     price = ''.join(filter(str.isdigit, price))
    #     price = int(price)
    # else:
    #     price = "not found"
    # driver.quit()
    # print(order['cost'])
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
    if user[0]["admin"] != 1:
        return render_template('home.html')
    else:
        return render_template('toppings.html')

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
