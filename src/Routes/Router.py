from flask import Blueprint
from src.Controller.HomeController import HomeController
from src.Controller.AddPeopleController import AddPeopleController
from src.Controller.SeePeopleController import SeePeopleController
from src.Controller.LoginController import LoginController

# The parameter in route will define the url like if /mywebsite is set, the url will be like localhost:XXXX/mywebsite

# Create a router for the index page
IndexRouter = Blueprint('IndexRouter', __name__)
IndexRouter.route('/', methods=['GET'])(HomeController.home)

# Create a router for the add page
AddPeopleRouter = Blueprint('AddRouter', __name__)
AddPeopleRouter.route('/add', methods=['GET', 'POST'])(AddPeopleController.add)

# Create a router for the unknows page
SeePeopleRouter = Blueprint('SeeRouter', __name__)
SeePeopleRouter.route('/unknowns', methods=['GET', 'POST'])(SeePeopleController.unknown)
SeePeopleRouter.route('/registered', methods=['GET', 'POST'])(SeePeopleController.registered)

# Create a router for the login page
LoginRouter = Blueprint('LoginRouter', __name__)
LoginRouter.route('/login', methods=['GET', 'POST'])(LoginController.login)
LoginRouter.route('/logout', methods=['GET'])(LoginController.logout)
