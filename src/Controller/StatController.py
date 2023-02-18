from src.Model.Utils.Utils import Utils
from flask import render_template as render
from src.Model.ViewsTemplates.StatViewModel import StatViewModel
from src.Model.StatModel import StatModel


class StatController:

    def __init__(self):
        pass

    @staticmethod
    def stats():
        """Method to render the stat page
        :return: render_template
        """

        preformat_dict = Utils.get_preformat_render('stats.html', obj=StatViewModel(
            StatModel.get_access_count(),
            StatModel.get_number_of_unknown()
        ))
        return render(**preformat_dict)
