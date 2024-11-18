import time
from Config import Config
from pybleno import *
from NanoRelationInitCharacteristic import NanoRelationInitCharacteristic_read, NanoRelationInitCharacteristic_write, NanoRelationInitCharacteristic_notify

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
nanoRelationInitCharacteristic_notify = NanoRelationInitCharacteristic_notify()


def onAdvertisingStart(error):
    print('on -> advertisingStart: ' +
          ('error ' + str(error) if error else 'success'))

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': NANORELATION_INIT_SERVICE_UUID,
                'characteristics': [
                    nanoRelationInitCharacteristic_read,
                    nanoRelationInitCharacteristic_write,
                    nanoRelationInitCharacteristic_notify
                ]
            })
        ])


def onDisconnect(clientAddress):
    print('on -> disconnect')
    bleno.disconnect()


bleno.on('advertisingStart', onAdvertisingStart)
bleno.on('disconnect', onDisconnect)

bleno.start()
bleno.disconnect()

counter = 0


def task():
    global counter
    counter += 1
    nanoRelationInitCharacteristic_notify._value = str(counter).encode()
    if nanoRelationInitCharacteristic_notify._updateValueCallback:

        print('Sending notification with value : ' +
              str(nanoRelationInitCharacteristic_notify._value))

        notificationBytes = str(
            nanoRelationInitCharacteristic_notify._value).encode()
        nanoRelationInitCharacteristic_notify._updateValueCallback(
            data=notificationBytes)


try:
    while True:
        task()
        time.sleep(5)
finally:
    bleno.stopAdvertising()
    bleno.disconnect()
