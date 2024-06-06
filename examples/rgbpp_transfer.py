from rgbpp.types import RgbppTransferReq
from rgbpp.rpc import rpc

# Warning: The example is not ready which inlcudes todo list to be resolved
def transfer_rgbpp_on_btc(params: RgbppTransferReq):
  response = rpc.generate_rgbpp_transfer_tx(params)
  btc_psbt_hex = response['btc_psbt_hex']
  ckb_virtual_tx_result = response['ckb_virtual_tx_result']

  # TODO: pseudocode
  # psbt = PSBT.from_hex(btcPsbtHex)
  # psbt.sign_all_inputs(btc_key_pair);
  # psbt.finalize_all_inputs();
  # const btcTx = psbt.extractTransaction();
  # btc_tx_id = btc_service.send_btc_transaction(psbt.extract_transaction().to_hex());

  # Repost the ckb virtual tx and ckb tx id to the Queue Service
  rpc.report_rgbpp_ckb_tx_btc_txid({
      'ckb_virtual_tx_result': ckb_virtual_tx_result,
      'btc_tx_id': "btc_tx_id"
  })

  # TODO: Query the RGB++ transaction state from the Queue Service
  response = rpc.get_rgbpp_tx_state({
      'btc_tx_id': "btc_tx_id"
  })
  

transfer_rgbpp_on_btc({
    'xudt_type_args': '0xb14ad9ac44164d6fb09701f46e274c6607e33372f7f22930f4997930516bd5c9',
    'rgbpp_lock_args_list': ['0x010000006052b830ba09b72edb187a03789e1d6a26f8cb0fb6f1dffe956dd459fa0b8bd7'],
    'transfer_amount': hex(2000 * 10 ** 8),
    'from_btc_address': 'tb1qvt7p9g6mw70sealdewtfp0sekquxuru6j3gwmt',
    'to_btc_address': 'tb1qvt7p9g6mw70sealdewtfp0sekquxuru6j3gwmt'
})