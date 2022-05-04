import sys
from logging import Logger
from lookup import Lookup

from connect import ping
from connection import Connection


def main():

    try:
        domain = sys.argv[1]

        lookup = Lookup()
        domain_name = lookup.dns_lookup(domainName=domain)
    except Exception as e:
        logger.error("Exception Occured :: Please give an input :: " + str(e))

    try:
        ping(domain_name)
    except Exception as e:
        logger.error("Exception Occured during ping :: " + str(e))


if __name__ == "__main__":
    logger = Logger("Main Logger")
    main()
