from flask import render_template
from src.Model.Utils import Utils
from src.Model.ViewsTemplates.SeePeopleViewModel import SeePeopleViewModel
from src.Model.FacesDB import FacesDB


class SeePeopleController:
    def __init__(self):
        pass

    @staticmethod
    def unknows():
        preformat = Utils.get_preformat_render("unknows.html", obj=SeePeopleViewModel(FacesDB.get_all_faces_db()))
        return render_template(**preformat)

    @staticmethod
    def registered():
        preformat = Utils.get_preformat_render("registered.html")
        return render_template(**preformat)
