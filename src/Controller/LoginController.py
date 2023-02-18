from flask import request, redirect, url_for, render_template, session
from src.Model.Utils import Utils
from src.Model.ViewsTemplates.LoginViewModel import LoginViewModel
from src.Model.DBCommunicator import DBCommunicator
from src.Model.JWToken import JWToken


class LoginController:
    TOKEN_HEADER = {
        "alg": "HS256",
        "typ": "JWT"
    }
    SECRET_KEY = "secret"

    def __init__(self):
        pass

    @staticmethod
    def login():
        """Method to login
        It will check if the user exists and if the password is correct and redirect depending on the result
        :return: render_template
        """
        if request.method == "POST":
            if request.form['submit'] == "login":
                if DBCommunicator.check_user_exists(request.form['inputUsername']):
                    if DBCommunicator.check_user_encoded_password(request.form['inputUsername'],
                                                                  request.form['inputPassword']):
                        session['is_connected'] = True
                        session['username'] = request.form['inputUsername']

                        response = redirect(url_for('IndexRouter.home'))

                        if request.form.get('flexSwitchCheckRememberMe'):
                            PAYLOAD = {
                                "username": request.form['inputUsername'],
                            }
                            flask_token = JWToken.generate_jw_token(LoginController.TOKEN_HEADER, PAYLOAD,
                                                                    LoginController.SECRET_KEY)

                            response.set_cookie("flask_token", str(flask_token))

                        return response
                    else:
                        preformat = Utils.get_preformat_render("login.html",
                                                               obj=LoginViewModel(
                                                                   is_password_valid=False,
                                                                   is_username_valid=True,
                                                                   username_entered=request.form['inputUsername']
                                                               ))
                        return render_template(**preformat)
                else:
                    preformat = Utils.get_preformat_render("login.html",
                                                           obj=LoginViewModel(
                                                               is_password_valid=False,
                                                               is_username_valid=False,
                                                               username_entered=request.form['inputUsername']
                                                           ))
                    return render_template(**preformat)
            else:
                preformat = Utils.get_preformat_render("login.html")
                return render_template(**preformat)
        else:
            if session.get("is_connected"):
                return redirect(url_for('IndexRouter.home'))

            if request.cookies.get("flask_token"):
                flask_token = request.cookies.get("flask_token")
                token = JWToken.token_from_string(flask_token)
                if token.check_token_signature(LoginController.SECRET_KEY):
                    if not token.is_expired():
                        session['is_connected'] = True
                        session['username'] = "admin"
                        return redirect(url_for('IndexRouter.home'))
            preformat = Utils.get_preformat_render("login.html")
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
        if session.get("is_connected"):
            session.pop('is_connected')
            session.pop('username')
        if request.cookies.get("flask_token"):
            response.set_cookie("flask_token", "", expires=0)
        return response
