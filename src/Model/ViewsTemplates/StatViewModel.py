from src.Model.StatModel import StatModel


class StatViewModel:

    def __init__(self, access_count: tuple[int, int] = (50, 50), unknown_count: int = 1):
        self.server_response = ""
        access_true_count, access_false_count = access_count
        self.access_true_count_percentage = 0 if access_true_count == 0 else access_true_count / (
                access_true_count + access_false_count) * 100
        self.access_false_count_percentage = 100 - self.access_true_count_percentage

        self.unknown_count = unknown_count
        self.max_unknown = StatModel.MAX_UNKNOWN
        self.unknown_percentage = self.unknown_count / self.max_unknown * 100

    def define_server_response(self, server_response: str):
        self.server_response = server_response
