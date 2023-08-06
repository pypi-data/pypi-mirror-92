import socket
import logging
import time

from dataclasses import dataclass

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 2.0
DISCOVERY_PORT = 23272
MAXCUBE_MAGIC = b'eQ3Max'
MAXCUBE_DISCOVERY_HEADER = b'*\0'
MAXCUBE_BROADCAST_ADDRESS = b'*' * 10
MAXCUBE_DISCOVERY_CMD = b'I'
MAXCUBE_DISCOVERY_MSG = MAXCUBE_MAGIC + MAXCUBE_DISCOVERY_HEADER + MAXCUBE_BROADCAST_ADDRESS + MAXCUBE_DISCOVERY_CMD

@dataclass(frozen=True)
class DiscoveredCube:
    address: str
    serial: str
    rf_address: str
    version: str

class Discovery:
    def __init__(self):
        self.__buffer: bytearray = bytearray()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.__socket.settimeout(DEFAULT_TIMEOUT)
        self.__socket.bind(("", 23272))


    def start(self):
        self.__socket.sendto(MAXCUBE_DISCOVERY_MSG, ('<broadcast>', DISCOVERY_PORT))
        try:
            while True:
                reply, addr = self.__socket.recvfrom(1024)
                print("Response from %s: %s\n" % (addr, reply.hex()))
                if len(reply) < 26:
                    continue
                if not reply.startswith(MAXCUBE_MAGIC):
                    continue
                if reply[19:20] != MAXCUBE_DISCOVERY_CMD:
                    continue

                serial = reply[8:18].decode('utf-8')
                rf_address = reply[21:24].hex()
                fw_version = "%d.%d.%d" % (int(reply[24]), int(reply[25] >> 4), int(reply[25] % 16))
                cube = DiscoveredCube(addr[0], serial, rf_address, fw_version)
                print("Cube detected: %s\n" % cube)
        except:
            raise

        """
Name?              8           eQ3MaxAp
Serial number      10          KEQ0523864
Request ID         1           >
Request Type       1           I
Zero               1           0
RF address         3           097F2C
Firmware version   2           1.1.3          
        """

d = Discovery()
d.start()