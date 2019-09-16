import threading

from SMTPServer import SMTPServer

# Main class of the server, handles threading other protocols.
# Author: Jami Laamanen
# Date: 16.9.2019

# Initializes the server and services

if __name__ == "__main__":
    print('Welcome to the TIES323-server!')
    threads = list()

    smtp = SMTPServer()
    smtp_thread = threading.Thread(smtp.listen(), args=(), daemon=True)
    threads.append(smtp)
