"""
Shape of Sender packet: 'checksum\tack\tdata' where checksum is calculated from 'ack\tdata'
Shape of Receiver Ack: 'ack\t '
"""
import socket
from queue import Queue
from infrastructure.util import *
import threading
from infrastructure.timeout import Timeout


class Sender:
    def __init__(self, address, friend_address):
        self.address = address
        self.friend_address = friend_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)
        self.send_buffer = Queue()
        self.state = 0
        main_thread = threading.Thread(target=self.run)
        main_thread.daemon = True
        main_thread.start()
        self.timeout = Timeout()

    def send(self, data: str):
        self.sock.sendto(data.encode('utf-8'), self.friend_address)
        self.timeout.register_start()

    def receive(self):
        data, addr = self.sock.recvfrom(1024)
        return data.decode('utf-8')

    def state_sending_from(self):
        packt = self.send_buffer.get()  # This is a blocking queue call
        packt = make_packet(self.state, packt)
        self.send(packt)
        return packt

    def state_wait_for_ack(self, packt: str):
        self.sock.settimeout(self.timeout.get_timeout())
        while True:
            try:
                data = self.receive()
                if corrupt_from_receiver(data) or get_ack(data) != self.state:
                    continue
                break
            except socket.timeout:
                # retry sending
                self.send(packt)
                # restart timer
                continue

        self.timeout.register_end()
        self.sock.settimeout(None)

    def run(self):
        while True:
            packt = self.state_sending_from()
            self.state_wait_for_ack(packt)
            self.state += 1


class Receiver:
    def __init__(self, address, friend_address):
        self.address = address
        self.friend_address = friend_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.address)
        self.rcv_buffer = Queue()
        self.ack_state = 0
        main_thread = threading.Thread(target=self.run)
        main_thread.daemon = True
        main_thread.start()

    def send(self, data: str):
        self.sock.sendto(data.encode('utf-8'), self.friend_address)

    def receive(self):
        data, addr = self.sock.recvfrom(1024)
        return data.decode('utf-8')

    def send_ack(self, ack_num):
        self.send(str(ack_num) + '\t ')

    def run(self):
        while True:
            packt = self.receive()
            if corrupt_from_sender(packt):
                continue
            if get_sender_ack(packt) < self.ack_state:
                # send ack
                self.send_ack(get_sender_ack(packt))
                continue
            self.rcv_buffer.put(packt)
            self.send_ack(self.ack_state)
            self.ack_state += 1
