from threading import Thread

from MailProtocols.Commons import Utils

# Interacts with the inbox and replies to IMAP-connections.
# Author: Jami Laamanen
# Date: 18.9.2019


class IMAPService(Thread):

    PORT = 143
    HOST = 'localhost'
    CONNECTIONS = 1

    # Initializes the IMAP-service
    def __init__(self, inbox):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.inbox = inbox

    # Listens for IMAP-connections and sends replies
    def run(self):
        s = Utils.init_socket(self.HOST, self.PORT, self.CONNECTIONS)
        print('IMAP initialized, now listening for incoming connections.')
        while True:
            # Accept new connection
            (conn, addr) = s.accept()
            with conn:
                print('(IMAP) Connection from: ', addr)
                conn.send(str.encode('OK IMAP ready for requests from  <' + addr[0] + '>\n'))

                while True:
                    data = conn.recv(1024)
                    if data:
                        reply = self.handle_pop3_message(data)

                        if not reply.isspace():
                            if 'a006 logout' not in data.decode().upper():
                                conn.send(str.encode(reply))
                            else:
                                print('(IMAP) Disconnect form: ', addr)
                                conn.close()
                                break

    # Handles a single POP3-message and creates appropriate reply
    def handle_pop3_message(self, data):
        message = data.decode('UTF-8')

        if 'a001 login' in message:
            reply = 'a001 OK LOGIN completed'
        elif 'a002 select inbox' in message:
            reply = '10 EXISTS \n' \
                    '* FLAGS (\Answered \Flagged \Deleted \Seen \Draft) \n' \
                    '* ' + str(self.inbox.get_message_amount()) + ' RECENT \n' \
                    'a002 OK [READ-WRITE] SELECT completed'
        elif 'a006 logout' in message:
            reply = 'a006 OK LOGOUT completed'
        else:
            reply = message[0:3] + 'BAD No such command'

        return reply + '\n'
