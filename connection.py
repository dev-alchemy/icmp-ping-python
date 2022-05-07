import socket


class Connection():

    def __init__(self):
        print(":: Connection Initialised For :: ")

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                  socket.getprotobyname("icmp"))
        print("Client")
        return self.sock

    def establish(self, address, packet):
        self.sock.sendto(packet, (address, 80))
        return self.sock, address

    def create_server(self):
        server = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        server.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
        print("Server")
        return server
