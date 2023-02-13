from flask import render_template
from src.Model.Utils import Utils, FieldsType
from flask import request
from src.Model.DataFace import DataFace

from src.Model.ViewsTemplates.AddPeopleViewModel import AddPeopleViewModel


class AddPeopleController:

    def add(self=None):
        if request.method == 'POST':
            # Get the data from the form and split it into array by the number at the end of the field
            # For example: inputData0, inputName0, inputFile0 will be split into 1 array
            # And inputData1, inputName1, inputFile1 will be split into another array

            data = request.form.items()
            return_error_string = []
            actual_form = 0
            data_faces = []
            field_counter = 0
            success_added_count = 0

            separated_form = {}

            for key, value in data:

                # If the number at the end changed or if a field not valid we check the another
                # line of fields
                if not key.endswith(str(actual_form)) or AddPeopleController.check_for_error(
                        key, value, separated_form, return_error_string, actual_form):
                    actual_form += 1

                field_counter += 1
                if field_counter == 3:
                    field_counter = 0

                    # In case of the field flexSwitch not here we set it to false
                    if key.startswith("flexSwitchCheckAccess"):
                        # The last value of a line is the checkbox, so we check if it's checked or not
                        separated_form["have_access"] = True if value == "on" else False
                    else:
                        separated_form["have_access"] = False
                    if Utils.verify_field(request.files[f"formFile{actual_form}"].filename, FieldsType.FILE):
                        file = request.files[f"formFile{actual_form}"]
                        file.filename = f"{separated_form['da']}.{file.filename.split('.')[-1]}"

                        file.save(f"src/static/img/{file.filename}")
                        separated_form["img"] = request.files[f"formFile{actual_form}"].filename

                        print(type(file))

                        data_faces.append(DataFace(**separated_form))

                        success_added_count += 1

            preformat = Utils.get_custom_preformat_render('add_people.html',
                                                          obj=AddPeopleViewModel(success_added_count, False),
                                                          script='add_input_fields.js')
        else:
            preformat = Utils.get_custom_preformat_render('add_people.html', obj=None, script='add_input_fields.js')
        return render_template(**preformat)

    @staticmethod
    def check_for_error(key: str, value: str, array_df_constructor: dict, return_error_string: list,
                        actual_line: int) -> bool:
        if key.startswith("inputDA"):
            if not Utils.verify_field(value, FieldsType.DA):
                return_error_string.append(f"Line ({actual_line}) : DA is not valid")
                return True
            array_df_constructor["da"] = value
        if key.startswith("inputName"):
            if not Utils.verify_field(value, FieldsType.NAME):
                return_error_string.append(f"Line ({actual_line}) : Name is not valid")
                return True
            array_df_constructor["name"] = value
        if key.startswith("inputFName"):
            if not Utils.verify_field(value, FieldsType.NAME):
                return_error_string.append(f"Line ({actual_line}) : First Name is not valid")
                return True
            array_df_constructor["surname"] = value

        return False
