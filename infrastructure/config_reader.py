import configparser


class ConfigReader:
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def get_value(self, section, key):
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    def get_appclient_info(self) -> dict:
        info = dict()

        ip = self.get_value("ME", "IP")
        udp_send = self.get_value("ME", "UDP_SEND_PORT")
        udp_receiver = self.get_value("ME", "UDP_RECV_PORT")
        tcp_send = self.get_value("ME", "TCP_SEND_PORT")
        tcp_receiver = self.get_value("ME", "TCP_RECV_PORT")

        udp_send = int(udp_send)
        udp_receiver = int(udp_receiver)
        tcp_send = int(tcp_send)
        tcp_receiver = int(tcp_receiver)

        info["rcv_address"] = (ip, udp_receiver)
        info["send_address"] = (ip, udp_send)
        info["send_address_tcp"] = (ip, tcp_send)
        info["rcv_address_tcp"] = (ip, tcp_receiver)

        ip = self.get_value("FRIEND", "IP")
        udp_send = self.get_value("FRIEND", "UDP_SEND_PORT")
        udp_receiver = self.get_value("FRIEND", "UDP_RECV_PORT")
        tcp_send = self.get_value("FRIEND", "TCP_SEND_PORT")
        tcp_receiver = self.get_value("FRIEND", "TCP_RECV_PORT")

        udp_send = int(udp_send)
        udp_receiver = int(udp_receiver)
        tcp_send = int(tcp_send)
        tcp_receiver = int(tcp_receiver)

        info["friend_rcv_address"] = (ip, udp_receiver)
        info["friend_send_address"] = (ip, udp_send)
        info["friend_rcv_address_tcp"] = (ip, tcp_receiver)
        info["friend_send_address_tcp"] = (ip, tcp_send)

        info["path_to_files_save"] = self.get_value("OTHER", "PATH_TO_SAVED_FILES")

        return info

    def get_username(self):
        return self.get_value("OTHER", "NAME")
