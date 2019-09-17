# Common utilities used across the server
# Author Jami Laamanen
# Date 16.9.2019
import socket


# Initializes a socket for listening for connectoins
def init_socket(host, port, connections):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(connections)
    return s