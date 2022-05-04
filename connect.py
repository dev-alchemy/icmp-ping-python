from cgitb import lookup
import socket
import os
import struct
import time
import select

from connection import Connection
from protocols import TCPPacketCreator
from connect import Connection

conn = Connection()


def ping(host, count=4, timeout=2):

    addr = host
    print(str("Host") +
          " is Ping {0} [{1}] have 32 Bytes of data :".format(str(host), str(addr)))

    lost = 0
    accept = 0
    sumtime = 0.0
    times = []

    for counter in range(count):
        tcp_packet = TCPPacketCreator()
        counter += 1
        icmp_packet = tcp_packet.request(int(counter))
        rawsocket, dst_addr = conn.connect(addr, icmp_packet)
        time0, sequence, ttl = tcp_packet.reply(
            rawsocket, time.time(), timeout)
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
          .format(int(counter), accept, lost, lost // (lost + accept) * 100,))
    print(' Estimated time of round trip ( In Milliseconds ):')
    print('\t The shortest = {0:.2f}ms, The longest = {1:.2f}ms, Average = {2:.2f}ms'
          .format(min(times), max(times), sum(times) // (lost + accept)))
