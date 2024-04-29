"""
EVERYTHING IS NON-BLOCKING AND THREADED
"""
from infrastructure.base_classes import Sender, Receiver
from infrastructure.file_sending import TCPReceiver, TCPSender
from infrastructure.util import get_content


class AppClient:
    # Note that each client needs 4 ports. 2 for each protocol (one is receiving and one is sending).
    def __init__(self, rcv_address, send_address, friend_rcv_address, friend_send_address, path_to_files_save,
                 rcv_address_tcp, send_address_tcp, friend_rcv_address_tcp, friend_send_address_tcp):
        self.sender = Sender(send_address, friend_rcv_address)
        self.receiver = Receiver(rcv_address, friend_send_address)
        self.tcp_sender = TCPSender(send_address_tcp, friend_rcv_address_tcp)
        self.tcp_receiver = TCPReceiver(rcv_address_tcp, friend_send_address_tcp, dir_path=path_to_files_save)

    def send_message(self, message):
        self.sender.send_buffer.put(message)

    def get_messages(self):
        messages = []
        while not self.receiver.rcv_buffer.empty():
            m = self.receiver.rcv_buffer.get()
            messages.append(get_content(m))
        return messages

    def send_file(self, path_to_file):
        if self.tcp_sender.is_sending():  # cannot send two files simultaneously
            return False
        self.tcp_sender.send_file(path_to_file)
        return True

    def get_next_message(self):
        """
        This is a blocking call
        :return:
        """
        message = self.receiver.rcv_buffer.get(block=True, timeout=None)
        return get_content(message)

    def get_next_file_sent(self):
        filename = self.tcp_receiver.buffer.get(block=True, timeout=None)
        return filename

    def close_all(self):
        if self.sender.sock is not None:
            self.sender.sock.close()
        if self.receiver.sock is not None:
            self.receiver.sock.close()
        if self.tcp_sender.sock is not None:
            self.tcp_sender.sock.close()
        if self.tcp_receiver.sock is not None:
            self.tcp_receiver.sock.close()
