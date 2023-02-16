from src.Model.DataFace import DataFace
from src.Model.database_handler import DatabaseHandler


class FacesDB:

    @staticmethod
    def insert_faces_db(data_faces: list[DataFace]):
        sql = "INSERT INTO faces (da, nom, prenom, encoded, image_location, acces) VALUES (%s, %s, %s, %s, %s, %s)"
        val = [(face.da, face.name, face.surname, face.face_encoded_bytes, face.img_path, face.have_access) for face in
               data_faces]
        return DatabaseHandler.insert_query(sql, val)

    @staticmethod
    def delete_face_db(da: int):
        sql = "DELETE FROM faces WHERE da = %s"
        # return DatabaseHandler.insert_query(sql, da)

    @staticmethod
    def get_all_faces_db():
        sql = "SELECT da, image_location, nom, prenom FROM faces"
        return DatabaseHandler.read_values(sql, as_dict=True)
