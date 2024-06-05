import os
import requests
import jsonrpcclient

from .types import RgbppTransferReq, RgbppTransferResp, Version, RgbppTxStateReq

DEFAULT_ENDPOINT = os.environ.get('RGBPP_SDK_SERVICE_URL', 'http://127.0.0.1:3000/json-rpc')


class RPCClient:
    def __init__(self, endpoint: str = DEFAULT_ENDPOINT):
        self.endpoint = endpoint

    def request(self, method: str, *args):
        payload = jsonrpcclient.request(method, params=tuple(args))
        response = requests.post(self.endpoint, json=payload)

        parsed = jsonrpcclient.parse(response.json())
        if isinstance(parsed, jsonrpcclient.Ok):
            return parsed.result
        else:
            raise Exception(parsed.message)

    def generate_rgbpp_transfer_tx(self, params: RgbppTransferReq) -> RgbppTransferResp:
        return self.request('generate_rgbpp_transfer_tx', params)
    
    def get_rgbpp_tx_state(self, params: RgbppTxStateReq) -> RgbppTxStateReq:
        return self.request('get_rgbpp_tx_state', params)

    def get_version(self) -> Version:
        return self.request('get_version')


rpc = RPCClient()