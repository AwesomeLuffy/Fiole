from flask import request, redirect, url_for, render_template, session
from src.Model.Utils.Utils import Utils
from src.Model.ViewsTemplates.LoginViewModel import LoginViewModel
from src.Model.LoginModel import LoginModel


class LoginController:
    # In days
    TOKEN_VALIDITY = 3

    # Session name
    SESSION_USERNAME = "username"
    SESSION_IS_CONNECTED = "is_connected"

    # Cookies name
    TOKEN_COOKIE = "flask_token"

    # Inputs
    INPUT_USERNAME = "inputUsername"
    INPUT_PASSWORD = "inputPassword"
    INPUT_REMEMBER_ME = "flexSwitchCheckRememberMe"

    def __init__(self):
        pass

    @staticmethod
    def login():
        """Method to login
        It will check if the user exists and if the password is correct and redirect depending on the result
        :return: render_template
        """
        # Check if the user is already connected
        if session.get("is_connected"):
            return redirect(url_for('IndexRouter.home'))
        # Check if the user has a token and if it is valid connect the user
        elif request.cookies.get("flask_token"):
            is_token_valid, token_username = LoginModel.check_login_token(request.cookies.get("flask_token"))
            if is_token_valid:
                session['is_connected'] = True
                session['username'] = token_username
                return redirect(url_for('IndexRouter.home'))

        # ----------------------------
        # Create the instance of the ViewModel (Set as None by default in case of no ViewModel have to be passed)
        lvm_instance = None
        if request.method == "POST":
            if request.form['submit'] == "login":
                username = request.form[LoginController.INPUT_USERNAME]
                is_username_valid, is_password_valid = LoginModel.check_login(username,
                                                                              request.form[
                                                                                  LoginController.INPUT_PASSWORD])

                if is_username_valid and is_password_valid:
                    session[LoginController.SESSION_IS_CONNECTED] = True
                    session[LoginController.SESSION_USERNAME] = username

                    response = redirect(url_for('IndexRouter.home'))

                    if request.form.get(LoginController.TOKEN_COOKIE):
                        token = LoginModel.get_login_token(username, 3600)
                        response.set_cookie(LoginController.TOKEN_COOKIE, token)

                    return response

                # Make the ViewModel
                lvm_instance = LoginViewModel(is_username_valid=is_username_valid,
                                              is_password_valid=is_password_valid,
                                              username_entered=username)

        preformat = Utils.get_preformat_render("login.html", obj=lvm_instance)
        return render_template(**preformat)

    @staticmethod
    def logout():
        """Method to logout
        Simply remove the session and redirect to the login page
        Delete session values
        Delete token if exists
        :return: redirect
        """
        response = redirect(url_for('LoginRouter.login'))
        if session.get(LoginController.SESSION_IS_CONNECTED):
            session.pop(LoginController.SESSION_IS_CONNECTED)
            session.pop(LoginController.SESSION_USERNAME)

        if request.cookies.get(LoginController.TOKEN_COOKIE):
            response.set_cookie(LoginController.TOKEN_COOKIE, "", expires=0)
        return response
