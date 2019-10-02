# Shared functions to be used both in the server and client implementations of TFTP
# Author: Jami Laamanen
# Date: 1.10.2019
import select
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


# Send & receive

# Handles communication after read request and writes to the given file
def receive_file(f, s):

    content = b''
    block = 1
    ack = create_ack(b'\x00\x01')  # Create ack 1
    while True:
        # Check time-out
        while True:
            data_ready = select.select([s], [], [], 1)

            if data_ready[0]:
                while True:
                    data, addr = s.recvfrom(600)
                    # Check data
                    if check_data(data, block):
                        break
                    else:
                        print("Erroneous data-packet, re-sending last ack-packet.")
                        s.sendto(ack, addr)
                break
            else:
                print('Data-packet timed out, resending last ack-packet')
                s.sendto(ack, addr)

        s.sendto(create_ack(data[2:4]), addr)
        content += data[4:]
        block += 1

        if len(data) < 516:
            f.write(content.decode())
            f.close()
            print('File read.')
            break


# Handles communication after a write request
def send_file(f, s):
    reply, addr = s.recvfrom(600)
    data = f.read().encode()
    send_data(s, data, addr)
    print("File sent.")


# Sends data over the given connection
def send_data(s, data, addr):
    block = 1
    for i in range(0, len(data), 512):
        data_packet = create_data_packet(data[i:i + 512], block)
        s.sendto(data_packet, addr)

        # Check time-out
        while True:
            data_ready = select.select([s], [], [], 1)

            if data_ready[0]:
                # Check ack
                while True:
                    reply = s.recv(600)
                    if check_ack(reply, block):
                        break
                    else:
                        print("Erroneous ack-packet, re-sending the last block.")
                        s.sendto(data_packet, addr)
                break
            else:
                print('Ack-packet timed out, resending last data packet')
                s.sendto(data_packet, addr)

        block += 1


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






