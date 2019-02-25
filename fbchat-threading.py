#!/usr/bin/python3

from fbchat import Client
from fbchat.models import *
from time import sleep
import threading

email = "<email>"
pw = "<password>"

def send():
    client = Client(email, pw)

    sleep(2)    # We sleep here just to avoid the "Login successful" message interfering with our input

    while True:
        payload = input('Message: ')
        if payload:
            client.send(Message(text=payload), thread_id=client.uid, thread_type=ThreadType.USER)

def receive():
    client2 = Client(email, pw)     # We have to create a dedicated Client for listening,
    client2.listen()                # while still being able to send messages


# Creating and starting separate threads for handling receiving and sending messages
t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send)
t1.start()
t2.start()

class PrintMessage(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        print("Incoming message: " + message_object.text) # This does not work for some reason
