from flask import render_template
from src.Model.Utils import Utils, FieldsType
from flask import request
from src.Model.DataFace import DataFace

from werkzeug.datastructures import ImmutableMultiDict

from src.Model.ViewsTemplates.AddPeopleViewModel import AddPeopleViewModel
from src.Model.FacesDB import FacesDB


class AddPeopleController:

    def __init__(self):
        pass

    @staticmethod
    def add():
        if request.method == 'POST':
            # Get the data from the form and split it into array by the number at the end of the field
            # For example: inputData0, inputName0, inputFile0 will be split into 1 array
            # And inputData1, inputName1, inputFile1 will be split into another array

            # To be sure to execute the "if" that import the data, we add a field with a space as key, it will not be
            # handled by the for loop but this allows to be sure to execute the last line field from the form
            # So, I convert the ImmutableMultiDict to a normal dict, add the space field and convert it back
            # to ImmutableMultiDict
            copy = request.form.copy()
            copy.add(' ', ' ')
            data = ImmutableMultiDict(copy).items()

            return_error_string = []
            actual_form = 0
            data_faces = []
            success_added_count = 0

            separated_form = {}

            for key, value in data:

                # If the number at the end changed or if a field not valid we check the another
                # line of fields
                if not key.endswith(str(actual_form)):
                    if Utils.verify_field(request.files[f"formFile{actual_form}"].filename,
                                          FieldsType.FILE) and return_error_string == []:
                        file = request.files[f"formFile{actual_form}"]
                        file.filename = f"{separated_form['da']}.{file.filename.split('.')[-1]}"

                        path = f"src/static/img/{file.filename}"
                        file.save(path)
                        separated_form["img_path"] = path

                        if "have_access" not in separated_form:
                            separated_form["have_access"] = False

                        data_face = DataFace(**separated_form)
                        is_success, error = data_face.build_face_encoded()

                        if is_success:
                            data_faces.append(data_face)
                            success_added_count += 1
                        else:
                            print(error)
                            return_error_string.append(f"Line ({actual_form}) for DA {separated_form['da']} : {error}")
                    actual_form += 1
                    separated_form = {}

                # Due to separated_from passed by reference we need to force the call of "check_for_error" so we can't
                # use the "or" operator
                Utils.check_for_error(key, value, separated_form, return_error_string, actual_form)

                if key.startswith("flexSwitchCheckAccess"):
                    separated_form["have_access"] = True

            if len(data_faces) > 0:
                FacesDB.insert_faces_db(data_faces)

            preformat = Utils.get_custom_preformat_render('add_people.html',
                                                          obj=AddPeopleViewModel(success_added_count,
                                                                                 return_error_string),
                                                          script='add_input_fields.js')
        else:
            preformat = Utils.get_custom_preformat_render('add_people.html', obj=None, script='add_input_fields.js')
        return render_template(**preformat)
