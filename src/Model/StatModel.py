import threading

from src.Model.Database.database_handler import DatabaseHandler
from src.Model.Utils.Client import Client
from src.Model.Utils.JWToken import JWToken
from _thread import *
from enum import Enum
from src.Model.Utils.DBHandlerManager import DBHandlerManager
import socket


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

    SERVER_RESPONSE = ""

    def __init__(self):
        pass

    @staticmethod
    def get_access_count() -> tuple[int, int]:
        values = DatabaseHandler.read_values(f"SELECT acces FROM {DBHandlerManager.MYSQL_FACE_TABLE}")
        # Convert list of tuple to list
        values = [value[0] for value in values]
        return values.count(True), values.count(False)

    @staticmethod
    def get_number_of_unknown() -> int:
        return DatabaseHandler.read_values(f"SELECT COUNT(*) FROM {DBHandlerManager.MYSQL_UNKNOWN_TABLE}")[0][0]

    @staticmethod
    def action_on_raspberry(act: Actions) -> str:
        try:
            communication = threading.Thread(target=StatModel.communicate_with_raspberry, args=(act,))
            communication.start()
            communication.join()
            return StatModel.SERVER_RESPONSE
        except Exception:
            pass
        finally:
            StatModel.SERVER_RESPONSE = ""

    @staticmethod
    def communicate_with_raspberry(act: Actions):
        try:
            clt = Client(start=True)
            token_with_data = JWToken.generate_jw_token(header=StatModel.TOKEN_HEADER,
                                                        payload={"action": act.value},
                                                        secret=StatModel.TOKEN_SECRET,
                                                        validity=1)
            clt.send(str(token_with_data))

            StatModel.SERVER_RESPONSE = clt.receive()
            if StatModel.SERVER_RESPONSE == "":
                StatModel.SERVER_RESPONSE = "No response from the raspberry, timeout"
            clt.close()
        except socket.timeout:
            StatModel.SERVER_RESPONSE = "No response from the raspberry, timeout"
        except ConnectionRefusedError:
            StatModel.SERVER_RESPONSE = "Connection refused by the raspberry, is it running ?"
        except Exception:
            StatModel.SERVER_RESPONSE = "An error occurred while communicating with the raspberry"
