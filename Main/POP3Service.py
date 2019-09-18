from threading import Thread

from Commons import Utils

# Interacts with the inbox and replies to POP3-connections.
# Author: Jami Laamanen
# Date: 16.9.2019


class POP3Service(Thread):

    PORT = 110
    HOST = 'localhost'
    CONNECTIONS = 1

    # Initializes the POP3-service
    def __init__(self, inbox):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.inbox = inbox

    # Listens for POP3-connections and sends replies
    def run(self):
        s = Utils.init_socket(self.HOST, self.PORT, self.CONNECTIONS)
        print('POP3 initialized, now listening for incoming connections.')
        while True:
            # Accept new connection
            (conn, addr) = s.accept()
            with conn:
                print('(POP3) Connection from: ', addr)
                conn.send(str.encode('+OK POP3 server ready for requests <' + self.HOST + '>\n'))

                while True:
                    data = conn.recv(1024)
                    if data:
                        reply = self.handle_pop3_message(data)
                        if 'QUIT' not in data.decode().upper():
                            conn.send(str.encode(reply))
                        else:
                            print('(POP3) Disconnect form: ', addr)
                            conn.close()
                            break
                    else:
                        conn.close()

    # Handles a single POP3-message and creates appropriate reply
    def handle_pop3_message(self, data):
        message = data.decode('UTF-8')

        if 'USER' in message.upper():
            reply = '+OK send PASS'
        elif 'PASS' in message.upper():
            reply = '+OK Welcome.'
        elif 'LIST' in message.upper():
            reply = '+OK ' + str(self.inbox.get_message_amount()) + ' messages: \n' + self.inbox.get_mails()
        elif 'QUIT' in message.upper():
            reply = '+OK Farewell.'

        return reply + '\n'
