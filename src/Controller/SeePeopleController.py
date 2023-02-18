from flask import render_template, request, redirect, url_for, session
from src.Model.Utils import Utils
from src.Model.ViewsTemplates.SeePeopleViewModel import SeePeopleViewModel
from src.Model.ViewsTemplates.SeeUnknownViewModel import SeeUnknownViewModel
from src.Model.DBCommunicator import DBCommunicator
from src.Model.DataFace import DataFace


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

    def __init__(self):
        pass

    @staticmethod
    def unknown():
        """Method to see unknown people in the database
        :return: render_template
        """
        if not session.get("is_connected"):
            return redirect(url_for("LoginRouter.login"))
        if request.method == "POST":
            count_affected = 0
            if request.form[SeePeopleController.SUBMIT_KEY] == "delete":
                count_affected = DBCommunicator.delete_specific_unknown(
                    request.form[SeePeopleController.UNKNOWN_NAME_KEY])
            elif request.form[SeePeopleController.SUBMIT_KEY] == "delete_all":
                count_affected = DBCommunicator.delete_unknown()

            preformat = Utils.get_preformat_render("unknown.html",
                                                   obj=SeeUnknownViewModel(unknown_list=DBCommunicator.get_unknown(),
                                                                           postback=True,
                                                                           count_affected=count_affected
                                                                           ))
        else:
            dataface_list = DBCommunicator.get_unknown()
            preformat = Utils.get_preformat_render("unknown.html", obj=SeeUnknownViewModel(dataface_list))
        return render_template(**preformat)

    @staticmethod
    def registered():
        """Method to see registered people in the database
        :return: render_template
        """
        if not session.get("is_connected"):
            return redirect(url_for("LoginRouter.login"))
        if request.method == "POST":
            if request.form[SeePeopleController.SUBMIT_KEY] == "Modifier":
                return_error_string = []
                separated_form = {DataFace.DA_PARAMETER_DF: request.form[SeePeopleController.DA_KEY],

                                  DataFace.NAME_PARAMETER_DF: request.form[SeePeopleController.NAME_KEY],

                                  DataFace.SURNAME_PARAMETER_DF: request.form[SeePeopleController.SURNAME_KEY],

                                  DataFace.HAVE_ACCESS_PARAMETER_DF:
                                      True if SeePeopleController.SWITCH_KEY in request.form else False,

                                  DataFace.IMG_PATH_PARAMETER_DF: None

                                  }

                for key, value in separated_form.items():
                    if Utils.check_for_error(key, value, separated_form, return_error_string, 0):
                        break

                if not return_error_string:
                    data_face = DataFace(**separated_form)

                    DBCommunicator.update_face_db(data_face)

                preformat = Utils.get_preformat_render("registered.html",
                                                       obj=SeePeopleViewModel(
                                                           dataface_list=DBCommunicator.get_all_faces_db(),
                                                           list_error=return_error_string,
                                                           postback=True
                                                           ))
            elif request.form[SeePeopleController.SUBMIT_KEY] == "Supprimer":
                DBCommunicator.delete_face_db(int(request.form[SeePeopleController.DA_KEY]))
                preformat = Utils.get_preformat_render("registered.html",
                                                       obj=SeePeopleViewModel(
                                                           dataface_list=DBCommunicator.get_all_faces_db(),
                                                           postback=True
                                                           ))
            else:
                preformat = Utils.get_preformat_render("registered.html",
                                                       obj=SeePeopleViewModel(
                                                           dataface_list=DBCommunicator.get_all_faces_db()))
        else:
            preformat = Utils.get_preformat_render("registered.html",
                                                   obj=SeePeopleViewModel(
                                                       dataface_list=DBCommunicator.get_all_faces_db()))
        return render_template(**preformat)
