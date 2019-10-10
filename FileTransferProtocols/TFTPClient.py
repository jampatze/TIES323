# A simple client for retrieving files over a network with TFTP
# Author: Jami Laamanen
# Date: 26.9.2019

import os
import select
import socket
from FileTransferProtocols import TFTPUtils as Utils

HOST = '127.0.0.1'
PORT = 69


# Receives a file from the server and saves it to disk
def receive_file(s):
    file_name = input('Enter file to read: \n')
    s.sendto(Utils.create_read_request(file_name), (HOST, PORT))

    last_addr = (HOST, PORT)
    last_packet = Utils.create_read_request(file_name)
    content = b''
    block = 1

    s.sendto(last_packet, last_addr)

    while True:
        # Check time-out
        while True:
            data_ready = select.select([s], [], [], 1)

            if data_ready[0]:
                while True:
                    data, addr = s.recvfrom(600)
                    last_addr = addr
                    # Check data
                    if Utils.check_data(data, block):
                        break
                    else:
                        print("Erroneous packet, resending..")
                        s.sendto(last_packet, last_addr)
                break
            else:
                print('Last packet timed out, resending.')
                s.sendto(last_packet, last_addr)

        last_packet = Utils.create_ack(data[2:4])
        s.sendto(last_packet, last_addr)
        content += data[4:]
        block += 1

        if len(data) < 516:
            f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), 'wt')
            f.write(content.decode())
            f.close()
            print('File read.')
            break


# Opens a file from this directory and sends it
def send_file(s):
    file_name = input('Enter file to send: \n')

    try:
        file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), 'rt')

        last_addr = (HOST, PORT)
        last_packet = Utils.create_write_request(file_name)

        s.sendto(last_packet, last_addr)

        # Get ack 0
        while True:
            # Check time-out
            while True:
                data_ready = select.select([s], [], [], 1)

                if data_ready[0]:
                    while True:
                        data, addr = s.recvfrom(600)
                        last_addr = addr
                        # Check data
                        if Utils.check_ack(data, 0):
                            break
                        else:
                            print("Ack 0 erroneous, resending")
                            s.sendto(last_packet, last_addr)
                    break
                else:
                    print('Ack 0 timed out, resending.')
                    s.sendto(last_packet, last_addr)

            content = file.read().encode()
            block = 1
            for i in range(0, len(content), 512):
                content_packet = Utils.create_data_packet(content[i:i + 512], block)
                s.sendto(content_packet, addr)

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
                                s.sendto(content_packet, addr)
                        break
                    else:
                        print('Ack-packet timed out, resending last data packet')
                        s.sendto(content_packet, addr)

                block += 1

            print('File sent')
            break
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
