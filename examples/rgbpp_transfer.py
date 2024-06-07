from io import BytesIO
from buidl.psbt import PSBT
from buidl.hd import HDPrivateKey
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
    network = "testnet"

    private_key = HDPrivateKey.from_seed(SEED, network=network)
    btc_address = private_key.child(0).p2wpkh_address()
    print(f'BTC P2WPKH Address: {btc_address}')

    response = rpc.generate_rgbpp_transfer_tx(params)
    btc_psbt_hex = response['btc_psbt_hex']
    ckb_virtual_tx_result = response['ckb_virtual_tx_result']

    psbt = PSBT.parse(BytesIO(bytes.fromhex(btc_psbt_hex)))
    psbt.tx_obj.network = network
    psbt.sign(private_key)
    btc_tx = psbt.final_tx()
    signed_tx_hex = btc_tx.serialize().hex()

    # Broadcast the signed transaction
    response = requests.post(BROADCAST_URL[network], data=signed_tx_hex) 

    if response.status_code == 200:
        print(f'Transaction broadcast successfully: {response.text}')
    else:
        print(f'Error broadcasting transaction: {response.text}')

    # Repost the ckb virtual tx and ckb tx id to the Queue Service
    rpc.report_rgbpp_ckb_tx_btc_txid({
        'ckb_virtual_tx_result': ckb_virtual_tx_result,
        'btc_tx_id': "btc_tx_id"
    })

    check_rgbpp_state("btc_tx_id")
    
    # Keep the script running
    while True:
        time.sleep(1)
  

transfer_rgbpp_on_btc({
    'xudt_type_args': '0xb14ad9ac44164d6fb09701f46e274c6607e33372f7f22930f4997930516bd5c9',
    'rgbpp_lock_args_list': ['0x010000006052b830ba09b72edb187a03789e1d6a26f8cb0fb6f1dffe956dd459fa0b8bd7'],
    'transfer_amount': hex(2000 * 10 ** 8),
    'from_btc_address': 'tb1qvt7p9g6mw70sealdewtfp0sekquxuru6j3gwmt',
    'to_btc_address': 'tb1qvt7p9g6mw70sealdewtfp0sekquxuru6j3gwmt'
})