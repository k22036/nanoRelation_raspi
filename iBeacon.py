from Config import Config
from pybleno import Bleno

config = Config()

# UUID, Major, Minor, Measured Power
uuid = config.iBeacon_uuid
major = int(config.iBeacon_major)
minor = int(config.iBeacon_minor)
measuredPower = -60  # RSSI at 1 meter

bleno = Bleno()


def on_state_change(state):
    print(f"State changed to: {state}")
    if state == 'poweredOn':
        print('Starting to advertise iBeacon...')
        bleno.startAdvertisingIBeacon(uuid, major, minor, measuredPower)
    else:
        bleno.stopAdvertising()


def on_advertising_start(error):
    if error:
        print(f"Advertising start error: {error}")
    else:
        print('iBeacon advertising started')


bleno.on('stateChange', on_state_change)
bleno.on('advertisingStart', on_advertising_start)


def iBeacon_start():
    global major, minor
    major = int(config.iBeacon_major)
    minor = int(config.iBeacon_minor)
    bleno.start()
    print("Waiting for Bluetooth state change...")
