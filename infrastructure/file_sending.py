import socket
from infrastructure.util import read_file_in_chunks, tcp_read_first_packet, tcp_create_first_packet
import threading
import os
from queue import Queue
from infrastructure.timeout import Timeout
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

CHUNK_SIZE = 10
FIRST_PACKET_SIZE = 51


class TCPSender:
    def __init__(self, my_address, friend_address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout = Timeout()
        self.update_timeout()
        self.other_address = friend_address
        self.this_address = my_address
        self.main_thread = None

    def run(self, path):
        # Cover me, I'm reloading

        while True:
            try:
                self.update_timeout()
                self.sock.connect(self.other_address)
                break
            except socket.error as e:
                continue
            
        # This is it, soldiers. Time to make a difference
        file_name = os.path.basename(path)
        file_size = os.path.getsize(path)
        first_packet = tcp_create_first_packet(file_name, file_size)
        self.update_timeout()
        self.sock.sendall(first_packet.encode('utf-8'))

        # send data
        for data in read_file_in_chunks(path, chunk_size=CHUNK_SIZE):
            self.update_timeout()
            self.sock.sendall(data)
        
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_file(self, path):  # Listen up boys. We've got a new mission
        self.main_thread = threading.Thread(target=self.run, args=(path, ))
        self.main_thread.daemon = True
        self.main_thread.start()

    def is_sending(self):
        if self.main_thread is None:
            return False
        return self.main_thread.is_alive()

    def update_timeout(self):
        self.sock.settimeout(self.timeout.get_timeout())


class TCPReceiver:
    def __init__(self, my_address, friend_address, dir_path='./received files'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(my_address)
        self.other_address = friend_address
        self.this_address = my_address
        self.directory = dir_path
        self.buffer = Queue()
        self.timeout = Timeout()
        main_thread = threading.Thread(target=self.run)
        main_thread.daemon = True
        main_thread.start()

    def run(self):
        
        while True:
            self.sock.listen()
            conn, addr = self.sock.accept()
            # get first packet
            first_packet = conn.recv(FIRST_PACKET_SIZE)
            file_name, file_size = tcp_read_first_packet(first_packet.decode('utf-8'))
            file_path = os.path.join(self.directory, file_name)
            file = open(file_path, 'wb+')

            bytes_received = 0
            while True:
                data = conn.recv(CHUNK_SIZE)
                bytes_received += len(data)
                file.write(data)
                print("Received:", data, "\t\t", bytes_received, file_size, self.timeout.get_timeout())
                if bytes_received == file_size:  # Extraction inbound
                    file.close()
                    break

            # we're done here boys, return to base
            self.buffer.put(file_name)
