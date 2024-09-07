from Config import Config
from pybleno import *
from NanoRelationInitCharacteristic import NanoRelationInitCharacteristic

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

nanoRelationInitCharacteristic = NanoRelationInitCharacteristic()


def onAdvertisingStart(error):
    print('on -> advertisingStart: ' +
          ('error ' + error if error else 'success'))

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': NANORELATION_INIT_SERVICE_UUID,
                'characteristics': [
                    nanoRelationInitCharacteristic
                ]
            })
        ])


bleno.on('advertisingStart', onAdvertisingStart)

bleno.start()


while True:
    input('Press <Enter> to stop...\n')
