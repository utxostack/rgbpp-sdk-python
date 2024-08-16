from typing import NewType, Sequence, Optional

from typing_extensions import TypedDict

Hex = NewType('Hex', str)
Version = NewType('Version', str)
BtcAddress = NewType('BtcAddress', str)
Json = NewType('Json', str)
# 'completed' | 'failed' | 'delayed' | 'active' | 'waiting'
State = NewType('State', str)
PubkeyPair = NewType('PubkeyPair', dict[str, str])

RgbppTransferReq = TypedDict('RgbppTransferReq', {
    'xudt_type_args': Hex,
    'rgbpp_lock_args_list': Sequence[Hex],
    'transfer_amount': Hex,
    'from_btc_address': BtcAddress,
    'to_btc_address': BtcAddress,
})

RgbppTransferResp = TypedDict('RgbppTransferResp', {
    'ckb_virtual_tx_result': Json,
    'btc_psbt_hex': Hex,
})

RgbppTxReportReq = TypedDict('RgbppTxReportReq', {
    'ckb_virtual_tx_result': Json,
    'btc_tx_id': Hex
})

RgbppTxStateParams = TypedDict('RgbppTxStateParams', {
    'with_data': bool,
})

RgbppTxStateReq = TypedDict('RgbppTxStateReq', {
    'btc_tx_id': Hex,
    'params': Optional[RgbppTxStateParams]
})

RgbppTxStateResp = TypedDict('RgbppTxStateResp', {
    'state': State,
    'failed_reason': Optional[str],
    'data': Json
})

RgbppCkbTxHashReq = TypedDict('RgbppCkbTxHashReq', {
    'btc_tx_id': Hex,
})

BtcTxSendReq = TypedDict('BtcTxSendReq', {
    'tx_hex': Hex
})

RgbppTransferAllCkb = TypedDict('RgbppTransferAllCkb', {
    'xudt_type_args': Hex,
    'fee_rate': Hex
})

RgbppTransferAllBtc = TypedDict('RgbppTransferAllBtc', {
    'asset_addresses': Sequence[BtcAddress],
    'from_address': BtcAddress,
    'to_address': BtcAddress,
    'from_pubkey': Optional[Hex],
    'pubkey_map': Optional[Sequence[PubkeyPair]],
    'change_address': Optional[BtcAddress],
    'fee_rate': Optional[int]
})

RgbppTransferAllReq = TypedDict('RgbppTransferAllReq', {
    'ckb': RgbppTransferAllCkb,
    'btc': RgbppTransferAllBtc,
})

RgbppTransferAllRet = TypedDict('RgbppTransferAllRet', {
    'ckb_virtual_tx_result': Json,
    'psbt_hex': Hex,
    'btc_fee_rate': int,
    'btc_fee': int,
})
RgbppTransferAllResp = NewType('RgbppTransferAllResp', Sequence[RgbppTransferAllRet])


RgbppGroupTxsParam = TypedDict('RgbppGroupTxsReq', {
    'ckb_virtual_tx_result': Json,
    'btc_tx_hex': Hex,
})
RgbppGroupTxsReq = NewType('RgbppGroupTxsReq', Sequence[RgbppGroupTxsParam])

RgbppGroupTxsRet = TypedDict('RgbppGroupTxsRet', {
    'btc_tx_id': Hex,
    'error': Hex,
})
RgbppGroupTxsResp = NewType('RgbppGroupTxsResp', Sequence[RgbppGroupTxsRet])

RgbppTxStateResp = TypedDict('RgbppTxStateResp', {
    'state': State,
    'failed_reason': Optional[str],
    'data': Json
})
