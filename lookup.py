from asyncio.log import logger
import socket
from logging import Logger


class Lookup():

    def __init__(self):
        logger = Logger("Lookup.py Logger Inititaited")
        logger.info("Lookup Class Initiated")

    def dns_lookup(self, domainName):
        ip_addr = socket.gethostbyname(domainName)
        return ip_addr

    def reverse_dns_lookup(self, ip):
        domain_name = socket.gethostbyaddr(ip)[0]
        return domain_name
