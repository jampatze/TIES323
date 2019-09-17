import threading

from Commons.Inbox import Inbox
from Main.POP3Service import POP3Service
from Main.SMTPService import SMTPService

# Main class of the server, handles threading other protocols.
# Author: Jami Laamanen
# Date: 16.9.2019

# Initializes the server and used services

if __name__ == "__main__":
    print('Welcome to the TIES323-server!')

    inbox = Inbox()

    pop3 = POP3Service(inbox)
    smtp = SMTPService(inbox)

    while True:
        pass







