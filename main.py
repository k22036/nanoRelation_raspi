import random
import string
import time
from pybleno import *

bleno = Bleno()

NANORELATION_INIT_SERVICE_UUID = 'AAAAAAAA-8883-49A8-8BDB-42BC1A7107F4'
NANORELATION_INIT_CHARACTERISTIC_UUID = 'BBBBBBBB-201F-44EB-82E8-10CC02AD8CE1'

DEVICE_ID = ''
PRIVATE_KEY = ''
PUBLIC_KEY = ''


class NanoRelationInitCharacteristic(Characteristic):

    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': NANORELATION_INIT_CHARACTERISTIC_UUID,
            'properties': ['write', 'read'],
            'value': None
        })

        self._updateValueCallback = None

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        global PRIVATE_KEY, PUBLIC_KEY
        # バイトデータを文字列に変換（デコード）
        raw_data = data.decode('utf-8').split(',')
        PRIVATE_KEY = raw_data[0]
        try:
            PUBLIC_KEY = raw_data[1]
        except IndexError:
            print('device public key is not found')
            callback(Characteristic.RESULT_UNLIKELY_ERROR)

        print('device private key: ' + PRIVATE_KEY)
        print('device public key: ' + PUBLIC_KEY)

        if withoutResponse:
            # クライアントはレスポンスを期待していないので、何もしない
            print("Write request without response")
        else:
            # クライアントがレスポンスを期待している場合は、正常終了を通知
            callback(Characteristic.RESULT_SUCCESS)

    def onReadRequest(self, offset, callback):
        global DEVICE_ID
        DEVICE_ID = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=20))
        print('ApproachCharacteristic - onReadRequest')
        callback(result=Characteristic.RESULT_SUCCESS,
                 data=DEVICE_ID.encode())


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
