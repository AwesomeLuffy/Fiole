from flask import Flask
import config

from src.Routes.Router import IndexRouter, AddPeopleRouter

'''
    To add a controller:
        1. Create a new file in src\Controller (like TextController.py)
        2. Create a new class in the file (like TextController)
        3. Create a new function in the class (like test)
        4. Add the function to the router (like TestRouter.route('/test', methods=['GET'])(TextController.test))
        5. Edit the app.py and add the router to the app (like app.register_blueprint(TestRouter, url_prefix="/"))
'''

app = Flask(__name__, template_folder=config.VIEWS_DIR, static_folder='src/static')

app.register_blueprint(IndexRouter, url_prefix="/")
app.register_blueprint(AddPeopleRouter, url_prefix="/")

app.config.from_object(config)

app.config["MYSQL_HOST"] = ""
app.config["MYSQL_USER"] = "user"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "database"

if __name__ == '__main__':
    app.run()
