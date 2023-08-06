import server
from server import *
from client import *
from mc_event import *
import threading
import os


class MCSignal:
    def __init__(self, settings: dict = {}):
        # Sets the host if there is host not set in settings the host is localhost
        try:
            settings["host"]
        except KeyError:
            settings["host"] = "127.0.0.1"

        # Sets the port if there is no port set in settings the port is 19321
        try:
            settings["port"]
        except KeyError:
            settings["port"] = 19321

        # Sets the connection method the standard is "TCP"
        try:
            settings["connect_type"]
        except KeyError:
            settings["connect_type"] = "UDP"

        self.server = Server(settings=settings)
        self.client = Client(settings=settings)

        self.server_thread = threading.Thread(target=self.server.run)
        self.server_thread.start()

    def trigger(self, event: str, file: str):
        # Extracts the filename from path
        head, tail = os.path.split(file)

        # Sends the event
        self.client.send(event, tail)

    def addEvent(self, mc_event: MCEvent):
        self.server.__events__.append(mc_event)










