from threading import Thread

from Commons import Utils
from Commons.EMail import EMail

# A low-level SMTP-server for the TIES323-course.
# Author: Jami Laamanen
# Date: 10.9.2019


class SMTPService(Thread):

    # Use the IANA assigned SMTP-port
    PORT = 25
    HOST = 'localhost'
    CONNECTIONS = 1

    def __init__(self, inbox):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.inbox = inbox

    # Listen for incoming connections and send replies.
    def run(self):
        s = Utils.init_socket(self.HOST, self.PORT, self.CONNECTIONS)
        print('SMTP initialized, now listening for incoming connections.')
        while True:
            # Accept new connection
            (conn, addr) = s.accept()
            with conn:
                print('(SMTP) Connection from: ', addr)
                conn.send(str.encode("220 " + self.HOST + " Simple Mail Transfer Service Ready \n"))
                mail = EMail()

                while True:
                    data = conn.recv(1024)
                    if data:
                        reply = self.handle_smtp_message(data, mail)
                        if 'QUIT' not in data.decode():
                            conn.send(str.encode(reply))
                        else:
                            print('(SMTP) Disconnect form: ', addr)
                            conn.send(str.encode(reply))
                            self.inbox.add_mail(mail)
                            print('(SMTP) New mail: ', mail)
                            conn.close()
                            break

    # Handle the incoming data.
    # Parse and return appropriate reply as string.
    def handle_smtp_message(self, data, mail):
        message = data.decode('UTF-8')
        if 'HELO' in message:
            reply = '250 ' + self.HOST + " OK"
        elif 'MAIL FROM' in message:
            mail.set_sender(message.split()[2])
            reply = '250 2.1.0 OK'
        elif 'RCPT TO' in message:
            mail.set_recipient(message.split()[2])
            reply = '250 2.1.5 OK'
        elif 'DATA' in message:
            reply = '354 Start mail input; end with <CRLF>.<CRLF>'
        elif message.endswith('.\r\n'):
            mail.set_data(message[:-5])
            reply = '250 2.0.0 OK'
        elif 'QUIT' in message:
            reply = '221 ' + self.HOST + ' Service closing transmission channel'
        else:
            reply = '503'

        # print('Sent: ' + reply)
        return reply + ' \n'
