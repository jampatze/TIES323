import os
import re
import socket
import sys

# A simple client for retrieving files over a network with FTP
# Author: Jami Laamanen
# Date: 25.9.2019

HOST = '127.0.0.1'
COMMAND_PORT = 21


# Raised when login fails.
class LoginError(Exception):
    pass


# Handles communication with the server
def handle_command(cmd, s):
    if cmd == 'QUIT':
        print('Closing connection, goodbye!')
        s.send(str.encode('QUIT \n'))
        s.close()
        sys.exit()
    elif 'LIST' in cmd:
        d_s = init_passive_mode(s)

        s.send(str.encode(cmd + '\n'))
        reply = s.recv(1024).decode()

        if '550' in reply:
            print('Directory not found')

        if '150' in reply:
            data = d_s.recv(1024)

            if data:
                print(data.decode())
            else:
                print('Directory is empty.')

        d_s.close()
    elif 'RETR' in cmd:
        d_s = init_passive_mode(s)

        s.send(str.encode(cmd + '\n'))
        reply = s.recv(1024).decode()

        if '550' in reply:
            print('File not found')

        if '150' in reply:
            data = d_s.recv(1024).decode()

            f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), reply[reply.rfind('/') + 1:reply.rfind('"')]), 'wt')
            f.write(data)
            f.close()

            print('File retrieved.')
        d_s.close()


# Handles user input, forms a reply to the server from user input
def get_user_input():
    while True:
        cmd = input()

        if 'HELP' == cmd:
            print('Currently supported commands: HELP, QUIT, LIST [<SP><path>], RETR <SP> <pathname>')
        elif 'QUIT' == cmd:
            reply = 'QUIT'
            break
        elif 'LIST' in cmd:
            if re.search('^LIST( \/([A-z0-9-_+]+\/)*)?$', cmd):
                reply = cmd
                break
            else:
                print('LIST-command not valid')
        elif 'RETR' in cmd:
            if re.search('^RETR (\/([A-z0-9-_+]+\/)*)?([a-zA-Z0_9]+)?.*$', cmd):
                reply = cmd
                break
            else:
                print('RETR-command not valid')
        else:
            print('Unrecognized command, try again.')

    return reply


# Parses the file address and port from the given string.
# Argument must be in the form of 'x,x,x,x,x,x'.
def parse_file_address(message):
    t = message.split(',')
    p_addr = t[0] + '.' + t[1] + '.' + t[2] + '.' + t[3]
    p_port = (int(t[4]) * 256) + int(t[5])

    return p_addr, p_port


# Stats passive FTP mode. Returns the data socket.
def init_passive_mode(s):
    s.send(str.encode('PASV \n'))

    while True:
        message = s.recv(1024).decode()
        if '227' in message:
            break

    data_addr, data_port = parse_file_address(message[message.find('(') + 1:message.find(')')])
    return create_socket(data_addr, data_port)


# Handles user login in a linear style
def handle_login(s):
    user = input('Username:')
    s.send(str.encode('USER ' + user + '\n'))
    user_reply = s.recv(1024)

    if '331' not in user_reply.decode():
        raise LoginError

    password = input('Password:')
    s.send(str.encode('PASS ' + password + '\n'))
    password_reply = s.recv(1024)

    if '230' not in password_reply.decode():
        raise LoginError

    print('Logged in.')


# Handles a single session to an FTP-server
def handle_session(s):
    if '220' not in s.recv(1024).decode():
        sys.exit('Server not responding.')

    try:
        handle_login(s)
    except LoginError:
        s.close()
        sys.exit('Login failed, closing connection.')

    print('Type HELP for info.')

    while True:
        cmd = get_user_input()
        handle_command(cmd, s)


# Initializes a new socket and connects it.
def create_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


if __name__ == "__main__":
    print('Welcome to the TIES323 FTP-Client!')
    print('Connecting to ' + HOST + ' on port ' + str(COMMAND_PORT))
    s = create_socket(HOST, COMMAND_PORT)
    handle_session(s)
