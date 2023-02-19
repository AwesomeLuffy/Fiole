from src.Model.Utils.DBHandlerManager import DBHandlerManager
from src.Model.Utils.JWToken import JWToken


class LoginModel:
    TOKEN_HEADER = {
        "alg": "HS256",
        "typ": "JWT"
    }
    SECRET_KEY = "secret"

    def __init__(self):
        pass

    @staticmethod
    def check_login(username: str, password: str) -> tuple[bool, bool]:
        """Method to check if the login is valid
        :param username: username
        :param password: password
        :return: tuple[bool, bool] (is_username_valid, is_password_valid)
        """
        if DBHandlerManager.check_user_exists(username):
            if DBHandlerManager.check_user_encoded_password(username,
                                                            password):
                return True, True
            else:
                return True, False
        else:
            return False, False

    @staticmethod
    def check_login_token(token: str) -> tuple[bool, str]:
        """Method to check if the token is valid
        It will return the username in the token if it valid (Only work for login token)
        :param token: token
        :return: tuple[bool, str] (is_token_valid, username)
        """
        token = JWToken.token_from_string(token)
        if token.check_token_signature(LoginModel.SECRET_KEY):
            if not token.is_expired():
                return True, token.read_payload()["username"]
        return False, ""

    @staticmethod
    def get_login_token(username: str, validity: int) -> str:
        """Method to get a token
        :param username: username
        :param validity: validity of the token
        :return: str
        """
        token = JWToken.generate_jw_token(header=LoginModel.TOKEN_HEADER,
                                          payload={"username": username},
                                          secret=LoginModel.SECRET_KEY,
                                          validity=validity
                                          )
        return str(token)
