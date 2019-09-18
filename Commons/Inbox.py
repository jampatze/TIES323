from threading import Lock

# Mocks a server side-inbox for storing mail.
# Stored mails do not persist over server restart
# Author: Jami Laamanen
# Date: 16.9.2019

class Inbox:

    mails = list()
    lock = Lock()

    # Empty initializer.
    def __init__(self):
        pass

    # Adds a mail to the inbox
    def add_mail(self, mail):
        self.lock.acquire()
        self.mails.append(mail)
        self.lock.release()

    # Returns a formatted list of messages in the inbox.
    def get_mails(self):
        mails = ''

        for mail in self.mails:
            mails += mail.__str__() + '\n'

        # Remove extra new line from the end
        if len(mails) > 0:
            mails = mails[:-1]

        return mails

    # Returns the amount of messages in the list.
    def get_message_amount(self):
        return len(self.mails)
