from app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
from app.models.user import Users
from app.models.topping import Topping
from app.models.order import Order

bcrypt = Bcrypt(app)

@app.route("/")
def home():
    return render_template('register.html')

@app.route("/register", methods=["POST"])
def register():
    is_valid = Users.validate_user(request.form)
    if not is_valid:
        return redirect("/")
    new_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "address": request.form["address"],
        "city": request.form["city"],
        "state": request.form["state"],
        "password": bcrypt.generate_password_hash(request.form["password"])
    }
    id = Users.save(new_user)
    if not id:
        flash("Email already taken.","register")
        return redirect('/')
    session['user_id'] = id
    return redirect('/login')

@app.route("/login")
def login_template():
    return render_template('login.html')

@app.route("/login",methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user = Users.get_by_email(data)
    print("hola", user)
    if not user:
        flash("Invalid Email/Password","login")
        return redirect("/login")
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect("/login")
    session['user_id'] = user.id
    data = {
    "id": session['user_id']
    }
    user_session = Users.get_one(data)
    print("hola", user_session)
    if user_session[0]["admin"] == 1:
        return redirect('/dashboard')
    else:
        return redirect('/home')

@app.route("/home")
def home_order():
    if 'user_id' not in session:
            return redirect("/login")
    return render_template('home.html', title = "Home")

@app.route("/account")
def account():
    if 'user_id' not in session:
        return redirect('/')
    data = {
    "id": session['user_id']
    }
    user = Users.get_one(data)
    return render_template('account_info.html', user = user)

@app.route("/account", methods=["POST"])
def account_info():
    user_id = session['user_id']
    if request.method == "POST":
        data = {
        'id': user_id,
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "address": request.form["address"],
        "city": request.form["city"],
        "state": request.form["state"],
        }
        Users.edit(data)
        return render_template('account_info.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')