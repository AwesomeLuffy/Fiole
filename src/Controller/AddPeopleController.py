from flask import render_template, session, redirect, url_for
from src.Model.Utils import Utils
from flask import request


from werkzeug.datastructures import ImmutableMultiDict

from src.Model.ViewsTemplates.AddPeopleViewModel import AddPeopleViewModel
from src.Model.AddPeopleModel import AddPeopleModel


class AddPeopleController:

    def __init__(self):
        pass

    @staticmethod
    def add():
        """Method to add people
        This method is a bit tricky, I use this 'cause it would have to me take a lot of time to do it in the good way like trim values in first time and so on
        Not the best way to do it but it works
        :return: render_template
        """
        if not session.get("is_connected"):
            return redirect(url_for("LoginRouter.login"))
        if request.method == 'POST':
            # To be sure to execute the "if" that import the data, we add a field with a space as key, it will not be
            # handled by the for loop but this allows to be sure to execute the last line field from the form
            # So, I convert the ImmutableMultiDict to a normal dict, add the space field and convert it back
            # to ImmutableMultiDict
            copy = request.form.copy()
            copy.add(' ', ' ')
            data = ImmutableMultiDict(copy)

            # Function add_people from the model, return how many successfully added and the errors (if there is)
            success_added_count, return_error_string = AddPeopleModel.add_people(data, request.files)

            preformat = Utils.get_custom_preformat_render('add_people.html',
                                                          obj=AddPeopleViewModel(success_added_count,
                                                                                 return_error_string),
                                                          script='add_input_fields.js')
        else:
            preformat = Utils.get_custom_preformat_render('add_people.html', obj=None, script='add_input_fields.js')
        return render_template(**preformat)
