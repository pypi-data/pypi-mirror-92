import jwt
from jwcrypto.jwt import JWK
from django.conf import settings
from revauth.settings import api_settings
import requests
import json
from revauth import exceptions
from revjwt import decode


class BaseCryptor:
    pub_key = settings.PUB_KEY
    audience = settings.CLIENT_ID
    API_KEY = settings.CLIENT_SECRET
    STAGE = settings.STAGE
    VERSION = api_settings.AUTH_VERSION

    @property
    def api_host(self):
        if self.STAGE != 'prod':
            return 'https://auth-stg.revtel-api.com/' + self.VERSION
        return 'https://auth.revtel-api.com/' + self.VERSION

    def decode(self, token):
        return decode(token, audience=self.audience, algorithms=['RS256'])

    def _post(self, path, data):
        headers = {'x-api-key': self.API_KEY, 'Content-Type': 'application/json'}
        resp = requests.post(f'{self.api_host}{path}', json=data, headers=headers)
        return resp


class JWTCryptor(BaseCryptor):
    def __init__(self, headers=None, unverified=None):
        pass

    def decode_register(self, token):
        decoded = self.decode(token)
        if decoded['typ'] != 'register':
            raise exceptions.RegisterDecodeTypeError
        return decoded

    def encode(self, data):
        path = '/jwt/server/encode'
        resp = self._post(path, data)
        return resp.json()


class GoogleCryptor(BaseCryptor):
    audience = api_settings.GOOGLE_CLIENT_ID

    def __init__(self, headers):
        kid = headers['kid']
        keys = requests.get('https://www.googleapis.com/oauth2/v3/certs').json()['keys']
        key = [k for k in keys if k['kid'] == kid][0]
        key = JWK.from_json(json.dumps(key))
        self.pub_key = key.export_to_pem()


class AppleCryptor(BaseCryptor):
    audience = api_settings.APPLE_CLIENT_ID

    def __init__(self, headers):
        kid = headers['kid']
        keys = requests.get('https://appleid.apple.com/auth/keys').json()['keys']
        key = [k for k in keys if k['kid'] == kid][0]
        key = JWK.from_json(json.dumps(key))
        self.pub_key = key.export_to_pem()
