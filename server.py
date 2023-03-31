from app import app
from app.controllers import users,orders, admins




if __name__=="__main__":
    app.run(debug=True)