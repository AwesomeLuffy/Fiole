# Fiole (A Website to manage another project : FaceRecognition
![image](https://github.com/AwesomeLuffy/Fiole/assets/56047226/fb8937e2-7d1e-4db5-8768-c7be3743a373)

# Introduction

For an end-therm school project at Cégep de Saint-Félicien, we had to create a system that allow to manage from a Website a way to add some face in the Database, see intruders and a lot of features.
This project is only in French and it's not planned to translate it.

# How is it made

Fiole use the framework [Flask](https://flask.palletsprojects.com/en/3.0.x/).
Flask is a micro web framework written in Python to create a web application.

So the backend is made in Python and the frontend is made in HTML, CSS and JavaScript.
For the HTML part I use [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/), a template engine for Python.

# Communication between project

With the library socket from Python, the Website is a "client" and the another project has a script that is the server.
From the Website we can send request to the server to add a face, delete a face, see the intruders, etc.

The only shared things between project is the database.

## Client-Server
In the `src/Model/Utils/Client.py` it's possible to change the Host (the Server) IP and the port.

```py
class Client:
    RECEIVE_TIMEOUT = 10
    RECEIVE_MAX_SIZE = 1024

    HOST_PORT = 45634 # The port of the server
    
    # Simply change the host to the server IP or create a local variable
    def __init__(self, host: str = "127.0.0.1", port: int = HOST_PORT, start: bool = False):
        self.host = host
        self.port = port
        ...
```

## Database

In this project I used Docker with PHPMyAdmin and MySQL to create the database.

You can simply change the Database configuration in the `src/Model/Database/database_handler.py` file.

Simply change the `ConnectionData` variable to your own configuration.

```py
    ConnectionData = {
        "host": "localhost",
        "port": 3307,
        "user": "root",
        "password": "test",
        "database": "data_faces"
    }

    # Return a connection to the database but not close it
    @staticmethod
    def get_conn():
        return mc.connect(**DatabaseHandler.ConnectionData)
```

## Connexion

The Website handle multiple user but cannot add it in a simple way presently.

However, the website can handle "Remember Me" feature with a [JWT](https://jwt.io/) system.
The code is in the `src/Model/Utils/JWToken.py` file.
