def make_packet(ack: int, data: str):
    return get_checksum(data) + '\t' + str(ack) + '\t' + data


def make_ack(ack: int):
    return str(ack) + '\t '


def corrupt_from_sender(data: str):
    try:
        checksum, ack, data = data.split('\t', 2)
        int(ack)
        if get_checksum(data) != checksum:
            return True
        return False
    except:
        print("Corrupt: ", data)
        return True


def corrupt_from_receiver(data: str):
    try:
        ack, _ = data.split('\t', 1)
        int(ack)
        return False
    except:
        return True


def get_ack(data: str):
    ack, _ = data.split('\t', 1)
    return int(ack)


def get_sender_ack(data: str):
    __, ack, _ = data.split('\t', 2)
    return int(ack)


def get_checksum(data: str):
    # Calculate checksum
    checksum = 0
    data = data.encode('utf-8')

    # Padding if the length of data is odd
    if len(data) % 2 != 0:
        data += b'\x00'

    # Calculate the one's complement sum
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word

    left_part = (checksum >> 16)
    right_part = (checksum & 0xffff)
    checksum = left_part + right_part
    checksum += checksum >> 16  # add any trailing 1
    checksum = ~checksum & 0xffff  # ones complement (the & 0xffff is to discard the higher order bits)
    return str(checksum)


def read_file_in_chunks(file_path, chunk_size=1024):
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data


def get_content(message: str):
    return message.split('\t', maxsplit=2)[-1]


def tcp_create_first_packet(name, size):
    return str(size).ljust(10, " ") + '\t' + str(name).ljust(40, " ")


def tcp_read_first_packet(packt: str):
    size, name = packt.split('\t', 1)
    size = size.strip()
    name = name.strip()
    return name, int(size)
