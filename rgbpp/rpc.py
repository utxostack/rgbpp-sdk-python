import os
import requests
import jsonrpcclient

from .types import Hex, RgbppTransferReq, RgbppTransferResp, Version, RgbppTxStateReq, RgbppTxStateResp, RgbppTxReportReq, RgbppCkbTxHashReq, BtcTxSendReq, RgbppGroupTxsReq, RgbppGroupTxsResp, RgbppTransferAllReq, RgbppTransferAllResp

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

    def generate_rgbpp_transfer_all_txs(self, params: RgbppTransferAllReq) -> RgbppTransferAllResp:
        return self.request('generate_rgbpp_transfer_all_txs', params)
    
    def report_rgbpp_ckb_tx_btc_txid(self, params: RgbppTxReportReq) -> RgbppTxStateResp:
        return self.request('report_rgbpp_ckb_tx_btc_txid', params)
    
    def get_rgbpp_tx_state(self, params: RgbppTxStateReq) -> RgbppTxStateResp:
        return self.request('get_rgbpp_tx_state', params)
    
    def get_rgbpp_ckb_tx_hash(self, params: RgbppCkbTxHashReq) -> Hex:
        return self.request('get_rgbpp_ckb_tx_hash', params)

    def send_btc_transaction(self, params: BtcTxSendReq) -> Hex:
        return self.request('send_btc_transaction', params)

    def send_rgbpp_group_txs(self, params: RgbppGroupTxsReq) -> RgbppGroupTxsResp:
        return self.request('send_rgbpp_group_txs', params)

    def get_version(self) -> Version:
        return self.request('get_version')


rpc = RPCClient()