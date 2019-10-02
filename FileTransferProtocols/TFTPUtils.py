# Shared functions to be used both in the server and client implementations of TFTP
# Author: Jami Laamanen
# Date: 1.10.2019

import struct


# Creates a read request from the given file name
def create_read_request(file_name):
    b = b'\x00\x01'
    b += str.encode(file_name)
    b += b'\x00'
    b += str.encode('netascii')
    b += b'\x00'

    return b


# Checks if the received package was marked as error
def check_error(data):
    return data[:2] == b'\x00\x05'


# Creates a ack-packet
def create_ack(block_id):
    b = b'\x00\x04'
    b += block_id

    return b


# Handles communication after read request and writes to the given file
def receive_file(f, s):

    content = b''
    while True:
        data, addr = s.recvfrom(600)

        if check_error(data):
            print('Error')
            s.close()
            break

        s.sendto(create_ack(data[2:4]), addr)
        content += data[4:]

        if len(data) < 512:
            f.write(content.decode())
            f.close()
            print('File read.')
            break


# Creates a write request from the given file name
def create_write_request(file_name):
    b = b'\x00\x02'
    b += str.encode(file_name)
    b += b'\x00'
    b += str.encode('netascii')
    b += b'\x00'

    return b


# Handles communication after a write request
def send_file(f, s):
    reply, addr = s.recvfrom(600)
    data = f.read().encode()
    send_data(s, data, addr)
    print("File sent")


# Sends data over the given connection
def send_data(s, data, addr):
    block = 1
    for i in range(0, len(data), 512):
        s.sendto(create_data_packet(data[i:i + 512], block), addr)
        if check_ack(s.recv(600)):
            block += 1
        else:
            print("Didn't receive ack, aborting transfer")


# Creates a data packet from the given, already split data
def create_data_packet(data, i):
    b = b'\x00\x03'
    b += struct.pack(">H", i)
    b += data

    return b


# Checks if ack-packet is acceptable
def check_ack(data):
    return data[:2] == b'\x00\x04'


# Parses info from a req packet
def parse_req(data):
    data = data[2:]
    return data.split(b'\x00')[0].decode()





