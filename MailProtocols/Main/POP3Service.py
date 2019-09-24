import os
import ssl
from threading import Thread

from MailProtocols.Commons import Utils

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

        # SSL
        main_path = os.path.dirname(os.path.abspath(__file__))
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=main_path + '/server.crt', keyfile=main_path + '/server.key')
        client_path = main_path[0:-5]
        context.load_verify_locations(cafile=client_path + '/client.crt')

        print('POP3 initialized, now listening for incoming connections.')
        while True:
            # Accept new connection
            (conn, addr) = s.accept()
            sconn = context.wrap_socket(conn, server_side=True)
            with sconn:
                print('(POP3) Connection from: ', addr)
                sconn.send(str.encode('+OK POP3 server ready for requests <' + self.HOST + '>\n'))

                while True:
                    try:
                        data = sconn.recv(1024)
                        if data:
                            reply = self.handle_pop3_message(data)
                            if 'QUIT' not in data.decode().upper():
                                sconn.send(str.encode(reply))
                            else:
                                print('(POP3) Disconnect form: ', addr)
                                sconn.close()
                                break
                    except ConnectionAbortedError:
                        print('SSL verification failed')
                        print('(POP3) Disconnect form: ', addr)
                        sconn.close()
                        break

    # Handles a single POP3-message and creates appropriate reply
    def handle_pop3_message(self, data):
        message = data.decode('UTF-8')

        if 'USER' in message.upper():
            reply = '+OK send PASS'
        elif 'PASS' in message.upper():
            reply = '+OK Welcome.'
        elif 'LIST' in message.upper():
            reply = '+OK ' + str(self.inbox.get_message_amount()) + ' messages: \n' + self.inbox.get_mails_pop3()
        elif 'QUIT' in message.upper():
            reply = '+OK Farewell.'
        else:
            reply = '-ERR error'

        return reply + '\n'
