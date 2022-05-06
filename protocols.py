import socket
import os
import struct
import time
import select


class TCPPacketCreator():

    def __init__(self):
        self.type = 8
        self.code = 0

    def request(self, seq, data="abcdefghijkl"):
        check_sum = 0
        ID = os.getpid() & 0xffff
        data = b'aaaavvvvbbbbbbggggggcdefghi'
        icmp_packet = struct.pack('>BBHHH32s', self.type, self.code,
                                  check_sum, ID, seq, data)
        check_sum = self.create_checksum(icmp_packet)  # Get the checksums

        icmp_packet = struct.pack('>BBHHH32s', self.type, self.code,
                                  check_sum, ID, seq, data)
        return icmp_packet

    def create_checksum(self, data):
        data_length = len(data)
        remainder = data_length % 2
        sum = 0
        for timer in range(0, data_length - remainder, 2):

            sum += (data[timer]) + ((data[timer + 1]) << 8)
            if remainder:
                sum += (data[-1])

            while sum >> 16:
                sum = (sum >> 16) + (sum & 0xffff)

        answer = ~sum & 0xffff
        answer = answer >> 8 | (answer << 8 & 0xff00)
        return answer

    def reply(self, rawsocket, ping_time, timeout=1):
        while True:

            start = time.time()
            recv = select.select([rawsocket], [], [], timeout)
            wait = (time.time() - start)

            if recv[0] == []:
                return -1, -1

            recieved = time.time()

            received_packet, addr = rawsocket.recvfrom(1024)

            timeout = timeout - wait
            if timeout <= 0:
                return -1, -1, -1
            time_to_live = received_packet[8]
            icmpHeader = received_packet[20:28]
            type, self.code, self.create_checksum, packet_id, sequence = struct.unpack(
                ">BBHHH", icmpHeader)
            if type == 0:
                return recieved - ping_time, sequence, time_to_live
