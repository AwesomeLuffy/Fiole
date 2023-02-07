from flask import Blueprint
from src.Controller.HomeController import HomeController
from src.Controller.AddPeopleController import AddPeopleController

# The parameter in route will define the url like if /mywebsite is set, the url will be like localhost:XXXX/mywebsite

# Create a router for the index page
IndexRouter = Blueprint('IndexRouter', __name__)
IndexRouter.route('/', methods=['GET'])(HomeController.home)

# Create a router for the test page
AddPeopleRouter = Blueprint('AddRouter', __name__)
AddPeopleRouter.route('/add', methods=['GET', 'POST'])(AddPeopleController.add)
