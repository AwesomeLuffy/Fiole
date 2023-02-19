from src.Model.Utils.DataFace import DataFace
from src.Model.Utils.DBHandlerManager import DBHandlerManager
from src.Model.Database.database_handler import DatabaseHandler
from enum import Enum
import re
from werkzeug.datastructures import ImmutableMultiDict


class FieldsType(Enum):
    DA = 1
    NAME = 2
    FILE = 3


class AddPeopleModel:
    PATTERN_REGEX_DA = re.compile("^[0-9]{9,12}$")

    PATTERN_REGEX_NAME = re.compile("^[a-zA-ZÀ-ÿ\\-\\s]{1,40}$")

    LIST_ACCEPT_FILES = [".jpg", ".jpeg", ".png"]

    FORM_DA = "inputDA"
    FORM_NAME = "inputName"
    FORM_FNAME = "inputFName"
    FORM_FILE = "formFile"
    FORM_ACCESS = "flexSwitchCheckAccess"


    def __init__(self):
        pass

    @staticmethod
    def add_people(data: ImmutableMultiDict, files: dict) -> tuple[int, list[str]]:
        """Method to add people to the database
            Get the data from the form and split it into array by the number at the end of the field
            For example: inputData0, inputName0, inputFile0 will be split into 1 array
            And inputData1, inputName1, inputFile1 will be split into another array

            :param data: The data from the form
            :param files: The files from the form
            :return: A tuple with the number of people added and a list of error
        """
        data = data.items()
        return_error_string = []
        actual_form = 0
        data_faces = []
        success_added_count = 0

        separated_form = {}

        for key, value in data:

            # If the number at the end changed or if a field not valid we check the another
            # line of fields
            if not key.endswith(str(actual_form)):
                if key == "":
                    break
                if AddPeopleModel.verify_field(files[f"formFile{actual_form}"].filename,
                                               FieldsType.FILE) and return_error_string == []:
                    file = files[f"formFile{actual_form}"]
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
            AddPeopleModel.check_for_error(key, value, separated_form, return_error_string, actual_form)

            if key.startswith("flexSwitchCheckAccess"):
                separated_form["have_access"] = True

        if len(data_faces) > 0:
            DBHandlerManager.insert_faces_db(data_faces)

        return success_added_count, return_error_string

    # Method to verify field from a form
    @staticmethod
    def verify_field(field: str, field_type: FieldsType) -> re.Match[str] | None | bool:
        """Method to verify a field from a form
            :param field: The field to verify
            :param field_type: The type of the field
            :return: A regex match if the field is a DA or a name, None if the field is a file and False if the field is
            not valid
            """
        if field_type == FieldsType.DA:
            return AddPeopleModel.PATTERN_REGEX_DA.match(field)
        elif field_type == FieldsType.NAME:
            return AddPeopleModel.PATTERN_REGEX_NAME.match(field)
        elif field_type == FieldsType.FILE:
            return field.split(".")[-1] not in AddPeopleModel.LIST_ACCEPT_FILES
        else:
            return False

    @staticmethod
    def check_for_error(key: str, value: str, array_df_constructor: dict, return_error_string: list,
                        actual_line: int) -> bool:
        """Method to check if a field is valid

            :param key: The key of the field
            :param value: The value of the field
            :param array_df_constructor: The array to add the field
            :param return_error_string: The list of error
            :param actual_line: The actual line of the form
            :return: True if the field is not valid, False if the field is valid
            """
        if key.startswith(AddPeopleModel.FORM_DA):
            if not AddPeopleModel.verify_field(value, FieldsType.DA):
                return_error_string.append(f"Line ({actual_line}) : DA is not valid ({value})")
                return True
            elif DatabaseHandler.check_value_exists("faces", "da", (value,)):
                return_error_string.append(f"Line ({actual_line}) : DA already exists ({value})")
                return True
            array_df_constructor["da"] = value
        if key.startswith(AddPeopleModel.FORM_NAME):
            if not AddPeopleModel.verify_field(value, FieldsType.NAME):
                return_error_string.append(f"Line ({actual_line}) : Name is not valid ({value})")
                return True
            array_df_constructor["name"] = value
        if key.startswith(AddPeopleModel.FORM_FNAME):
            if not AddPeopleModel.verify_field(value, FieldsType.NAME):
                return_error_string.append(f"Line ({actual_line}) : File Name is not valid ({value})")
                return True
            array_df_constructor["surname"] = value

        return False
