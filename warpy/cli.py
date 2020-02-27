import datetime
import os
from base64 import b64encode

import requests
from nacl.bindings import crypto_scalarmult_base

from warpy.utils import generate_string, conf


class WarpPlus:

    @staticmethod
    def generate_key():
        private_key = os.urandom(32)
        public_key = crypto_scalarmult_base(private_key)
        return b64encode(private_key).decode('utf-8'), b64encode(public_key).decode('utf-8')

    def enable_warp(self, config):
        data = {"warp_enabled": True}
        url = 'https://api.cloudflareclient.com/v0a745/reg/' + config['id']
        headers = {"Accept-Encoding": "gzip",
                   "User-Agent": "okhttp/3.12.1",
                   "Authorization": "Bearer {}".format(config['token']),
                   "Content-Type": "application/json; charset=UTF-8"}
        req = requests.patch(url, json=data, headers=headers)
        req.raise_for_status()
        req = req.json()
        assert req["warp_enabled"] is True

    def register(self, key=None, referrer=None):

        url = 'https://api.cloudflareclient.com/v0a745/reg'

        headers = {'Content-Type': 'application/json; charset=UTF-8',
                   'Host': 'api.cloudflareclient.com',
                   'Connection': 'Keep-Alive',
                   'Accept-Encoding': 'gzip',
                   'User-Agent': 'okhttp/3.12.1'}

        install_id = generate_string(11)
        key = key if key else self.generate_key()
        data = {"key": key[1],
                "install_id": install_id,
                "fcm_token": "{}:APA91b{}".format(install_id, generate_string(134)),
                "referrer": referrer or "",
                "warp_enabled": True,
                "tos": datetime.datetime.now().isoformat()[:-3] + "+07:00",
                "type": "Android",
                "locale": "en-GB"}

        req = requests.post(url, headers=headers, json=data)
        if req.status_code != 200:
            return {}
        req_json = dict(req.json())
        req_json['key'] = {"public_key": req_json['config']['peers'][0]['public_key'], "private_key": key[0]}
        return req_json

    @staticmethod
    def get_info(ID, token):
        url = 'https://api.cloudflareclient.com/v0i1909221500/reg/' + ID.strip()
        headers = {"Authorization": "Bearer " + token.strip()}
        req = requests.get(url, headers=headers)
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
