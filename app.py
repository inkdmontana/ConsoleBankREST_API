import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from Controllers.AccountController import account_controller
from Controllers.AuthController import auth_controller


load_dotenv()

app = Flask(__name__)

CORS(
    app,
    origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

app.register_blueprint(account_controller)
app.register_blueprint(auth_controller)


if __name__ == "__main__":
    app.run(debug=True)