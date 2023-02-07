from flask import render_template
from src.Model.Utils import Utils
from flask import request
from src.Model.ViewsTemplates.AddPeopleViewModel import AddPeopleViewModel


class AddPeopleController:

    def add(self=None):
        if request.method == 'POST':
            preformat = Utils.get_custom_preformat_render('add_people.html',
                                                          obj=None,
                                                          script='add_input_fields.js')
        else:
            preformat = Utils.get_custom_preformat_render('add_people.html', obj=None, script='add_input_fields.js')
        return render_template(**preformat)
