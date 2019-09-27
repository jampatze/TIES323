import os
import socket
import struct

# A simple TFTP-server
# Author: Jami Laamanen
# Date: 27.9.2019


HOST = '127.0.0.1'
COMMAND_PORT = 69
FILE_PORT = 6969


# Checks if ack-packet is acceptable
def check_ack(data):
    return data[:2] == b'\x00\x04'

# Creates a data packet from the given, already split data
def create_data_packet(data, i):
    b = b'\x00\x03'
    b += struct.pack(">H", i)
    b += data

    return b


# Sends the data
def send_data(content, addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, FILE_PORT))

    data = content.encode()

    block = 1
    for i in range(0, len(data), 512):
        s.sendto(create_data_packet(data[i:i + 512], block), addr)
        if check_ack(s.recv(600)):
            block += 1
        else:
            print("Didn't receive ack, aborting transfer")


# Parses info from a read req packet
def parse_read_req(data):
    data = data[2:]
    return data.split(b'\x00')[0].decode()


# Starts the server and listens for incoming connections
def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, COMMAND_PORT))

    while True:
        data, addr = s.recvfrom(600)

        if data:
            file_name = parse_read_req(data)

            try:
                file = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name), 'rt')
            except FileNotFoundError:
                # TODO: error packet
                print('File not found')
                s.close()
                break

            send_data(file.read(), addr)


if __name__ == "__main__":
    print('Welcome to the TIES323 TFTP-Server!')
    print('Listening on ' + HOST + ':' + str(COMMAND_PORT))
    run()
