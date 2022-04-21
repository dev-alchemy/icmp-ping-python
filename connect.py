import socket
import os
import struct
import time
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                     socket.getprotobyname("icmp"))


def connect(address, packet):

    sock.sendto(packet, (address, 800))
    return sock, address


def request(seq, data="abcd"):

    type = 8
    code = 0
    check_sum = 0
    ID = os.getpid() & 0xffff

    # data = bytes(data)
    data = b'abcdefghijklmnopqrstuvwabcdefghi'
    icmp_packet = struct.pack('>BBHHH32s', type, code,
                              check_sum, ID, seq, data)
    check_sum = checksum(icmp_packet)  # Get the checksums

    icmp_packet = struct.pack('>BBHHH32s', type, code,
                              check_sum, ID, seq, data)
    return icmp_packet


def checksum(data):
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


def reply(rawsocket, ping_time, timeout=1):
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
        type, code, checksum, packet_id, sequence = struct.unpack(
            ">BBHHH", icmpHeader)
        if type == 0:
            return received_time - ping_time, sequence, ttl


def ping(host, count=4, timeout=2):
    addr = socket.gethostbyname(host)  # obtain ip Address
    print(" is Ping {0} [{1}] have 32 Bytes of data :".format(host, addr))
    lost = 0
    accept = 0
    sumtime = 0.0
    times = []  # Count the round-trip time of all packets
    for i in range(count):
        i += 1
        icmp_packet = request(i)
    # print(icmp_packet)
        rawsocket, dst_addr = connect(addr, icmp_packet)
        time0, sequence, ttl = reply(rawsocket, time.time(), timeout)
        if time0 < 0:
            print(" request timeout ")
            lost += 1
            times.append(timeout * 1000)
        else:
            time0 = time0 * 1000
            print(" come from {0} Reply to : byte =32 seq = {1} Time ={2:.2f}ms TTL={3}".format(
                dst_addr, sequence, time0, ttl))
            accept += 1
            sumtime += time0
            times.append(time0)
    # Statistics
    print('{0} Of Ping Statistics :'.format(addr))
    print('\t Data packets : Has been sent = {0}, Received = {1}, The loss of = {2} ({3}% The loss of ),'
          .format(count, accept, lost, lost // (lost + accept) * 100,))
    print(' Estimated time of round trip ( In Milliseconds ):')
    print('\t The shortest = {0:.2f}ms, The longest = {1:.2f}ms, Average = {2:.2f}ms'
          .format(min(times), max(times), sum(times) // (lost + accept)))


ping("www.google.com")
