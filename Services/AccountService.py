from decimal import Decimal

from Models.Account import Account
from Models.Transaction import Transaction
from Repositories.AccountRepository import AccountRepository
from Repositories.UserRepository import UserRepository
from Repositories.TransactionRepository import TransactionRepository


class AccountService:
    """Service layer for account operations using MongoDB repositories."""

    def __init__(
        self,
        account_repository=None,
        user_repository=None,
        transaction_repository=None
    ):
        self.account_repository = (
            account_repository
            if account_repository is not None
            else AccountRepository()
        )

        self.user_repository = (
            user_repository
            if user_repository is not None
            else UserRepository()
        )

        self.transaction_repository = (
            transaction_repository
            if transaction_repository is not None
            else TransactionRepository()
        )

    def create_account(self, user_id, account_type):
        user = self.user_repository.find_by_id(user_id)

        if user is None:
            raise ValueError("User does not exist.")

        if account_type is None or account_type.strip() == "":
            raise ValueError("Account type is required.")

        normalized_account_type = account_type.strip().title()

        if normalized_account_type not in ["Checking", "Savings"]:
            raise ValueError(
                "Account type must be Checking or Savings."
            )

        existing_account = (
            self.account_repository.find_by_user_and_type(
                user_id,
                normalized_account_type
            )
        )

        if existing_account is not None:
            raise ValueError(
                f"You already have a {normalized_account_type} account."
            )

        account = Account(
            account_id=None,
            user_id=user_id,
            balance=Decimal("0.00"),
            account_type=normalized_account_type,
            created_at=None
        )

        created = self.account_repository.create_account(account)

        if not created:
            raise Exception("Account could not be created.")

        return True

    def get_account(self, account_id):
        account = self.account_repository.find_by_id(account_id)

        if account is None:
            raise ValueError("Account not found.")

        return account

    def get_account_for_user(self, account_id, user_id):
        account = self.get_account(account_id)

        if account.user_id != user_id:
            raise PermissionError(
                "You do not have access to this account."
            )

        return account

    def get_accounts_by_user(self, user_id):
        user = self.user_repository.find_by_id(user_id)

        if user is None:
            raise ValueError("User does not exist.")

        return self.account_repository.find_by_user_id(user_id)

    def deposit(self, account_id, amount, user_id):
        account = self.get_account_for_user(account_id, user_id)

        try:
            amount = Decimal(str(amount))
        except Exception:
            raise ValueError("Deposit amount must be a valid number.")

        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        new_balance = account.balance + amount

        updated = self.account_repository.update_balance(
            account_id,
            new_balance
        )

        if not updated:
            raise Exception("Deposit could not be completed.")

        transaction = Transaction(
            txn_id=None,
            account_id=account_id,
            txn_type="Deposit",
            amount=amount,
            created_at=None
        )

        transaction_created = (
            self.transaction_repository.create_transaction(transaction)
        )

        if not transaction_created:
            raise Exception("Transaction record could not be created.")

        return new_balance

    def withdraw(self, account_id, amount, user_id):
        account = self.get_account_for_user(account_id, user_id)

        try:
            amount = Decimal(str(amount))
        except Exception:
            raise ValueError("Withdrawal amount must be a valid number.")

        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")

        if amount > account.balance:
            raise ValueError("Insufficient funds.")

        new_balance = account.balance - amount

        updated = self.account_repository.update_balance(
            account_id,
            new_balance
        )

        if not updated:
            raise Exception("Withdrawal could not be completed.")

        transaction = Transaction(
            txn_id=None,
            account_id=account_id,
            txn_type="Withdraw",
            amount=amount,
            created_at=None
        )

        transaction_created = (
            self.transaction_repository.create_transaction(transaction)
        )

        if not transaction_created:
            raise Exception("Transaction record could not be created.")

        return new_balance

    def get_transactions(self, account_id, user_id):
        self.get_account_for_user(account_id, user_id)

        return self.transaction_repository.find_by_account_id(
            account_id
        )