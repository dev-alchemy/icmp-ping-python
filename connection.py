import socket


class Connection():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                  socket.getprotobyname("icmp"))

    def connect(self, address, packet):
        self.sock.sendto(packet, (address, 800))
        return self.sock, address
