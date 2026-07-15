from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from Services.AccountService import AccountService


account_controller = Blueprint("account_controller", __name__)

service = AccountService()


@account_controller.route("/accounts", methods=["GET"])
@jwt_required()
def get_user_accounts():
    try:
        user_id = get_jwt_identity()

        accounts = service.get_accounts_by_user(user_id)

        results = []

        for account in accounts:
            results.append({
                "account_id": account.account_id,
                "balance": float(account.balance),
                "account_type": account.account_type,
                "created_at": account.created_at
            })

        return jsonify(results), 200

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@account_controller.route("/accounts/<string:account_id>", methods=["GET"])
@jwt_required()
def get_account(account_id):
    try:
        user_id = get_jwt_identity()

        account = service.get_account_for_user(
            account_id,
            user_id
        )

        return jsonify({
            "account_id": account.account_id,
            "balance": float(account.balance),
            "account_type": account.account_type,
            "created_at": account.created_at
        }), 200

    except PermissionError as error:
        return jsonify({"error": str(error)}), 403

    except ValueError as error:
        return jsonify({"error": str(error)}), 404

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@account_controller.route("/accounts", methods=["POST"])
@jwt_required()
def create_account():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        service.create_account(
            user_id,
            data["account_type"]
        )

        return jsonify({
            "message": "Account created successfully."
        }), 201

    except KeyError as error:
        return jsonify({
            "error": f"Missing required field: {error.args[0]}"
        }), 400

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@account_controller.route(
    "/accounts/<string:account_id>/deposit",
    methods=["POST"]
)
@jwt_required()
def deposit(account_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        balance = service.deposit(
            account_id,
            data["amount"],
            user_id
        )

        return jsonify({
            "message": "Deposit successful.",
            "new_balance": float(balance)
        }), 200

    except KeyError as error:
        return jsonify({
            "error": f"Missing required field: {error.args[0]}"
        }), 400

    except PermissionError as error:
        return jsonify({"error": str(error)}), 403

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@account_controller.route(
    "/accounts/<string:account_id>/withdraw",
    methods=["POST"]
)
@jwt_required()
def withdraw(account_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        balance = service.withdraw(
            account_id,
            data["amount"],
            user_id
        )

        return jsonify({
            "message": "Withdrawal successful.",
            "new_balance": float(balance)
        }), 200

    except KeyError as error:
        return jsonify({
            "error": f"Missing required field: {error.args[0]}"
        }), 400

    except PermissionError as error:
        return jsonify({"error": str(error)}), 403

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@account_controller.route(
    "/accounts/<string:account_id>/transactions",
    methods=["GET"]
)
@jwt_required()
def get_transactions(account_id):
    try:
        user_id = get_jwt_identity()

        transactions = service.get_transactions(
            account_id,
            user_id
        )

        results = []

        for transaction in transactions:
            results.append({
                "transaction_id": transaction.txn_id,
                "account_id": transaction.account_id,
                "transaction_type": transaction.txn_type,
                "amount": float(transaction.amount),
                "created_at": transaction.created_at
            })

        return jsonify(results), 200

    except PermissionError as error:
        return jsonify({"error": str(error)}), 403

    except ValueError as error:
        return jsonify({"error": str(error)}), 404

    except Exception as error:
        return jsonify({"error": str(error)}), 500