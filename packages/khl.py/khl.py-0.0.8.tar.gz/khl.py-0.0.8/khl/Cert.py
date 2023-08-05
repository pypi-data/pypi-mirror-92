import base64
from enum import IntEnum

from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding

# https://pycryptodome.readthedocs.io/en/latest/src/installation.html


class Cert:
    """
    permission certification

    used in auth/data encrypt/decrypt
    """
    class Types(IntEnum):
        NOTSET = 0
        WS = 1
        WH = 2

    def __init__(self,
                 *,
                 type: Types = Types.NOTSET,
                 client_id: str,
                 client_secret: str,
                 token: str,
                 verify_token: str = '',
                 encrypt_key: str = ''):
        """
        all fields from bot config panel
        """
        if type != Cert.Types.NOTSET:
            self.type = type
        else:
            if verify_token:
                self.type = self.Types.WH
            else:
                self.type = self.Types.WS
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.verify_token = verify_token
        self.encrypt_key = encrypt_key

    def decrypt(self, data: bytes) -> str:
        """ decrypt data

        :param data: encrypted byte array
        :return: decrypted str
        """
        if not self.encrypt_key:
            return ''
        data = base64.b64decode(data)
        data = AES.new(key=self.encrypt_key.encode().ljust(32, b'\x00'),
                       mode=AES.MODE_CBC,
                       iv=data[0:16]).decrypt(base64.b64decode(data[16:]))
        data = Padding.unpad(data, 16)
        return data.decode('utf-8')
