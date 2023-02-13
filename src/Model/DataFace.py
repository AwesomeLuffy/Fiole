import numpy


class DataFace:

    def __init__(self, da: int, img, name: str, surname: str, have_access: bool):
        self.name = name
        self.surname = surname
        self.have_access = have_access
        self.img = img
        self.da = da
        self.face_encoded = None

    def build_face_encoded(self, face_encoded):
        nd = numpy.ndarray
        nd.dumps()
        pass

