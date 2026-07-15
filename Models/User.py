class User:

    def __init__(
        self,
        user_id,
        name,
        email,
        password_hash=None,
        created_at=None
    ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at

    def __str__(self):
        return (
            f"User ID: {self.user_id}, "
            f"Name: {self.name}, "
            f"Email: {self.email}"
        )