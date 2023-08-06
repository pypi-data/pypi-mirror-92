# -*- coding: utf-8 -*-
import datetime
import json
import hashlib
import hmac
from base64 import urlsafe_b64encode
import os
import secrets

from M2Crypto import EVP

class Multipass:
    def __init__(self, secret):
        key = hashlib.sha256(secret.encode()).digest()
        self.encryptionKey = key[0:16]
        self.signatureKey = key[16:32]

    def generateToken(self, customerDataHash):
        customerDataHash['created_at'] = datetime.datetime.utcnow().isoformat()
        cipherText = self.encrypt(json.dumps(customerDataHash))
        return urlsafe_b64encode(cipherText + self.sign(cipherText))

    def generateURL(self, customerDataHash, url):
        token = self.generateToken(customerDataHash).decode('utf-8')
        return '{0}/account/login/multipass/{1}'.format(url, token)

    def encrypt(self, plainText):
        iv = os.urandom(16)
        cipher = EVP.Cipher(alg='aes_128_cbc', key=self.encryptionKey, iv=iv, op=1)
        cipherText = cipher.update(plainText.encode())
        cipherText += cipher.final()
        return iv + cipherText

    def sign(self, message):
        return hmac.new(self.signatureKey, message, hashlib.sha256).digest()
