#!/usr/bin/env python3

from infrastructure.base_classes import Sender, Receiver
from infrastructure.file_sending import TCPReceiver, TCPSender
from time import sleep
from RDT import AppClient

client1 = AppClient(
    rcv_address=("127.0.0.1", 5000),
    send_address=("127.0.0.1", 5001),
    friend_rcv_address=("127.0.0.1", 5002),
    friend_send_address=("127.0.0.1", 5003),
    path_to_files_save="client1_files",
    rcv_address_tcp=("127.0.0.1", 6000),
    send_address_tcp=("127.0.0.1", 6001),
    friend_rcv_address_tcp=("127.0.0.1", 6002),
    friend_send_address_tcp=("127.0.0.1", 6003)
)

client2 = AppClient(
    rcv_address=("127.0.0.1", 5002),
    send_address=("127.0.0.1", 5003),
    friend_rcv_address=("127.0.0.1", 5000),
    friend_send_address=("127.0.0.1", 5001),
    path_to_files_save="client2_files",
    rcv_address_tcp=("127.0.0.1", 6002),
    send_address_tcp=("127.0.0.1", 6003),
    friend_rcv_address_tcp=("127.0.0.1", 6000),
    friend_send_address_tcp=("127.0.0.1", 6001)
)


client1.send_message("Hi man")
client1.send_message("Do you wanna go to the movies sometime ?")

sleep(20)

message1 = client2.get_messages()
print(message1)

client2.send_message("Hi man, of course why not we will figure it out.")

sleep(10)

response = client1.get_messages()
print(response)

