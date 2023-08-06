import socket
import types
from typing import List
from mc_event import MCEvent

class Server:
    def __init__(self, settings: dict, events: List[MCEvent] = []):
        # The events call if a signal came
        self.__events__ = events

        self.host = settings["host"]
        self.port = settings["port"]
        self.connect_type = settings["connect_type"]

    def run(self):
        self.__socket_connection_loop__()

    def __data_decoder__(self, data_raw: str):
        data_array = data_raw.split(";")

        # Decodes the package by the standard in NETWORK_STANDARDS.md
        try:
            sender_name = data_array[0]
            signal_name = data_array[1]
        except IndexError:
            raise ConnectionError("Received broken data package")

        # Look for the event that is called on this signal form another file
        for event in self.__events__:
            if event.name == signal_name:
                event.call_function()

    def __socket_connection_loop__(self):
        if self.connect_type == "UDP":
            # Socket connection init
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind((self.host, self.port))

                # Socket loop for connections
                while True:
                    data, addr = s.recvfrom(1024)

                    self.__data_decoder__(data.decode())

        else:
            raise ValueError(f"Connection type '{self.connect_type}' does not exist")








