from flask import Flask
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

# app.config["MYSQL_HOST"] = "localhost"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "test"
# app.config["MYSQL_DB"] = "data_faces"
app
from src.Routes.Router import IndexRouter, AddPeopleRouter, SeePeopleRouter

app.register_blueprint(IndexRouter, url_prefix="/")
app.register_blueprint(AddPeopleRouter, url_prefix="/")
app.register_blueprint(SeePeopleRouter, url_prefix="/")

if __name__ == '__main__':
    app.run()
