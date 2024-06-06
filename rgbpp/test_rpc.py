import json

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
        response = rpc.generate_rgbpp_transfer_tx(request)
        # print('response: ', response)
        self.assertEqual(len(response["btc_psbt_hex"]) > 10, True)

        data = json.loads(response["ckb_virtual_tx_result"])
        self.assertEqual(data["ckbRawTx"]["version"], "0x0")

    def test_report_rgbpp_ckb_tx_btc_txid(self):
        request = {
            'ckb_virtual_tx_result': '{"ckbRawTx":{"version":"0x0","cellDeps":[{"outPoint":{"txHash":"0xf1de59e973b85791ec32debbba08dff80c63197e895eb95d67fc1e9f6b413e00","index":"0x0"},"depType":"code"},{"outPoint":{"txHash":"0xf1de59e973b85791ec32debbba08dff80c63197e895eb95d67fc1e9f6b413e00","index":"0x1"},"depType":"code"},{"outPoint":{"txHash":"0xbf6fb538763efec2a70a6a3dcb7242787087e1030c4e7d86585bc63a9d337f5f","index":"0x0"},"depType":"code"},{"outPoint":{"txHash":"0xf8de3bb47d055cdf460d93a2a6e1b05f7432f9777c8c474abf4eec1d4aee5d37","index":"0x0"},"depType":"depGroup"}],"headerDeps":[],"inputs":[{"previousOutput":{"txHash":"0x4cef44a6e03819322e826c85ec891f556c7ce6e9fab8155af953c13d0bffbfbf","index":"0x0"},"since":"0x0"}],"outputs":[{"lock":{"codeHash":"0x61ca7a4796a4eb19ca4f0d065cb9b10ddcf002f10f7cbb810c706cb6bb5c3248","hashType":"type","args":"0x010000000000000000000000000000000000000000000000000000000000000000000000"},"type":{"codeHash":"0x25c29dc317811a6f6f3985a7a9ebc4838bd388d19d0feeecf0bcd60f6c0975bb","hashType":"type","args":"0xb14ad9ac44164d6fb09701f46e274c6607e33372f7f22930f4997930516bd5c9"},"capacity":"0x5e9f52db8"},{"lock":{"codeHash":"0x61ca7a4796a4eb19ca4f0d065cb9b10ddcf002f10f7cbb810c706cb6bb5c3248","hashType":"type","args":"0x020000000000000000000000000000000000000000000000000000000000000000000000"},"type":{"codeHash":"0x25c29dc317811a6f6f3985a7a9ebc4838bd388d19d0feeecf0bcd60f6c0975bb","hashType":"type","args":"0xb14ad9ac44164d6fb09701f46e274c6607e33372f7f22930f4997930516bd5c9"},"capacity":"0x5e9f53e00"}],"outputsData":["0x00d0ed902e0000000000000000000000","0x007019c9c17507000000000000000000"],"witnesses":["0xFF"]},"commitment":"df644812e2cb679c6ab712652eb642cf42837bba7aa38012929ece451b0fb861","needPaymasterCell":true,"sumInputsCapacity":"0x5e9f52db8"}',
            'btc_tx_id': 'fb4ebf0f4f9c9fc32b22c89cac7eccd7364d013f4a0422e402c70839c70339ca'
        }
        response = rpc.report_rgbpp_ckb_tx_btc_txid(request)
        self.assertEqual(response["state"], "completed")

    def test_get_rgbpp_tx_state(self):
        request = {
            'btc_tx_id': 'fb4ebf0f4f9c9fc32b22c89cac7eccd7364d013f4a0422e402c70839c70339ca',
            'params': {
                'with_data': True
            }
        }
        response = rpc.get_rgbpp_tx_state(request)
        self.assertEqual(response["state"], "completed")
        # See the response of the API https://btc-assets-api.testnet.mibao.pro/docs/static/index.html#/RGB%2B%2B/get_rgbpp_v1_transaction__btc_txid__job
        self.assertEqual(response["data"]["ckbVirtualResult"]["ckbRawTx"]["version"], "0x0")
