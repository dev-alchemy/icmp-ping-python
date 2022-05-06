import sys
from logging import Logger
from lookup import Lookup

from ping import ping
from connection import Connection


def main():

    try:
        domain = sys.argv[1]

        lookup = Lookup()
        host = lookup.dns_lookup(domainName=domain)
    except Exception as e:
        logger.error("Exception Occured :: Please give an input :: " + str(e))

    try:
        ping(host, domain)
    except Exception as e:
        logger.error("Exception Occured during ping :: " + str(e))


if __name__ == "__main__":
    logger = Logger("Main Logger")
    main()
