class MySQLFlaskHandler:

    def __init__(self, app):
        self.app = app
        self.connection = None
        self.cursor = None
