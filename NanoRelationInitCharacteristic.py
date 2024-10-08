from pybleno import Characteristic
from Config import Config
from iBeacon import iBeacon_start

config = Config()

NANORELATION_INIT_SERVICE_UUID = config.NANORELATION_INIT_SERVICE_UUID
NANORELATION_INIT_CHARACTERISTIC_UUID = config.NANORELATION_INIT_CHARACTERISTIC_UUID
bleno = config.bleno


class NanoRelationInitCharacteristic(Characteristic):

    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': NANORELATION_INIT_CHARACTERISTIC_UUID,
            'properties': ['write', 'read'],
            'value': None
        })

        self._updateValueCallback = None

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        # バイトデータを文字列に変換（デコード）
        raw_data = data.decode('utf-8').split(',')

        # private_key = raw_data[0]
        # if not private_key:
        #     print('device private key is not found')
        #     callback(Characteristic.RESULT_UNLIKELY_ERROR)
        #     return
        # try:
        #     public_key = raw_data[1]
        # except IndexError:
        #     print('device public key is not found')
        #     callback(Characteristic.RESULT_UNLIKELY_ERROR)
        #     return
        # try:
        #     major = raw_data[2]
        # except IndexError:
        #     print('major is not found')
        #     callback(Characteristic.RESULT_UNLIKELY_ERROR)
        #     return
        # try:
        #     minor = raw_data[3]
        # except IndexError:
        #     print('minor is not found')
        #     callback(Characteristic.RESULT_UNLIKELY_ERROR)
        #     return

        # if not private_key or not public_key:
        #     print('device private key or public key is not found')
        #     callback(Characteristic.RESULT_UNLIKELY_ERROR)
        #     return
        major = raw_data[0]
        try:
            minor = raw_data[1]
        except IndexError:
            print('minor is not found')
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
            return
        if not major or not minor:
            print('major or minor is not found')
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
            return

        # config.set_PRIVATE_KEY(private_key)
        # config.set_PUBLIC_KEY(public_key)
        config.set_iBeacon_major(int(major))
        config.set_iBeacon_minor(int(minor))
        # print('device private key: ' + config.PRIVATE_KEY)
        # print('device public key: ' + config.PUBLIC_KEY)
        print('major: ' + str(config.iBeacon_major))
        print('minor: ' + str(config.iBeacon_minor))

        iBeacon_start()

        if withoutResponse:
            # クライアントはレスポンスを期待していないので、何もしない
            print("Write request without response")
        else:
            # クライアントがレスポンスを期待している場合は、正常終了を通知
            print("Write request with response")
            callback(Characteristic.RESULT_SUCCESS)

    def onReadRequest(self, offset, callback):
        device_id = config.generate_device_id()
        print('ApproachCharacteristic - onReadRequest')
        callback(result=Characteristic.RESULT_SUCCESS,
                 data=device_id.encode())
