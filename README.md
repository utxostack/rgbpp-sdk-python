# rgbpp-sdk-python

This repository offers essential utilities for RGB++ asset integration using the [RGB++ SDK Service](https://github.com/ckb-cell/rgbpp-sdk/tree/feat/rgbpp-sdk-service).

## Start RGB++ SDK Service

> [!IMPORTANT]
> The RGB++ SDK Service must be runing before using `rgbpp-sdk-python` to build your RGB++ DApps

### Clone rgbpp-sdk to start service

```shell
git clone https://github.com/ckb-cell/rgbpp-sdk.git
cd apps/service
```

### Update Environment Variables

Copy the `.env.example` file to `.env`:

```shell
cp .env.example .env
```

Update the configuration values:

```yml
# testnet for CKB and BTC Testnet and mainnet for CKB and BTC Mainnet, the default value is testnet
NETWORK=testnet

# The Bitcoin Testnet type including Testnet3 and Signet, the default value is Signet
# Testnet3: https://mempool.space/testnet
# Signet: https://mempool.space/signet
BTC_TESTNET_TYPE=Signet

# CKB node url which should match NETWORK
CKB_RPC_URL=https://testnet.ckb.dev

# The BTC assets api url which should match NETWORK and BTC_TESTNET_TYPE
# The BTC Testnet Service url is: https://api.testnet.rgbpp.io
# The BTC Signet Service url is: https://api.signet.rgbpp.io
BTC_SERVICE_URL=https://api.signet.rgbpp.io

# The BTC assets api token which should match NETWORK and BTC_TESTNET_TYPE
# To get an access token of BTC Testnet, please refer to https://github.com/ckb-cell/rgbpp-sdk/tree/develop/packages/service#get-an-access-token
BTC_SERVICE_TOKEN=

# The BTC assets api origin which should match NETWORK and BTC_TESTNET_TYPE
BTC_SERVICE_ORIGIN=https://btc-test.app
```

### Run RGB++ SDK Service

```shell
pnpm install && pnpm dev
```

## Quick Start

Install in a virtualenv

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Example Code

See `examples/` directory. For instance this example calls the RGB++ SDK Service RPC to get RGB++ tx state:

```shell
PYTHONPATH=. python examples/rpc_state.py
```

And the RGB++ assets transfer on BTC example is provided:
```shell
# The example is only for RGB++ transfer on BTC 
# You can get RGB++ assets using the [rgbpp-sdk examples](https://github.com/ckb-cell/rgbpp-sdk/tree/develop/examples/rgbpp/xudt)
PYTHONPATH=. python examples/rgbpp_transfer.py
```

## Test

Please make sure the RGB++ SDK Service is running

```shell
python3 -m unittest
```

## Reference

There are BTC and CKB transactions for RGB++ transfer on BTC Signet network as following:

BTC TX: https://mempool.space/signet/tx/395b0eeeed629e389bcbcb93c211b343e8a3ca2396e95891e6c38c186dc40a2d
CKB TX: https://pudge.explorer.nervos.org/transaction/0xf021237b6a6af7fa5628e4a69736efa5f5fed9a858439e6e9d612097f1bf38be