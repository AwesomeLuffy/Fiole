from flask import render_template, request
from src.Model.Utils import Utils
from src.Model.ViewsTemplates.SeePeopleViewModel import SeePeopleViewModel
from src.Model.FacesDB import FacesDB
from src.Model.DataFace import DataFace


class SeePeopleController:
    # Form KEY
    DA_KEY = "inputDA"
    NAME_KEY = "inputName"
    SURNAME_KEY = "inputFName"
    SWITCH_KEY = "flexSwitchCheckAccess"
    SUBMIT_KEY = "submit"

    def __init__(self):
        pass

    @staticmethod
    def unknows():
        preformat = Utils.get_preformat_render("unknows.html", obj=None)
        return render_template(**preformat)

    @staticmethod
    def registered():
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

                    FacesDB.update_face_db(data_face)

                preformat = Utils.get_preformat_render("registered.html",
                                                       obj=SeePeopleViewModel(dataface_list=FacesDB.get_all_faces_db(),
                                                                              list_error=return_error_string,
                                                                              postback=True
                                                                              ))
            elif request.form[SeePeopleController.SUBMIT_KEY] == "Supprimer":
                FacesDB.delete_face_db(int(request.form[SeePeopleController.DA_KEY]))
                preformat = Utils.get_preformat_render("registered.html",
                                                       obj=SeePeopleViewModel(dataface_list=FacesDB.get_all_faces_db(),
                                                                              postback=True
                                                                              ))
            else:
                preformat = Utils.get_preformat_render("registered.html",
                                                       obj=SeePeopleViewModel(dataface_list=FacesDB.get_all_faces_db()))
        else:
            preformat = Utils.get_preformat_render("registered.html",
                                                   obj=SeePeopleViewModel(dataface_list=FacesDB.get_all_faces_db()))
        return render_template(**preformat)
