from src.Model.Database.database_handler import DatabaseHandler


class StatModel:

    MAX_UNKNOWN = 999

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
