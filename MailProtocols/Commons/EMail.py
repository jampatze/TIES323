import datetime

# A simple mail-object.
# Author: Jami Laamanen
# Date: 16.9.2019


class EMail:

    sender = ''
    recipient = ''
    timestamp = datetime.datetime.now()
    data = ''

    # Initializes a new mail
    def __init__(self):
        pass

    # Prints the mail.
    def __str__(self):
        return self.sender + ' to ' + self.recipient + ' on ' + self.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ': ' + self.data

    # Sets the sender of this mail.
    def set_sender(self, sender):
        self.sender = sender

    # Sets the recipient of this mail.
    def set_recipient(self, recipient):
        self.recipient = recipient

    # Sets the data of this mail.
    def set_data(self, data):
        self.data = data
