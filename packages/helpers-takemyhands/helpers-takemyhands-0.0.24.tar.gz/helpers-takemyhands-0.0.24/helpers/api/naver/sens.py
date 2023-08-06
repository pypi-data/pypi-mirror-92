import base64
import hashlib
import hmac
import json
import requests
import time
from ...python.dict.utils import dict_get_or_raise_error
from ...python.converter import string_to_bytearray

class SensManager:

    """ Ncloud SENS Manager Definition """

    def __init__(self, **kwargs):
        # Init first more then others
        self.need_message = "SensManager need initialization this value."
        self.time_stamp = int(float(time.time()) * 1000)

        # client
        self.app_name = dict_get_or_raise_error(kwargs, "app_name", self.need_message)

        # calling number
        self.calling_number = dict_get_or_raise_error(
            kwargs, "calling_number", self.need_message
        )

        # keys
        self.service_id = dict_get_or_raise_error(
            kwargs, "service_id", self.need_message
        )
        self.account_key_id = dict_get_or_raise_error(
            kwargs, "account_key_id", self.need_message
        )
        self.account_secret_key = string_to_bytearray(
            dict_get_or_raise_error(kwargs, "account_secret_key", self.need_message)
        )

        # options
        self.request_uri = f"/sms/v2/services/{self.service_id}/messages"
        self.request_url = f"https://sens.apigw.ntruss.com{self.request_uri}"

    def create_signature(self):
        hash_str = f"POST {self.request_uri}\n{self.time_stamp}\n{self.account_key_id}"

        digest = hmac.new(
            self.account_secret_key,
            msg=hash_str.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()

        return base64.b64encode(digest).decode()

    def create_headers(self):
        return {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": str(self.time_stamp),
            "x-ncp-iam-access-key": self.account_key_id,
            "x-ncp-apigw-signature-v2": self.create_signature(),
        }

    def create_bodies_for_cert(self, phone_number, code):
        message = f"[{self.app_name}] 인증 번호 [{code}]를 입력해주세요."

        return {
            "code": code,
            "type": "SMS",
            "countryCode": "82",
            "from": self.calling_number,
            "contentType": "COMM",
            "content": message,
            "messages": [{"to": phone_number}],
        }

    def send_for_cert(self, phone_number, code):
        header = self.create_headers()
        body = self.create_bodies_for_cert(phone_number, code)

        res = requests.post(
            self.request_url,
            headers=header,
            data=json.dumps(body),
        )

        if res.status_code == 202:
            return {"results": body}
        else:
            return {"results": "Something is wrong."}

    def create_bodies_for_message(self, phone_number, message):
        message = f"[{self.app_name}] {message}"

        results = {
            "type": "SMS",
            "countryCode": "82",
            "from": self.calling_number,
            "contentType": "COMM",
            "content": message,
            "messages": [{"to": phone_number}],
        }

        return results

    def send_message(self, phone_number, message):
        header = self.create_headers()
        body = self.create_bodies_for_message(phone_number, message)

        res = requests.post(
            self.request_url,
            headers=header,
            data=json.dumps(body),
        )

        if res.status_code == 202:
            return {"results": body}
        else:
            return {"results": "Something is wrong."}
