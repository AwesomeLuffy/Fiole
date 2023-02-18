import base64

import bcrypt

from src.Model.Utils.DataFace import DataFace
from src.Model.Database.database_handler import DatabaseHandler


class DBHandlerManager:
    """Class to communicate with the database

    This class is used to communicate with the database. It is used to insert, delete, update and get data from the database.
    Instead of database_handler that only used to execute queries, this class is used to execute queries and convert the data
    """

    @staticmethod
    def insert_faces_db(data_faces: list[DataFace]):
        """Insert a list of faces into the database

        data_faces: list of DataFace to insert
        """
        sql = "INSERT INTO faces (da, nom, prenom, encoded, image_location, acces) VALUES (%s, %s, %s, %s, %s, %s)"
        # Convert DataFace to tuple
        val = [(face.da, face.name, face.surname, face.face_encoded_bytes, face.img_path, face.have_access) for face in
               data_faces]
        return DatabaseHandler.insert_query(sql, val)

    @staticmethod
    def delete_face_db(da: int):
        """ Delete a face from the database

        da: da of the face to delete
        """
        sql = "DELETE FROM faces WHERE da = %s"
        return DatabaseHandler.delete_values(sql, (da,))

    @staticmethod
    def get_all_faces_db():
        """Get all faces from the database
        :return:
        """
        sql = "SELECT da, image_location, nom, prenom, acces FROM faces"
        return DatabaseHandler.read_values(sql, as_dict=True)

    @staticmethod
    def get_unknown():
        """Get all unknown faces from the database
        :return:
        """
        sql = "SELECT name, image, date_inserted FROM unknows"
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
        sql = "DELETE FROM unknows"
        return DatabaseHandler.delete_values(sql, None)

    @staticmethod
    def delete_specific_unknown(name: str) -> int:
        """Delete a specific unknown face from the database

        name: name of the unknown face

        :return: number of rows deleted
        """
        sql = "DELETE FROM unknows WHERE name = %s"
        return DatabaseHandler.delete_values(sql, (name,))

    @staticmethod
    def update_face_db(face: DataFace):
        """Update the face in the database

        face: face to update
        """
        sql = "UPDATE faces SET nom = %s, prenom = %s, acces = %s WHERE da = %s"
        val = (face.name, face.surname, face.have_access, face.da)
        return DatabaseHandler.update_values(sql, val)

    @staticmethod
    def check_user_encoded_password(username: str, password_check: str) -> bool:
        """Check if the password is correct for the user by encoding it and comparing it to the one in the database
        username: username of the user

        password_check: password to check


        :return: True if the password is correct, False otherwise
        """
        sql = "SELECT password FROM user WHERE name = %s"
        password, = DatabaseHandler.read_values(sql, (username,), only_one=True)
        return bcrypt.checkpw(password_check.encode('utf-8'), password.encode('utf-8'))

    @staticmethod
    def check_user_exists(user: str) -> bool:
        """ Check if the user exists in the database
        :param user: username to check
        :return: True if the user exists, False otherwise
        """
        return DatabaseHandler.check_value_exists("user", "name", (user,))
