from flask import Blueprint, request, jsonify

from Services.AccountService import AccountService


account_controller = Blueprint("account_controller", __name__)

service = AccountService()


@account_controller.route("/accounts/<string:account_id>", methods=["GET"])
def get_account(account_id):
    try:
        account = service.get_account(account_id)

        return jsonify({
            "account_id": account.account_id,
            "user_id": account.user_id,
            "balance": float(account.balance),
            "account_type": account.account_type,
            "created_at": account.created_at
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 404


@account_controller.route("/accounts", methods=["POST"])
def create_account():
    try:
        data = request.get_json()

        service.create_account(
            data["user_id"],
            data["account_type"]
        )

        return jsonify({
            "message": "Account created successfully."
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@account_controller.route(
    "/accounts/<string:account_id>/deposit",
    methods=["POST"]
)
def deposit(account_id):
    try:
        data = request.get_json()

        balance = service.deposit(
            account_id,
            data["amount"]
        )

        return jsonify({
            "message": "Deposit successful.",
            "new_balance": float(balance)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@account_controller.route(
    "/accounts/<string:account_id>/withdraw",
    methods=["POST"]
)
def withdraw(account_id):
    try:
        data = request.get_json()

        balance = service.withdraw(
            account_id,
            data["amount"]
        )

        return jsonify({
            "message": "Withdrawal successful.",
            "new_balance": float(balance)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@account_controller.route(
    "/accounts/<string:account_id>/transactions",
    methods=["GET"]
)
def get_transactions(account_id):
    try:
        transactions = service.get_transactions(account_id)

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

    except Exception as e:
        return jsonify({"error": str(e)}), 400