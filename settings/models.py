import base64
import os
import hashlib

from tortoise import fields, timezone, Model


class User(Model):
    username = fields.CharField(max_length=100, unique=True, blank=False, null=False)
    password = fields.TextField(blank=False, null=False)
    salt = fields.BinaryField(blank=False, null=False)
    admin = fields.BooleanField(null=False, default=False)
    created = fields.DatetimeField(default=timezone.now, null=False)
    last_successful_login = fields.DatetimeField(default=None, null=True)
    last_failed_login = fields.DatetimeField(default=None, null=True)
    failed_login_count = fields.IntField(default=0, null=False)

    async def generate_salt(self):
        salt = os.urandom(128)
        self.salt = salt
        return True

    async def set_password(self, password):
        if self.salt is None:
            await self.generate_salt()
        m = hashlib.sha256()
        m.update(password.encode('utf-8'))
        m.update(self.salt)
        self.password = m.hexdigest()
        return True

    async def check_password(self, password):
        m = hashlib.sha256()
        m.update(password.encode('utf-8'))
        m.update(self.salt)
        if self.password == m.hexdigest():
            return True
        else:
            return False