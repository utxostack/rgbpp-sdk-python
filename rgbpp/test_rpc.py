from unittest import TestCase
from .rpc import rpc

class TestRpc(TestCase):
    def test_get_version(self):
        self.assertEqual(rpc.get_version(), "0.0.1")

    def test_generate_rgbpp_transfer_tx(self):
        request = {
            'xudt_type_args': '0xb14ad9ac44164d6fb09701f46e274c6607e33372f7f22930f4997930516bd5c9',
            'rgbpp_lock_args_list': ['0x010000006052b830ba09b72edb187a03789e1d6a26f8cb0fb6f1dffe956dd459fa0b8bd7'],
            'transfer_amount': hex(2000 * 10 ** 8),
            'from_btc_address': 'tb1qvt7p9g6mw70sealdewtfp0sekquxuru6j3gwmt',
            'to_btc_address': 'tb1qvt7p9g6mw70sealdewtfp0sekquxuru6j3gwmt'
        }
        print('request: ', request)
        response = rpc.generate_rgbpp_transfer_tx(request)
        print('response: ', response)
