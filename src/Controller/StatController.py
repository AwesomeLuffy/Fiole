from src.Model.Utils.Utils import Utils
from flask import render_template as render, session, redirect, url_for, request
from src.Model.ViewsTemplates.StatViewModel import StatViewModel
from src.Model.StatModel import StatModel
from src.Controller.LoginController import LoginController


class StatController:

    def __init__(self):
        pass

    @staticmethod
    def stats():
        """Method to render the stat page
        :return: render_template
        """

        if request.method == "POST":
            if not session.get(LoginController.SESSION_IS_CONNECTED):
                return redirect(url_for("LoginRouter.login"))
            StatModel.actualize_face_on_raspberry()

        preformat_dict = Utils.get_preformat_render('stats.html', obj=StatViewModel(
            StatModel.get_access_count(),
            StatModel.get_number_of_unknown()
        ))
        return render(**preformat_dict)
