# A simple client for retrieving files over a network with TFTP
# Author: Jami Laamanen
# Date: 26.9.2019

import os
import socket
from FileTransferProtocols import TFTPUtils as Utils

HOST = '127.0.0.1'
PORT = 69


# Receives a file from the server and saves it to disk
def receive_file(s):
    file_name = input('Enter file to read: \n')
    s.sendto(Utils.create_read_request(file_name), (HOST, PORT))
    Utils.receive_file(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), 'wt'), s)


# Opens a file from this directory and sends it
def send_file(s):
    file_name = input('Enter file to send: \n')
    s.sendto(Utils.create_write_request(file_name), (HOST, PORT))
    try:
        Utils.send_file(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), 'rt'), s)
    except FileNotFoundError:
        print('No such local file.')


# Handles the TFTP-session and communication to the server
def handle_session(s):
    print("Press s to send, r to read, q to quit.")

    while True:
        cmd = input()

        if 's' == cmd:
            send_file(s)
        elif 'r' == cmd:
            receive_file(s)
        elif 'q' == cmd:
            print("Closing connection, bye!")
            s.close()
            break
        else:
            print("Unknown command, try again.")


if __name__ == "__main__":
    print('Welcome to the TIES323 TFTP-Client!')
    print('Connecting to ' + HOST + ' on port ' + str(PORT))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    handle_session(s)
