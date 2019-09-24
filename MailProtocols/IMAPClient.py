import socket

# Fetches emails from a IMAP-server.
# Author: Jami Laamanen
# Date: 18.9.2019

HOST = 'localhost'
PORT = 143


# Handles messages from the server
# Returns the appropriate reply
def handle_message(data):
    message = data.decode('UTF-8')
    reply = ''

    if 'ready for requests' in message:
        reply = 'a001 login ' + user + ' ' + password
    elif 'a001 OK' in message:
        reply = 'a002 select inbox'
    elif 'a002 OK' in message:
        print(message)
        reply = 'a006 logout'

    return reply + '\r\n'


# Gets emails of the specified user
def retrieve_emails():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except:
        print('Connection failed')

    while True:
        data = s.recv(2048)
        if data:
            if 'a006 OK' in data.decode():
                break
            reply = handle_message(data)

            if not reply.isspace():
                s.send(str.encode(reply))


# Main, handles user interaction
if __name__ == "__main__":
    print('Welcome to the TIES323 IMAP-client')
    user = input('Username:')
    password = input('Password:')
    retrieve_emails()
