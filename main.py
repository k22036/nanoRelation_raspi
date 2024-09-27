from Config import Config
from pybleno import *
from NanoRelationInitCharacteristic import NanoRelationInitCharacteristic_read, NanoRelationInitCharacteristic_write

config = Config()

NANORELATION_INIT_SERVICE_UUID = config.NANORELATION_INIT_SERVICE_UUID
bleno = config.bleno


def onStateChange(state):
    print('on -> stateChange: ' + state)

    if (state == 'poweredOn'):
        bleno.startAdvertising(name='Approach', service_uuids=[
                               NANORELATION_INIT_SERVICE_UUID])
    else:
        bleno.stopAdvertising()


bleno.on('stateChange', onStateChange)

nanoRelationInitCharacteristic_read = NanoRelationInitCharacteristic_read()
nanoRelationInitCharacteristic_write = NanoRelationInitCharacteristic_write()


def onAdvertisingStart(error):
    print('on -> advertisingStart: ' +
          ('error ' + str(error) if error else 'success'))

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': NANORELATION_INIT_SERVICE_UUID,
                'characteristics': [
                    nanoRelationInitCharacteristic_read,
                    nanoRelationInitCharacteristic_write
                ]
            })
        ])


bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()
bleno.disconnect()


try:
    input("Press Enter to stop...\n")
finally:
    bleno.stopAdvertising()
    bleno.disconnect()
