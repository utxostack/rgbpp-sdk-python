from io import BytesIO
from buidl.psbt import PSBT, serialize_binary_path, NamedHDPublicKey
from buidl.hd import HDPrivateKey
from buidl.helper import encode_varstr
import requests
import threading
import time

from rgbpp.types import RgbppTransferReq, Hex
from rgbpp.rpc import rpc

# API endpoint for broadcasting transactions
BROADCAST_URL = {
    "mainnet": "https://blockstream.info/api",
    "testnet": "https://blockstream.info/testnet/api",
    "signet": "https://mempool.space/signet/api",
}
SEED = b'Hello RGB++'

def check_rgbpp_state(btc_tx_id: Hex):
    print(f"Checking RGB++ state is running at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    response = rpc.get_rgbpp_tx_state({
        'btc_tx_id': btc_tx_id
    })
    state = response["state"]

    if (state != "completed" and state != 'failed'):
        # Schedule the task to run again after 30 seconds
        threading.Timer(30, check_rgbpp_state).start()
    elif (state == "completed"):
        ckb_tx_hash = rpc.get_rgbpp_ckb_tx_hash({'btc_tx_id': btc_tx_id})
        print(f"RGB++ assets have been completed and CKB tx hash: {ckb_tx_hash}")
    else:
        print(f"RGB++ assets have been failed and the reason is {response["failed_reason"]}")
    

# Warning: The example is not ready which inlcudes todo list to be resolved
def transfer_rgbpp_on_btc(params: RgbppTransferReq):
    network = "signet"

    response = rpc.generate_rgbpp_transfer_tx(params)
    btc_psbt_hex = response['btc_psbt_hex']
    ckb_virtual_tx_result = response['ckb_virtual_tx_result']

    print(f'btc_psbt_hex: {btc_psbt_hex}')

    psbt = PSBT.parse(BytesIO(bytes.fromhex(btc_psbt_hex)))
    psbt.tx_obj.network = network

    tx_lookup = psbt.tx_obj.get_input_tx_lookup()
    hd_key = HDPrivateKey.from_seed(SEED, network=network).child(0)
    stream = BytesIO(
        encode_varstr(hd_key.fingerprint() + serialize_binary_path("m/44'/1'/0'"))
    )
    hd = NamedHDPublicKey.parse(hd_key, stream)
    psbt.update(tx_lookup, hd.bip44_lookup())

    btc_address = hd_key.p2wpkh_address()
    print(f'BTC P2WPKH Address: {btc_address}')

    signed = psbt.sign(hd_key)
    print(f'signed: {signed}')
    # psbt.finalize()

    # print(f'PSBT BTC TX: {psbt.tx_obj}')

    # btc_tx = psbt.final_tx()

    # signed_tx_hex = btc_tx.serialize().hex()

    # # Broadcast the signed transaction
    # response = requests.post(BROADCAST_URL[network], data=signed_tx_hex) 

    # if response.status_code == 200:
    #     print(f'Transaction broadcast successfully: {response.text}')
    # else:
    #     print(f'Error broadcasting transaction: {response.text}')

    # # Repost the ckb virtual tx and ckb tx id to the Queue Service
    # rpc.report_rgbpp_ckb_tx_btc_txid({
    #     'ckb_virtual_tx_result': ckb_virtual_tx_result,
    #     'btc_tx_id': "btc_tx_id"
    # })

    # check_rgbpp_state("btc_tx_id")
    
    # # Keep the script running
    # while True:
    #     time.sleep(1)
  

transfer_rgbpp_on_btc({
    'xudt_type_args': '0x562e4e8a2f64a3e9c24beb4b7dd002d0ad3b842d0cc77924328e36ad114e3ebe',
    'rgbpp_lock_args_list': ['0x000000003df7c4e1e9a6c366d8d8b45390025e28c515254f1fd24f189e53d45534d37707'],
    'transfer_amount': hex(800 * 10 ** 8),
    'from_btc_address': 'tb1qh65mw2nq9l4647ddga83fhmted3deeq5398axk',
    'to_btc_address': 'tb1qh65mw2nq9l4647ddga83fhmted3deeq5398axk'
})