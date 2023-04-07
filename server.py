from app import app
from app.controllers import users,orders, admins, stripe    




if __name__=="__main__":
    app.run(debug=True)