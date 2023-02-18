import base64
import hashlib
import json
from datetime import datetime, timedelta
import re


class JWToken:

    def __init__(self, head, payl, sig):
        self.header = head
        self.payload = payl
        self.signature = sig

    @staticmethod
    def generate_jw_token(header, payload, secret, validity=7):
        if validity < 1:
            raise Exception("Validity should be 1 day or higher!")
        now = datetime.now()
        payload["iat"] = now.timestamp()
        payload["exp"] = (now + timedelta(days=validity)).timestamp()
        header_encoded = JWToken.b64_encode(json.dumps(header).encode('utf-8'))
        payload_encoded = JWToken.b64_encode(json.dumps(payload).encode('utf-8'))
        signature = JWToken.generate(header_encoded, payload_encoded, secret)
        signature = JWToken.b64_encode(signature)
        return JWToken(header_encoded, payload_encoded, signature)

    @staticmethod
    def generate(header_encoded, payload_encoded, secret):
        secret_encoded = JWToken.b64_encode(secret.encode('utf-8'))
        message = f"{header_encoded}.{payload_encoded}".encode('utf-8')
        return hashlib.sha256(secret_encoded + message).digest()

    def check_token_signature(self, secret):
        return JWToken.b64_encode(JWToken.generate(self.header, self.payload, secret)) == self.signature

    def is_expired(self):
        payload = self.read_payload()
        now = datetime.now()
        return payload["exp"] < now.timestamp()

    @staticmethod
    def is_valid(token):
        return bool(re.match('^[a-zA-Z0-9\-\_\=]+\.[a-zA-Z0-9\-\_\=]+\.[a-zA-Z0-9\-\_\=]+$', token))

    def __str__(self):
        return f"{self.header}.{self.payload}.{self.signature}"

    @staticmethod
    def token_from_string(token):
        if JWToken.is_valid(token):
            token_exploded = token.split(".")
            return JWToken(token_exploded[0], token_exploded[1], token_exploded[2])
        return None

    @staticmethod
    def b64_encode(data):
        # 1 - Encode in base64 the data (payload or header)
        # 2 - Replace + to - & / to _ with strtr (Not in JWT chart)
        # 3 - Remove the "=" with trim (Not in JWT chart)
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode('utf-8')

    def read_header(self):
        return json.loads(base64.urlsafe_b64decode(self.header + '==').decode('utf-8'))

    def read_payload(self):
        return json.loads(base64.urlsafe_b64decode(self.payload + '==').decode('utf-8'))
