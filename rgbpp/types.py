from typing import NewType, Sequence

from typing_extensions import TypedDict

Hex = NewType('Hex', str)
Version = NewType('Version', str)
BtcAddress = NewType('BtcAddress', str)
Json = NewType('Json', str)

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
