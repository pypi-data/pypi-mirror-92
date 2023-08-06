"""
import server

Server = server.Server()

def func1():
    print("This event call")


def func2():
    print("help command")


Server.addEvent(server.MCEvent(name="call", call_function=func1))
Server.addEvent(server.MCEvent(name="help", call_function=func2))

Server.run()

"""

from mc_signal import *

hello = MCSignal()

def funci():
    print("dflkfj")

hi = MCEvent(name="mye", call_function=funci)

hello.addEvent(hi)

hello.trigger("mye", __file__)

