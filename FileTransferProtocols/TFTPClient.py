# A simple client for retrieving files over a network with TFTP
# Author: Jami Laamanen
# Date: 26.9.2019
import os
import socket

HOST = '127.0.0.1'
PORT = 69


# Creates a ack-packet
def create_ack(block_id):
    b = b'\x00\x04'
    b += block_id

    return b


# Checks if the received package was a error package
def check_error(data):
    return data[:2] == b'\x00\x05'


# Creates a read request from the given file name
def create_read_request(file_name):
    b = b'\x00\x01'
    b += str.encode(file_name)
    b += b'\x00'
    b += str.encode('netascii')
    b += b'\x00'

    return b


# Handles the TFTP-session and communication to the server
def handle_session(s):
    file_name = input('Enter file to read:')

    s.sendto(create_read_request(file_name), (HOST, PORT))
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), 'wt')

    while True:
        data, addr = s.recvfrom(600)

        if check_error(data):
            print('Error')
            s.close()
            break

        s.sendto(create_ack(data[2:4]), addr)
        content = data[4:]
        f.write(content.decode())

        if len(data) < 512:
            f.close()
            print('File retrieved, closing connection!')
            break


if __name__ == "__main__":
    print('Welcome to the TIES323 TFTP-Client!')
    print('Connecting to ' + HOST + ' on port ' + str(PORT))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    handle_session(s)
