# A simple TFTP-server
# Author: Jami Laamanen
# Date: 27.9.2019

import os
import select
import socket
from FileTransferProtocols import TFTPUtils as Utils

HOST = '127.0.0.1'
COMMAND_PORT = 69
FILE_PORT = 6969


# Sends given file content to the given address.
def send_data(content, addr):
    data = content.encode()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, FILE_PORT))

    block = 1
    for i in range(0, len(data), 512):
        data_packet = Utils.create_data_packet(data[i:i + 512], block)
        s.sendto(data_packet, addr)

        # Check time-out
        while True:
            data_ready = select.select([s], [], [], 1)

            if data_ready[0]:
                # Check ack
                while True:
                    reply = s.recv(600)
                    if Utils.check_ack(reply, block):
                        break
                    else:
                        print("Erroneous ack-packet, re-sending the last block.")
                        s.sendto(data_packet, addr)
                break
            else:
                print('Ack-packet timed out, resending last data packet')
                s.sendto(data_packet, addr)

        block += 1

    s.close()
    print('File sent')


# Takes data from a connection and writes it to a file
def receive_data(file_name, addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, FILE_PORT))
    s.sendto(Utils.create_ack(b'\x00\x00'), addr)

    content = b''
    block = 1
    ack = Utils.create_ack(b'\x00\x01')  # Create ack 1
    while True:
        # Check time-out
        while True:
            data_ready = select.select([s], [], [], 1)

            if data_ready[0]:
                while True:
                    data, addr = s.recvfrom(600)
                    # Check data
                    if Utils.check_data(data, block):
                        break
                    else:
                        print("Erroneous data-packet, re-sending last ack-packet.")
                        s.sendto(ack, addr)
                break
            else:
                print('Data-packet timed out, resending last ack-packet')
                s.sendto(ack, addr)

        s.sendto(Utils.create_ack(data[2:4]), addr)
        content += data[4:]
        block += 1

        if len(data) < 516:
            f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), 'wt')
            f.write(content.decode())
            f.close()
            print('File read.')
            break


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
                receive_data(Utils.parse_req(data), addr)


if __name__ == "__main__":
    print('Welcome to the TIES323 TFTP-Server!')
    print('Listening on ' + HOST + ':' + str(COMMAND_PORT))
    run()
