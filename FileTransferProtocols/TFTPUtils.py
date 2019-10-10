# Shared functions to be used both in the server and client implementations of TFTP
# Author: Jami Laamanen
# Date: 1.10.2019
import struct

# Packet creation


# Creates a read request from the given file name
def create_read_request(file_name):
    b = b'\x00\x01'
    b += str.encode(file_name)
    b += b'\x00'
    b += str.encode('netascii')
    b += b'\x00'

    return b


# Creates a data packet from the given, already split data
def create_data_packet(data, i):
    b = b'\x00\x03'
    b += struct.pack(">H", i)
    b += data

    return b


# Creates a ack-packet
def create_ack(block_id):
    b = b'\x00\x04'
    b += block_id

    return b


# Creates a write request from the given file name
def create_write_request(file_name):
    b = b'\x00\x02'
    b += str.encode(file_name)
    b += b'\x00'
    b += str.encode('netascii')
    b += b'\x00'

    return b

# Other utils


# Checks if ack-packet is acceptable
def check_ack(data, id):
    return data[:2] == b'\x00\x04' and int.from_bytes(data[2:4], byteorder='big') == id


# Checks if data-packet is acceptable
def check_data(data, id):
    return data[:2] == b'\x00\x03' and int.from_bytes(data[2:4], byteorder='big') == id


# Parses info from a req packet
def parse_req(data):
    data = data[2:]
    return data.split(b'\x00')[0].decode()


# Checks if the received package was marked as error
def check_error(data):
    return data[:2] == b'\x00\x05'






