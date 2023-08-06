# libopy

## Installing<a name="installing"></a>

Installing from PyPI repository (https://pypi.org/project/libopy):

```bash
pip install libopy
```

## Usage<a name="usage"></a>

### Generating a wallet<a name="generating-a-wallet"></a>

```python
from libopy import generate_wallet

wallet = generate_wallet()
```

The value assigned to `wallet` will be a dictionary just like:

```python
{
    "seed": "YOUR_MNEMONIC_SEED",
    "derivation_path": "m/44'/118'/0'/0/0",
    "private_key": b"\xcc\xec^\xf6\xdcg\xe6\xb5\x89\xed\x8cG\x05\x03\xdf0:\xc9\x8b \x85\x8a\x14\x12\xd7\xa6a\x01\xcd\xf8\x88\x93",
    "public_key": b"\x13\x1d\xae\xa7\x9eO\x8e\xc5\xff\xa3sAw\xe6\xdd\xc9\xb8b\x06\x0eo\xc5a%z\xe3\xff\x1e\xd2\x8e5\xe7",
    "address": "libonomy5byhna3psjqfxnw4msrfzsr0g08yuyfxeht0qak",
}
```

### Converter functions<a name="converter-functions"></a>

#### Mnemonic seed to private key<a name="mnemonic-seed-to-private-key"></a>

```python
from libopy import BIP32DerivationError, seed_to_privkey

seed = (
    "YOUR_MNEMONIC_SEED"
)
try:
    privkey = seed_to_privkey(seed, path="m/44'/118'/0'/0/0")
except BIP32DerivationError:
    print("No valid private key in this derivation path!")
```

#### Private key to public key<a name="private-key-to-public-key"></a>

```python
from libopy import privkey_to_pubkey

privkey = bytes.fromhex(
    "1dcd05d7ac71e09d3cf7da666709ebd59362486ff9e99db0e8bc663570515ala"
)
pubkey = privkey_to_pubkey(privkey)
```

#### Public key to address<a name="public-key-to-address"></a>

```python
from libopy import pubkey_to_address

pubkey = bytes.fromhex(
    "1dcd05d7ac71e09d3cf7da666709ebd59362486ff9e99db0e8bc663570515ala"
)
addr = pubkey_to_address(pubkey)
```

#### Private key to address<a name="private-key-to-address"></a>

```python
from libopy import privkey_to_address

privkey = bytes.fromhex(
    "1dcd05d7ac71e09d3cf7da666709ebd59362486ff9e99db0e8bc663570515ala"
)
addr = privkey_to_address(privkey)
```

### Signing transactions<a name="signing-transactions"></a>

```python
from libopy import Transaction

tx = Transaction(
    privkey=bytes.fromhex(
        "1dcd05d7ac71e09d3cf7da666709ebd59362486ff9e99db0e8bc663570515ala"
    ),
    account_num=0,
    sequence=0,
    fee=0,
    gas=0,
    memo="",
    chain_id="chain-id",
    sync_mode="sync",
)
tx.add_transfer(
    recipient="libonomy5byhna3psjqfxnw4msrfzsr0g08yuyfxeht0qak", amount=1000000 
)
tx.add_transfer(recipient="libonomy5byhna3psjqfxnw4msrfzsr0g08yuyfxeht0qak", amount=1000000)
pushable_tx = tx.get_pushable()
```

One or more token transfers can be added to a transaction by calling the `add_transfer` method.

When the transaction is fully prepared, calling `get_pushable` will return a signed transaction in the form of a JSON string.
This can be used as request body when calling the `POST /txs` endpoint.