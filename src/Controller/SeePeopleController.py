from flask import render_template, request, redirect, url_for, session
from src.Model.Utils.Utils import Utils
from src.Model.ViewsTemplates.SeePeopleViewModel import SeePeopleViewModel
from src.Model.ViewsTemplates.SeeUnknownViewModel import SeeUnknownViewModel
from src.Model.Utils.DBHandlerManager import DBHandlerManager
from src.Model.Utils.DataFace import DataFace
from src.Model.SeePeopleModel import SeePeopleModel
from src.Controller.LoginController import LoginController


class SeePeopleController:
    """Controller to see people in the database
    """
    # Form KEY
    DA_KEY = "inputDA"
    NAME_KEY = "inputName"
    SURNAME_KEY = "inputFName"
    SWITCH_KEY = "flexSwitchCheckAccess"
    SUBMIT_KEY = "submit"

    UNKNOWN_NAME_KEY = "hiddenName"

    SUBMIT_ACTION_DELETE = "delete"
    SUBMIT_ACTION_DELETE_ALL = "delete_all"
    SUBMIT_ACTION_MODIFY = "modify"

    def __init__(self):
        pass

    @staticmethod
    def unknown():
        """Method to see unknown people in the database
        :return: render_template
        """
        if not session.get(LoginController.SESSION_IS_CONNECTED):
            return redirect(url_for("LoginRouter.login"))

        # Create the instance of the ViewModel
        suvm_instance = SeeUnknownViewModel(unknown_list=SeePeopleModel.get_unknowns())

        if request.method == "POST":
            count_affected = 0
            if request.form[SeePeopleController.SUBMIT_KEY] == SeePeopleController.SUBMIT_ACTION_DELETE:
                count_affected = SeePeopleModel.delete_specific_unknown(
                    request.form[SeePeopleController.UNKNOWN_NAME_KEY])

            elif request.form[SeePeopleController.SUBMIT_KEY] == SeePeopleController.SUBMIT_ACTION_DELETE_ALL:
                count_affected = SeePeopleModel.delete_unknown()

            suvm_instance.postback = True
            suvm_instance.count_affected = count_affected

        preformat = Utils.get_preformat_render("unknown.html",
                                               obj=suvm_instance)
        return render_template(**preformat)

    @staticmethod
    def registered():
        """Method to see registered people in the database
        :return: render_template
        """
        if not session.get("is_connected"):
            return redirect(url_for("LoginRouter.login"))



        # Create the instance of the ViewModel
        spvm_instance = SeePeopleViewModel(dataface_list=DBHandlerManager.get_all_faces_db())

        if request.method == "POST":
            if request.form[SeePeopleController.SUBMIT_KEY] == SeePeopleController.SUBMIT_ACTION_MODIFY:
                # Separate the form into a dict
                separated_form = {DataFace.DA_PARAMETER_DF: request.form[SeePeopleController.DA_KEY],

                                  DataFace.NAME_PARAMETER_DF: request.form[SeePeopleController.NAME_KEY],

                                  DataFace.SURNAME_PARAMETER_DF: request.form[SeePeopleController.SURNAME_KEY],

                                  DataFace.HAVE_ACCESS_PARAMETER_DF:
                                      True if SeePeopleController.SWITCH_KEY in request.form else False,

                                  DataFace.IMG_PATH_PARAMETER_DF: None

                                  }

                # Modify the person in the database and get the error list ([] if no error)
                return_error_string = SeePeopleModel.modify_people(separated_form)

                # Assign to the instance the error list and the postback
                spvm_instance.data_list = DBHandlerManager.get_all_faces_db()
                spvm_instance.error_list = return_error_string
                spvm_instance.postback = True

            elif request.form[SeePeopleController.SUBMIT_KEY] == SeePeopleController.SUBMIT_ACTION_DELETE:
                DBHandlerManager.delete_face_db(int(request.form[SeePeopleController.DA_KEY]))
                # Assign to the instance the postback to display the card with the message
                spvm_instance.data_list = DBHandlerManager.get_all_faces_db()
                spvm_instance.postback = True

        preformat = Utils.get_preformat_render("registered.html",
                                               obj=spvm_instance)
        return render_template(**preformat)
