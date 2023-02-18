from flask import Flask, session, send_from_directory, redirect, url_for
import app_config

'''
    To add a controller:
        1. Create a new file in src\Controller (like TextController.py)
        2. Create a new class in the file (like TextController)
        3. Create a new function in the class (like test)
        4. Add the function to the router (like TestRouter.route('/test', methods=['GET'])(TextController.test))
        5. Edit the app.py and add the router to the app (like app.register_blueprint(TestRouter, url_prefix="/"))
'''

app = Flask(__name__, template_folder=app_config.VIEWS_DIR, static_folder='src/static')

app.config.from_object(app_config)

app.secret_key = app_config.SECRET_KEY

# Import the routers later to avoid circular import
from src.Routes.Router import IndexRouter, AddPeopleRouter, SeePeopleRouter, LoginRouter

app.register_blueprint(IndexRouter, url_prefix="/")
app.register_blueprint(AddPeopleRouter, url_prefix="/")
app.register_blueprint(SeePeopleRouter, url_prefix="/")
app.register_blueprint(LoginRouter, url_prefix="/")


@app.route('/static/img/<path:path>')
def send_img(path):
    """
    Secure the img/X path, only connected user can access this directory
    :param path:
    :return:
    """
    if session.get("is_connected"):
        return send_from_directory('src/static/img', path)
    else:
        return redirect(url_for("LoginRouter.login"))


if __name__ == '__main__':
    app.run()
