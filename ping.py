from cgitb import lookup
import socket
import os
import struct
import time
import select

from connection import Connection
from protocols import TCPPacketCreator

conn = Connection()
conn.connect()


def ping(host, host_name, count=2, timeout=2):

    addr = host
    print("\npinging {0} with 256 Bytes of data :\n".format(
        str(host)))

    lost = 0
    accept = 0
    sumtime = 0.0
    times = []
    counter = 1

    # for counter in range(count):
    while counter <= count:
        tcp_packet = TCPPacketCreator()

        icmp_packet = tcp_packet.request(int(counter))
        rawsocket, dst_addr = conn.establish(addr, icmp_packet)
        reply_time, sequence, ttl = tcp_packet.reply(
            rawsocket, time.time(), timeout)
        if reply_time < 0:
            print(" request timeout ")
            lost += 1
            times.append(timeout * 1000)
        else:
            reply_time = reply_time * 1000
            print(" 256 byte from {0} seq = {1} Time ={2:.2f}ms TTL={3}".format(
                dst_addr, sequence, reply_time, ttl))
            accept += 1
            sumtime += reply_time
            times.append(reply_time)

        counter += 1

    print(
        '\n-----------Ping Statistics for {0}------------------- :'.format(host_name))
    print('\n Data packets sent = {0}, Received = {1}, lost = {2} ({3}% The loss of ),'
          .format(int(counter), accept, lost, lost // (lost + accept) * 100,))
    print('---------------Estimated time of round trip ( In Milliseconds )---------------- \n')
    print('The shortest = {0:.2f}ms, The longest = {1:.2f}ms, Average = {2:.2f}ms'
          .format(min(times), max(times), sum(times) // (lost + accept)))
