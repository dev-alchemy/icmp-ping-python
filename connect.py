import socket
import os
import struct


def connect(address, packet):
    socket = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                           socket.getprotobyname("icmp"))
    socket.sendto(packet, (address, 800))
    return socket, address


def request(seq, data="abcd"):
    type = 8
    code = 0
    check_sum = 0
    ID = os.getpid() & 0xffff

    data = bytes(data)

    icmp_packet = struct.pack('>BBHHH32s', type, code,
                              check_sum, ID, seq, data)
    check_sum = checksum(icmp_packet)  # Get the checksums

    icmp_packet = struct.pack('>BBHHH32s', type, code,
                              check_sum, ID, seq, data)
    return icmp_packet


def checksum():
    n = len(data)
    m = n % 2
    sum = 0
    for i in range(0, n - m, 2):
        # Pass in data Every two bytes （ Hexadecimal ）, The first byte is in the low order , The second byte is high
    sum += (data[i]) + ((data[i + 1]) << 8)
    if m:
    sum += (data[-1])
    # Will be higher than 16 Bit and low 16 Add bits
    while sum >> 16:
    sum = (sum >> 16) + (sum & 0xffff)
    # If there is more than 16 position , Will continue with low 16 Add bits
    answer = ~sum & 0xffff
    # Host byte sequence to network byte sequence
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer
