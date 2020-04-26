import datetime
import os
import ssl
from base64 import b64encode

import requests
from nacl.bindings import crypto_scalarmult_base

from warpy.utils import generate_string, conf, TlsAdapter

api_version = "v0a884"

session = requests.session()
adapter = TlsAdapter()
session.mount("https://", adapter)


class WarpPlus:

    @staticmethod
    def generate_key():
        private_key = os.urandom(32)
        public_key = crypto_scalarmult_base(private_key)
        return b64encode(private_key).decode('utf-8'), b64encode(public_key).decode('utf-8')

    def enable_warp(self, config):
        data = {"warp_enabled": True}
        url = 'https://api.cloudflareclient.com/' + api_version + '/reg/' + config['id']
        headers = {"Accept-Encoding": "gzip",
                   "User-Agent": "okhttp/3.12.1",
                   "Authorization": "Bearer {}".format(config['token']),
                   "Content-Type": "application/json; charset=UTF-8"}
        req = session.request("PATCH", url, json=data, headers=headers)
        req.raise_for_status()
        req = req.json()
        assert req["warp_enabled"] is True

    def register(self, key=None, referrer=None):

        url = 'https://api.cloudflareclient.com/' + api_version + '/reg'

        headers = {"User-Agent": "okhttp/3.12.1",
                   "Content-Type": "application/json; charset=UTF-8"}

        install_id = generate_string(11)
        key = key if key else self.generate_key()
        data = {"key": key[1],
                "install_id": "",
                "fcm_token": "",
                "referrer": referrer or "",
                "warp_enabled": True,
                "tos": datetime.datetime.now().isoformat()[:-7] + "Z",
                "model": "",
                "type": "Android",
                "locale": "en_US"}
        req = session.post(url, headers=headers, json=data)
        if req.status_code != 200:
            return {}
        req_json = dict(req.json())
        req_json['key'] = {"public_key": req_json['config']['peers'][0]['public_key'], "private_key": key[0]}
        return req_json

    @staticmethod
    def get_info(ID, token):
        url = 'https://api.cloudflareclient.com/' + api_version + '/reg/' + ID.strip()
        headers = {"Authorization": "Bearer " + token.strip()}
        req = session.request("GET", url, headers=headers)
        if req.status_code != 200:
            raise Exception(req.text)
        return req.json()

    @staticmethod
    def export_to_wireguard(config):
        conf_text = conf.format(private_key=config['key']['private_key'],
                                public_key=config['config']['peers'][0]['public_key'],
                                address=config['config']['interface']['addresses']['v4'],
                                endpoint=config['config']['peers'][0]['endpoint']['host'])
        return conf_text

    def increase_quota(self, config):
        return self.register(referrer=config['id'])
