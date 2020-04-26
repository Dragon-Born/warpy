import random
import string
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_
import ssl

CIPHERS = (
    'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:'
    'ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA'
)

conf = '''
[Interface]
PrivateKey = {private_key}
Address = {address}
DNS = 1.1.1.1
[Peer]
PublicKey = {public_key}
Endpoint = {endpoint}
AllowedIPs = 0.0.0.0/0'''


class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options,
                                          ssl_version=ssl.PROTOCOL_TLSv1_1)
        self.poolmanager = PoolManager(*pool_args,
                                       ssl_context=ctx,
                                       **pool_kwargs)


class Colored:
    HEADER = '\033[43;40m'
    PINK = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW = '\033[33;1m'


def generate_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
