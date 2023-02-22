import threading

from src.Model.Database.database_handler import DatabaseHandler
from src.Model.Utils.Client import Client
from src.Model.Utils.JWToken import JWToken
from _thread import *
from enum import Enum


class Actions(Enum):
    ACTUALIZE_FACE = "actualize_face"
    STOP_CAMERA = "stop_camera"
    START_CAMERA = "start_camera"


class StatModel:

    MAX_UNKNOWN = 999

    TOKEN_HEADER = {
        "alg": "HS256",
        "typ": "JWT"
    }
    TOKEN_SECRET = "secret"

    def __init__(self):
        pass

    @staticmethod
    def get_access_count() -> tuple[int, int]:
        values = DatabaseHandler.read_values("SELECT acces FROM faces")
        # Convert list of tuple to list
        values = [value[0] for value in values]
        return values.count(True), values.count(False)

    @staticmethod
    def get_number_of_unknown():
        return DatabaseHandler.read_values("SELECT COUNT(*) FROM unknows")[0][0]

    @staticmethod
    def actualize_face_on_raspberry():
        return_msg = ""
        def communicate_with_raspberry():
            clt = Client(start=True)
            token_with_data = JWToken.generate_jw_token(header=StatModel.TOKEN_HEADER,
                                                        payload={"action": Actions.STOP_CAMERA.value},
                                                        secret=StatModel.TOKEN_SECRET,
                                                        validity=1)
            clt.send(str(token_with_data))

            return_msg = clt.receive()
            clt.close()
        communication = threading.Thread(target=communicate_with_raspberry)
        communication.start()
        communication.join()
        print("End of communication with raspberry")



