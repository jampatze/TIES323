import socket

# Fetches emails from a POP3-server.
# Author: Jami Laamanen
# Date: 13.9.2019

HOST = 'localhost'
PORT = 110


# Handles messages from the server
# Returns the appropriate reply
def handle_message(data):
    message = data.decode('UTF-8')

    if 'ready for requests' in message:
        reply = 'user ' + user
    if 'OK send PASS' in message:
        reply = 'pass ' + password
    if 'OK Welcome' in message:
        reply = 'list'
    if 'messages' in message:
        print(message)
        reply = 'quit'

    return reply + ' \n'


# Gets emails of the specified user
def retrieve_emails():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except:
        print('Connection failed')

    while True:
        data = s.recv(1024)
        if data:
            if 'Farewell' in data.decode():
                break
            s.send(str.encode(handle_message(data)))


# Main, handles user interaction
if __name__ == "__main__":
    print('Welcome to the TIES323 POP3-client')
    user = input('Username:')
    password = input('Password:')
    retrieve_emails()


