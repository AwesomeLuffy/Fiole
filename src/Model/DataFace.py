import face_recognition


class DataFace:
    DA_PARAMETER_DF = "da"
    NAME_PARAMETER_DF = "name"
    SURNAME_PARAMETER_DF = "surname"
    HAVE_ACCESS_PARAMETER_DF = "have_access"
    IMG_PATH_PARAMETER_DF = "img_path"

    def __init__(self, da: int, img_path, name: str, surname: str, have_access: bool):
        self.name = name
        self.surname = surname
        self.have_access = have_access
        self.img_path = img_path
        self.da = da
        self.face_encoded = None
        self.face_encoded_bytes = None

    def build_face_encoded(self) -> tuple[bool, str]:
        """
        Build the face encoded from the image path
        Return true if success, false if not
        :return: tuple[bool, str]
        """
        try:
            image = face_recognition.load_image_file(self.img_path)
            self.face_encoded = face_recognition.face_encodings(image)[0]
            self.face_encoded_bytes = bytes(memoryview(self.face_encoded))
            return True, "Success"
        except IndexError:
            return False, f"Error : no face detected for this image !"
        except Exception as e:
            print(e)
            return False, "Error occurred"

