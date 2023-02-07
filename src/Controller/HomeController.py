from flask import render_template as render
from src.Model.Utils import Utils


class HomeController:

    def home(self=None):
        preformat_dict = Utils.get_preformat_render('index.html')
        return render(**preformat_dict)

    def test(self=None):
        preformat_dict = Utils.get_preformat_render('test.html')
        return render(**preformat_dict)
