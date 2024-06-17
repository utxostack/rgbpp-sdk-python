from rgbpp.rpc import rpc

request = {
    'btc_tx_id': 'fb4ebf0f4f9c9fc32b22c89cac7eccd7364d013f4a0422e402c70839c70339ca',
    'params': {
        'with_data': True
    }
}
response = rpc.get_rgbpp_tx_state(request)
print('response: ', response)
