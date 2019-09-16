import socket

# A low-level SMTP-server for the TIES323-course.
# Author: Jami Laamanen
# Date: 10.9.2019


class SMTPServer:

    # Use the IANA assigned SMTP-port
    PORT = 25
    HOST = 'localhost'
    CONNECTIONS = 1

    def __init__(self):
        pass

    # Initialize a socket and return it.
    def init_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        s.listen(self.CONNECTIONS)
        return s

    # Listen for incoming connections and send replies.
    def listen(self):
        s = self.init_socket()
        print('SMTP initialized, now listening for incoming connections.')
        while True:
            (conn, addr) = s.accept()
            # Accept the connection
            with conn:
                print('Connection (SMTP) from: ', addr)
                conn.send(str.encode("220 " + self.HOST + " Simple Mail Transfer Service Ready \n"))

                while True:
                    data = conn.recv(1024)
                    if data:
                        reply = self.handle_smtp_message(data)
                        if 'QUIT' not in data.decode():
                            conn.send(str.encode(reply))
                        else:
                            print('Disconnect (SMTP) form: ', addr)
                            conn.close()
                            break

    # Handle the incoming data.
    # Parse and return appropriate reply as string.
    def handle_smtp_message(self, data):
        message = data.decode('UTF-8').split()
        if message[0] == 'HELO':
            reply = '250 ' + self.HOST + " OK"
        elif message[0] == 'MAIL' and message[1] == 'FROM:':
            reply = '250 2.1.0 OK'
        elif message[0] == 'RCPT' and message[1] == 'TO:':
            reply = '250 2.1.5 OK'
        elif message[0] == 'DATA':
            reply = '354 Start mail input; end with <CRLF>.<CRLF>'
        elif message[-1] == '.':
            reply = '250 2.0.0 OK'
        elif message[0] == "QUIT":
            reply = '221 ' + self.HOST + ' Service closing transmission channel'
        else:
            reply = '503'

        # print('Sent: ' + reply)
        return reply + ' \n'




