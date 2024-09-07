from Config import Config

config = Config()
bleno = config.bleno


def iBeacon_start():
    # iBeaconの広告パケットの構成
    ibeacon_prefix = bytes([
        0x02, 0x01, 0x1A,  # Flags
        0x1A,  # Length of the remaining advertisement
        0xFF,  # Manufacturer specific data
        0x4C, 0x00,  # Apple company identifier (0x004C)
        0x02,  # iBeacon type
        0x15   # Length of remaining iBeacon data
    ])

    # UUID (16バイト), Major (2バイト), Minor (2バイト), TX Power (1バイト)
    uuid = bytes.fromhex('e2c56db5dffb48d2b060d0f5a71096e0')
    major = (1).to_bytes(2, byteorder='big')
    minor = (1).to_bytes(2, byteorder='big')
    tx_power = (200).to_bytes(1, byteorder='big')

    # 完全なiBeaconパケット
    ibeacon_packet = ibeacon_prefix + uuid + major + minor + tx_power

    # iBeaconの広告を開始
    bleno.startAdvertisingWithEIRData(ibeacon_packet, bytes([]))
