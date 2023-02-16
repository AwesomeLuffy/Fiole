from flask import Blueprint
from src.Controller.HomeController import HomeController
from src.Controller.AddPeopleController import AddPeopleController
from src.Controller.SeePeopleController import SeePeopleController

# The parameter in route will define the url like if /mywebsite is set, the url will be like localhost:XXXX/mywebsite

# Create a router for the index page
IndexRouter = Blueprint('IndexRouter', __name__)
IndexRouter.route('/', methods=['GET'])(HomeController.home)

# Create a router for the add page
AddPeopleRouter = Blueprint('AddRouter', __name__)
AddPeopleRouter.route('/add', methods=['GET', 'POST'])(AddPeopleController.add)

# Create a router for the unknows page
SeePeopleRouter = Blueprint('SeeRouter', __name__)
SeePeopleRouter.route('/unknowns', methods=['GET', 'POST'])(SeePeopleController.unknows)