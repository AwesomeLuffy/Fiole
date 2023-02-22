# Import socket module
import socket


class Client:
    RECEIVE_TIMEOUT = 10
    RECEIVE_MAX_SIZE = 1024

    HOST_PORT = 45634

    def __init__(self, host: str = "127.0.0.1", port: int = HOST_PORT, start: bool = False):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if start:
            self.start()

    def start(self):
        self.socket.connect((self.host, self.port))

    def send(self, message):
        self.socket.send(message.encode('ascii'))

    def receive(self) -> str:
        self.socket.settimeout(Client.RECEIVE_TIMEOUT)
        return self.socket.recv(Client.RECEIVE_MAX_SIZE).decode('ascii')

    def close(self):
        self.socket.close()
