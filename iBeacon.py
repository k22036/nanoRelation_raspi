from Config import Config
from pybleno import Bleno

config = Config()
bleno = Bleno()


def iBeacon_start():
    # UUID (16バイト), Major (2バイト), Minor (2バイト), TX Power (1バイト)
    uuid = bytes.fromhex(config.iBeacon_uuid)
    major = (int(config.iBeacon_major)).to_bytes(2, byteorder='big')
    minor = (int(config.iBeacon_minor)).to_bytes(2, byteorder='big')
    measuredPower = -60

    bleno.startAdvertisingIBeacon(uuid, major, minor, measuredPower)
    print('start iBeacon')
