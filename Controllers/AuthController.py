from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from Services.AuthService import AuthService


auth_controller = Blueprint("auth_controller", __name__)

service = AuthService()


@auth_controller.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()

        user_id = service.register(
            data["name"],
            data["email"],
            data["password"],
            data["account_type"]
        )

        return jsonify({
            "message": "Registration successful.",
            "user_id": user_id
        }), 201

    except KeyError as error:
        return jsonify({
            "error": f"Missing required field: {error.args[0]}"
        }), 400

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500
    
@auth_controller.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        user = service.login(
            data["email"],
            data["password"]
        )

        access_token = create_access_token(
            identity=user.user_id
        )

        return jsonify({
            "message": "Login successful.",
            "access_token": access_token,
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email
            }
        }), 200

    except KeyError as error:
        return jsonify({
            "error": f"Missing required field: {error.args[0]}"
        }), 400

    except ValueError as error:
        return jsonify({"error": str(error)}), 401

    except Exception as error:
        return jsonify({"error": str(error)}), 500