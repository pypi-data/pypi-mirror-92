import socket

class Client:
    def __init__(self, settings: dict):

        self.host = settings["host"]
        self.port = settings["port"]
        self.connect_type = settings["connect_type"]

    def send(self, event: str, sender: str):
        if self.connect_type == "UDP":

            # Encodes the data
            data = f"{sender};{event}"

            # Sends the package via UDP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(bytes(data, "ascii"), (self.host, self.port))



