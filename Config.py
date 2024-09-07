from pybleno import Bleno
import random
import string


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

            self._bleno = Bleno()

            self._NANORELATION_INIT_SERVICE_UUID = 'AAAAAAAA-8883-49A8-8BDB-42BC1A7107F4'
            self._NANORELATION_INIT_CHARACTERISTIC_UUID = 'BBBBBBBB-201F-44EB-82E8-10CC02AD8CE1'

            self._DEVICE_ID = ''
            self._PRIVATE_KEY = ''
            self._PUBLIC_KEY = ''

    # bleno
    @property
    def bleno(self):
        return self._bleno

    # NANORELATION_INIT_SERVICE_UUID
    @property
    def NANORELATION_INIT_SERVICE_UUID(self):
        return self._NANORELATION_INIT_SERVICE_UUID

    # NANORELATION_INIT_CHARACTERISTIC_UUID
    @property
    def NANORELATION_INIT_CHARACTERISTIC_UUID(self):
        return self._NANORELATION_INIT_CHARACTERISTIC_UUID

    # DEVICE_ID
    @property
    def DEVICE_ID(self):
        return self._DEVICE_ID

    def generate_device_id(self):
        self._DEVICE_ID = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=20))
        return self._DEVICE_ID

    # PRIVATE_KEY
    @property
    def PRIVATE_KEY(self):
        return self._PRIVATE_KEY

    def set_PRIVATE_KEY(self, private_key):
        self._PRIVATE_KEY = private_key

    # PUBLIC_KEY
    @property
    def PUBLIC_KEY(self):
        return self._PUBLIC_KEY

    def set_PUBLIC_KEY(self, public_key):
        self._PUBLIC_KEY = public_key
