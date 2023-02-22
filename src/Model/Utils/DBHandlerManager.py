import base64

import bcrypt

from src.Model.Utils.DataFace import DataFace
from src.Model.Database.database_handler import DatabaseHandler


class DBHandlerManager:
    """Class to communicate with the database

    This class is used to communicate with the database. It is used to insert, delete, update and get data from the database.
    Instead of database_handler that only used to execute queries, this class is used to execute queries and convert the data
    """
    MYSQL_FACE_TABLE = "face"
    MYSQL_UNKNOWN_TABLE = "unknowns"
    MYSQL_USER_TABLE = "user"

    @staticmethod
    def insert_faces_db(data_faces: list[DataFace]):
        """Insert a list of faces into the database

        data_faces: list of DataFace to insert
        """
        sql = f"INSERT INTO {DBHandlerManager.MYSQL_FACE_TABLE} (da, nom, prenom, encoded, image_location, acces) VALUES (%s, %s, %s, %s, %s, %s)"
        # Convert DataFace to tuple
        val = [(face.da, face.name, face.surname, face.face_encoded_bytes, face.img_path, face.have_access) for face in
               data_faces]
        return DatabaseHandler.insert_query(sql, val)

    @staticmethod
    def delete_face_db(da: int):
        """ Delete a face from the database

        da: da of the face to delete
        """
        sql = f"DELETE FROM {DBHandlerManager.MYSQL_FACE_TABLE} WHERE da = %s"
        return DatabaseHandler.delete_values(sql, (da,))

    @staticmethod
    def get_all_faces_db():
        """Get all faces from the database
        :return:
        """
        sql = f"SELECT da, image_location, nom, prenom, acces FROM {DBHandlerManager.MYSQL_FACE_TABLE}"
        return DatabaseHandler.read_values(sql, as_dict=True)

    @staticmethod
    def update_face_db(face: DataFace):
        """Update the face in the database

        face: face to update
        """
        sql = f"UPDATE {DBHandlerManager.MYSQL_FACE_TABLE} SET nom = %s, prenom = %s, acces = %s WHERE da = %s"
        val = (face.name, face.surname, face.have_access, face.da)
        return DatabaseHandler.update_values(sql, val)

    @staticmethod
    def check_user_encoded_password(username: str, password_check: str) -> bool:
        """Check if the password is correct for the user by encoding it and comparing it to the one in the database
        username: username of the user

        password_check: password to check


        :return: True if the password is correct, False otherwise
        """
        sql = f"SELECT password FROM {DBHandlerManager.MYSQL_USER_TABLE} WHERE name = %s"
        password, = DatabaseHandler.read_values(sql, (username,), only_one=True)
        return bcrypt.checkpw(password_check.encode('utf-8'), password.encode('utf-8'))

    @staticmethod
    def check_user_exists(user: str) -> bool:
        """ Check if the user exists in the database
        :param user: username to check
        :return: True if the user exists, False otherwise
        """
        return DatabaseHandler.check_value_exists("user", "name", (user,))
