from django.db import models
from hashlib import sha3_512, pbkdf2_hmac
from django.contrib import admin
from secrets import token_bytes
from binascii import b2a_base64
import datetime
import pytz
# Create your models here.

# TODO enable validation | done


class Account(models.Model):
    username = models.CharField(max_length=32)
    passw_hash = models.BinaryField(max_length=64)
    passw_salt = models.BinaryField(max_length=24)

    def __str__(self) -> str:
        return self.username

    def setpass(self, passwd):
        self.passw_salt = token_bytes(24)
        self.passw_hash = pbkdf2_hmac(
            'sha512', passwd.encode(), self.passw_salt, 100000)

    def checkpass(self, passwd):
        return pbkdf2_hmac('sha512', passwd.encode(), self.passw_salt, 100000) == self.passw_hash

# TODO make sessions expire | done


class Session(models.Model):
    identifier = models.BinaryField(max_length=64)
    K2 = models.BinaryField(max_length=64)
    K3 = models.BinaryField(max_length=64)
    validuntil = models.DateTimeField(default=datetime.datetime.today())
    def initialize(self):
        self.identifier = token_bytes(64)
        K1 = token_bytes(64)
        self.K2 = token_bytes(64)
        self.K3 = sha3_512(K1+self.K2).digest()
        self.validuntil = pytz.UTC.localize(datetime.datetime.today() + datetime.timedelta(days=1))
        return {'key': K1, 'id': self.identifier}

    def validate(self, K1):
        if  pytz.UTC.localize(datetime.datetime.today()) > self.validuntil:
            self.delete()
            return False
        return sha3_512(K1+self.K2).digest() == self.K3

    def __str__(self):
        return b2a_base64(self.identifier).decode()
