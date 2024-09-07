from Config import Config

config = Config()
bleno = config.bleno


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
uuid = bytes.fromhex(config.iBeacon_uuid)
major = (config.iBeacon_major).to_bytes(2, byteorder='big')
minor = (config.iBeacon_minor).to_bytes(2, byteorder='big')
tx_power = (200).to_bytes(1, byteorder='big')

# 完全なiBeaconパケット
ibeacon_packet = ibeacon_prefix + uuid + major + minor + tx_power


def iBeacon_start():

    bleno.stopAdvertising()
    bleno.disconnect()

    bleno.startAdvertisingWithEIRData(ibeacon_packet, bytes([]))
    print('start iBeacon')
