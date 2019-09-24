from MailProtocols.Commons.Inbox import Inbox
from MailProtocols.Main.IMAPService import IMAPService
from MailProtocols.Main.POP3Service import POP3Service
from MailProtocols.Main.SMTPService import SMTPService

# Main class of the server, handles threading other protocols.
# Author: Jami Laamanen
# Date: 16.9.2019

# Initializes the server and used services

if __name__ == "__main__":
    print('Welcome to the TIES323-server!')

    inbox = Inbox()

    pop3 = POP3Service(inbox)
    smtp = SMTPService(inbox)
    imap = IMAPService(inbox)

    while True:
        pass
