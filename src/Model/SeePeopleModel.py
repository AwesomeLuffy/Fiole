from typing import List

from src.Model.Database.database_handler import DatabaseHandler
from src.Model.Utils.DBHandlerManager import DBHandlerManager
import base64
from src.Model.AddPeopleModel import AddPeopleModel
from src.Model.Utils.DataFace import DataFace
import os


class SeePeopleModel:

    def __init__(self):
        pass

    @staticmethod
    def modify_people(separated_form: dict) -> List[str]:
        """Modify a person in the database
        It will check if the form is valid and then modify the person in the database
        :param separated_form: dict
        :return: list of error, return empty list if no error
        """
        return_error_string = []

        for key, value in separated_form.items():
            # AppPeople and modify people use the same verification
            if AddPeopleModel.check_for_error(key, value, separated_form, return_error_string, 0):
                break

        if not return_error_string:
            data_face = DataFace(**separated_form)

            DBHandlerManager.update_face_db(data_face)

        return return_error_string

    @staticmethod
    def delete_people(da: str):
        """Delete a person in the database
        :param da: da of the person
        :return: None
        """
        da_image_path, = DatabaseHandler.read_values(f"SELECT image_location FROM {DBHandlerManager.MYSQL_FACE_TABLE} WHERE da = %s",
                                                     (da,),
                                                     only_one=True)
        if da_image_path:
            os.remove(da_image_path)
        DBHandlerManager.delete_face_db(int(da))

    @staticmethod
    def get_unknowns() -> list[tuple]:
        """Get all unknown faces from the database
        :return:
        """
        sql = f"SELECT name, image, date_inserted FROM {DBHandlerManager.MYSQL_UNKNOWN_TABLE}"
        values = DatabaseHandler.read_values(sql, as_dict=True)
        # Get BLOB image and convert to base64

        for value in values:
            value["image"] = base64.b64encode(value["image"]).decode("utf-8")
        return values

    @staticmethod
    def delete_unknown() -> int:
        """Delete all unknown faces from the database

        :return: number of rows deleted
        """
        sql = f"DELETE FROM {DBHandlerManager.MYSQL_UNKNOWN_TABLE}"
        return DatabaseHandler.delete_values(sql, None)

    @staticmethod
    def delete_specific_unknown(name: str) -> int:
        """Delete a specific unknown face from the database

        name: name of the unknown face

        :return: number of rows deleted
        """
        sql = f"DELETE FROM {DBHandlerManager.MYSQL_UNKNOWN_TABLE} WHERE name = %s"
        return DatabaseHandler.delete_values(sql, (name,))
