from flask import render_template as render
from src.Model.Utils import Utils


class HomeController:

    def __init__(self):
        pass

    @staticmethod
    def home():
        preformat_dict = Utils.get_preformat_render('index.html')
        return render(**preformat_dict)
