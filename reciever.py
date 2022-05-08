import socket
import struct
import select

from protocols import TCPPacketCreator
from connection import Connection
from writer import write_to_file

conn = Connection()
sock_server = conn.create_server()
conn.connect()

print("Recieving ")

while True:
    recPacket, addr = sock_server.recvfrom(1024)
    icmp_header = recPacket[20:28]
    type, code, checksum, p_id, sequence = struct.unpack(
        '>BBHHH', icmp_header)

    print(recPacket)

    file_string = "\nSenders Address :: " + str(addr[0] + "\n")
    file_string = file_string + ("ICMP Header :: " + str(icmp_header) + "\n")
    file_string = file_string + ("Type :: " + str(type) + "\n")
    file_string = file_string + ("Code :: " + str(code) + "\n")
    file_string = file_string + ("Sequence :: " + str(sequence) + "\n")
    file_string = file_string + ("Data :: " + str(recPacket) + "\n")

    write_to_file(file_name="reply", write_data=file_string)
