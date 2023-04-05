from app import app
from app.controllers import users,orders, admins
import os
import stripe


# stripe_keys = {
#     "secret_key": os.environ["STRIPE_SECRET_KEY"],
#     "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
# }

stripe.api_key = stripe_keys["secret_key"]

# @app.route("/config")
# def get_publishable_key():
#     stripe_config = {"publicKey": stripe_keys["publishable_key"]}
#     return jsonify(stripe_config)

if __name__=="__main__":
    app.run(debug=True)