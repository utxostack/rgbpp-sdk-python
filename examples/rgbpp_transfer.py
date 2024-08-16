from io import BytesIO
from buidl import HDPrivateKey, NamedHDPublicKey, PSBT, read_varstr
import requests
import threading
import time

from rgbpp.types import RgbppTransferReq, Hex
from rgbpp.rpc import rpc

INTERVAL_TIME_SECONDS = 30
# Please use your own BTC seed to generate private key
SEED = b'Hello RGB++'

# Please make sure you have enough BTC and RGB++ Assets, the example is only for RGB++ transfer on BTC.
# You can get RGB++ assets using the [rgbpp-sdk examples](https://github.com/ckb-cell/rgbpp-sdk/tree/develop/examples/rgbpp/xudt)
def transfer_rgbpp_on_btc(params: RgbppTransferReq):
    # Please make sure the network of BTC is correct, including mainnet, testnet and signet
    network = "signet"

    # HD Key (note the named_key path only contains 4 layers)
    root_key = HDPrivateKey.from_seed(SEED, network)
    root_named_key = NamedHDPublicKey.from_hd_priv(root_key, "m/84'/0'/0'")

    # P2WPKH Address
    p2wpkh_path = "m/84'/0'/0'/0"
    p2wpkh_key = root_key.traverse(p2wpkh_path)
    p2wpkh_child_0 = p2wpkh_key.child(0)
    print(f'BTC P2WPKH Address: {p2wpkh_child_0.p2wpkh_address()}')

    # Generate RGB++ CKB virtual tx and BTC PSBT hex from the rgbpp-sdk-service
    response = rpc.generate_rgbpp_transfer_tx(params)
    btc_psbt_hex = response['btc_psbt_hex']
    ckb_virtual_tx_result = response['ckb_virtual_tx_result']
    print(f'CKB virtual tx result: {ckb_virtual_tx_result}')

    # Parse PSBT
    psbt = PSBT.parse(BytesIO(bytes.fromhex(btc_psbt_hex)), network)
    
    # Update lookup context
    tx_lookup = psbt.tx_obj.get_input_tx_lookup()
    pubkey_lookup = root_named_key.bip44_lookup()
    psbt.update(tx_lookup, pubkey_lookup)

    # Sign PSBT with the root_key
    psbt.sign(root_key)

    # Finalize PSBT and convert to TX
    psbt.finalize()
    btc_tx = psbt.final_tx()
    signed_tx_hex = btc_tx.serialize().hex()
    print(f"BTC signed tx: {signed_tx_hex}")

    # Broadcast the BTC signed transaction
    btc_tx_id = rpc.send_btc_transaction({ 'tx_hex': signed_tx_hex })
    print(f"BTC tx id: {btc_tx_id}")

    # Re-post the CKB virtual tx and BTC tx id to the Queue Service
    rpc.report_rgbpp_ckb_tx_btc_txid({
        'ckb_virtual_tx_result': ckb_virtual_tx_result,
        'btc_tx_id': btc_tx_id
    })

    # Check the RGB++ TX state from the Queue Service every 30 seconds
    while True:
        response = rpc.get_rgbpp_tx_state({
            'btc_tx_id': btc_tx_id,
            'params': {
                'with_data': False
            }
        })
        state = response["state"]
        print(f"RGB++ TX state: {state}")

        if (state == "completed"):
            ckb_tx_hash = rpc.get_rgbpp_ckb_tx_hash({'btc_tx_id': btc_tx_id})
            print(f"RGB++ assets have been completed and CKB tx hash: {ckb_tx_hash}")
            break
        elif (state == "failed"):
            print(f"RGB++ assets have been failed and the reason is {response["failed_reason"]}")
            break
        else:
            time.sleep(INTERVAL_TIME_SECONDS)


# Please replace the correct parameters with your own
transfer_rgbpp_on_btc({
    # xUDT type args which can be found in the CKB explorer or the logs from your RGB++ issue transaction
    'xudt_type_args': '0x562e4e8a2f64a3e9c24beb4b7dd002d0ad3b842d0cc77924328e36ad114e3ebe',
    # RGB++ lock args is the RGB++ lock script args which you can find in the CKB explorer
    # The args includes two parts: btc tx output index(little endian u32) and btc tx id(32 bytes)
    # The btc tx id displayed on BTC explorer is different from the btc tx id in the RGB++ lock args. They are in reverse byte order
    'rgbpp_lock_args_list': ['0x010000002d0ac46d188cc3e69158e99623caa3e843b311c293cbcb9b389e62edee0e5b39'],
    'transfer_amount': hex(800 * 10 ** 8),
    'from_btc_address': 'tb1qs4n7d4c7n242uyw26gcwvmurhnrt2he84zk2cr',
    'to_btc_address': 'tb1qs4n7d4c7n242uyw26gcwvmurhnrt2he84zk2cr'
})