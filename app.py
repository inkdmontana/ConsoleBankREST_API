from flask import Flask

from Controllers.AccountController import account_controller

app = Flask(__name__)

app.register_blueprint(account_controller)

if __name__ == "__main__":
    app.run(debug=True)
