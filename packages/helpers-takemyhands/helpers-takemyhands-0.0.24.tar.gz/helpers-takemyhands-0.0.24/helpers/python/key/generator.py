import secrets
import random
import string


class Generator:
    def generate_by_url(self, length):
        return secrets.token_urlsafe(length)

    def generate_by_hex(self, length):
        return secrets.token_hex(length)

    def generate_by_string(self, length):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(length))
