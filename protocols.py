import socket
import os
import struct
import time
import select


class TCPPacketCreator():

    def __init__(self):
        self.type = 8
        self.code = 0

    def request(self, seq, data="abcd"):
        check_sum = 0
        ID = os.getpid() & 0xffff

        data = b'abcdefghijklmnopqrstuvwabcdefghi'
        icmp_packet = struct.pack('>BBHHH32s', self.type, self.code,
                                  check_sum, ID, seq, data)
        check_sum = self.checksum(icmp_packet)  # Get the checksums

        icmp_packet = struct.pack('>BBHHH32s', self.type, self.code,
                                  check_sum, ID, seq, data)
        return icmp_packet

    def checksum(self, data):
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

    def reply(self, rawsocket, ping_time, timeout=1):
        while True:

            # Starting time
            started_time = time.time()
            # Instantiation select object , Can be read rawsocket, Can be written as empty , Executable is null , Timeout time
            recv = select.select([rawsocket], [], [], timeout)
            # Waiting time
            wait_for_time = (time.time() - started_time)
            # If no writable content is returned, it is judged as timeout
            if recv[0] == []:
                return -1, -1
            # Record the receiving time
            received_time = time.time()
            # Set the bytes of the received packet to 1024 byte
            received_packet, addr = rawsocket.recvfrom(1024)
            # Judge whether it's time-out
            timeout = timeout - wait_for_time
            if timeout <= 0:
                return -1, -1, -1
            # obtain ip The message TTL
            ttl = received_packet[8]
            # obtain icmp The header of the message
            icmpHeader = received_packet[20:28]
            # print(received_packet)
            type, self.code, self.checksum, packet_id, sequence = struct.unpack(
                ">BBHHH", icmpHeader)
            if type == 0:
                return received_time - ping_time, sequence, ttl
