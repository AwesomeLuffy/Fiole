from src.Model.Utils.Utils import Utils
from flask import render_template as render, session, redirect, url_for, request
from src.Model.ViewsTemplates.StatViewModel import StatViewModel
from src.Model.StatModel import StatModel, Actions
from src.Controller.LoginController import LoginController


class StatController:
    SUBMIT_KEY = "submit"

    SUBMIT_ACTUALIZE = "refresh"
    SUBMIT_STOP = "stop_cam"
    SUBMIT_START = "start_cam"

    def __init__(self):
        pass

    @staticmethod
    def stats():
        """Method to render the stat page
        :return: render_template
        """
        svm_instance = StatViewModel(StatModel.get_access_count(), StatModel.get_number_of_unknown())
        if request.method == "POST":
            if not session.get(LoginController.SESSION_IS_CONNECTED):
                return redirect(url_for("LoginRouter.login"))
            if request.form[StatController.SUBMIT_KEY] == StatController.SUBMIT_ACTUALIZE:
                # Actualize face on raspberry (it's an equivalent to notifyDataChanged)
                svm_instance.define_server_response(StatModel.action_on_raspberry(Actions.ACTUALIZE_FACE))
            elif request.form[StatController.SUBMIT_KEY] == StatController.SUBMIT_STOP:
                # Stop the camera (just stop recording, it will not stop the program)
                svm_instance.define_server_response(StatModel.action_on_raspberry(Actions.STOP_CAMERA))
            elif request.form[StatController.SUBMIT_KEY] == StatController.SUBMIT_START:
                # Start the camera (just start recording)
                svm_instance.define_server_response(StatModel.action_on_raspberry(Actions.START_CAMERA))
        preformat_dict = Utils.get_preformat_render('stats.html', obj=svm_instance)
        return render(**preformat_dict)
