import socket
import struct
import select

from protocols import TCPPacketCreator
from connection import Connection

conn = Connection()
sock_server = conn.create_server()
mySocket = sock_server

print("Recieving ping from client")

while True:

    recPacket, addr = sock_server.recvfrom(1024)
    icmp_header = recPacket[20:28]
    type, code, checksum, p_id, sequence = struct.unpack(
        '>BBHHH', icmp_header)

    # tcp_packet = TCPPacketCreator()
    # icmp_res = tcp_packet.request(sequence, data=b'This is a test')

    # sock_server.sendto(icmp_res, addr)

    print("type: [" + str(type) + "] code: [" + str(code) + "] checksum: [" +
          str(checksum) + "] p_id: [" + str(p_id) + "] sequence: [" + str(sequence) + "]")

    print("ICMP data ---- : " + str(recPacket[31:]))

    print("Size of String representation is {}.".format(
        struct.calcsize('>BBHHH')))
