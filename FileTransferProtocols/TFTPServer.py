# A simple TFTP-server
# Author: Jami Laamanen
# Date: 27.9.2019

import os
import socket
from FileTransferProtocols import TFTPUtils as Utils

HOST = '127.0.0.1'
COMMAND_PORT = 69
FILE_PORT = 6969


# Sends given file content to the given address.
def send_data(content, addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, FILE_PORT))
    Utils.send_data(s, content.encode(), addr)
    print('File sent')


# Starts the server and listens for incoming connections.
def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, COMMAND_PORT))

    while True:
        data, addr = s.recvfrom(600)

        if data:
            if data[:2] == b'\x00\x01':
                file_name = Utils.parse_req(data)

                try:
                    file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), 'rt')
                except FileNotFoundError:
                    print('File not found')
                    s.close()
                    break

                send_data(file.read(), addr)
            elif data[:2] == b'\x00\x02':
                file_name = Utils.parse_req(data)
                s.sendto(Utils.create_ack(b'\x00\x00'), addr)
                Utils.receive_file(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), 'wt'), s)


if __name__ == "__main__":
    print('Welcome to the TIES323 TFTP-Server!')
    print('Listening on ' + HOST + ':' + str(COMMAND_PORT))
    run()
