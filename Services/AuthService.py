from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from Models.User import User
from Repositories.UserRepository import UserRepository
from Services.AccountService import AccountService


class AuthService:

    def __init__(self, user_repository=None, account_service=None):
        self.user_repository = user_repository or UserRepository()
        self.account_service = account_service or AccountService()

    def register(self, name, email, password, account_type):
        # Validate name
        if name is None or name.strip() == "":
            raise ValueError("Name is required.")

        # Validate email
        if email is None or email.strip() == "":
            raise ValueError("Email is required.")

        normalized_email = email.strip().lower()

        # Prevent duplicate users
        existing_user = self.user_repository.find_by_email(
            normalized_email
        )

        if existing_user is not None:
            raise ValueError("A user with this email already exists.")

        # Validate password
        if password is None or password.strip() == "":
            raise ValueError("Password is required.")

        if len(password) < 8:
            raise ValueError(
                "Password must contain at least 8 characters."
            )

        # Validate account type
        if account_type is None or account_type.strip() == "":
            raise ValueError("Account type is required.")

        normalized_account_type = account_type.strip().title()

        if normalized_account_type not in ["Checking", "Savings"]:
            raise ValueError(
                "Account type must be Checking or Savings."
            )

        # Hash the password before saving it
        password_hash = generate_password_hash(password)

        user = User(
            user_id=None,
            name=name.strip(),
            email=normalized_email,
            password_hash=password_hash,
            created_at=None
        )

        # Create the user and receive the new MongoDB ID
        user_id = self.user_repository.create_user(user)

        if user_id is None:
            raise Exception("User could not be created.")

        # Automatically create the user's first bank account
        try:
            self.account_service.create_account(
                user_id,
                normalized_account_type
            )

        except Exception as error:
            raise Exception(
                f"User was created, but the account could not be created: "
                f"{error}"
            )

        return user_id
    
    def login(self, email, password):
        if email is None or email.strip() == "":
            raise ValueError("Email is required.")

        if password is None or password.strip() == "":
            raise ValueError("Password is required.")

        normalized_email = email.strip().lower()

        user = self.user_repository.find_by_email(normalized_email)

        if user is None:
            raise ValueError("Invalid email or password.")

        if not check_password_hash(user.password_hash, password):
            raise ValueError("Invalid email or password.")

        return user