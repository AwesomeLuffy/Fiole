class LoginViewModel:
    def __init__(self, is_password_valid: bool, is_username_valid: bool, username_entered: str):
        self.is_password_valid = is_password_valid
        self.is_username_valid = is_username_valid
        self.username_entered = username_entered

