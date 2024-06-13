# rgbpp-sdk-python

This repository offers essential utilities for RGB++ asset integration using the [RGB++ SDK Service](https://github.com/ckb-cell/rgbpp-sdk/tree/feat/rgbpp-sdk-service).

## Start RGB++ SDK Service

> [!IMPORTANT]
> The RGB++ SDK Service must be run before using `rgbpp-sdk-python` to build your RGB++ DApps

### Clone rgbpp-sdk to start service

> [!TIP]
> The RGB++ SDK Service will be ready when the [PR](https://github.com/ckb-cell/rgbpp-sdk/pull/218) is approved and merged

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

# The Bitcoin Testnet type including Testnet3 and Signet, default value is Testnet3
# Testnet3: https://mempool.space/testnet
# Signet: https://mempool.space/signet
BTC_TESTNET_TYPE=Testnet3

# CKB node url which should be matched with NETWORK
CKB_RPC_URL=https://testnet.ckb.dev

# The BTC assets api url which should be matched with NETWORK and BTC_TESTNET_TYPE
BTC_SERVICE_URL=https://btc-assets-api.testnet.mibao.pro

# The BTC assets api token which should be matched with NETWORK and BTC_TESTNET_TYPE
# To get an access token, please refer to https://github.com/ckb-cell/rgbpp-sdk/tree/develop/packages/service#get-an-access-token
BTC_SERVICE_TOKEN=

# The BTC assets api origin which should be matched with NETWORK and BTC_TESTNET_TYPE
BTC_SERVICE_ORIGIN=https://btc-assets-api.testnet.mibao.pro


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

```
PYTHONPATH=. python examples/rpc_state.py
```

## Test

```shell
python3 -m unittest
```