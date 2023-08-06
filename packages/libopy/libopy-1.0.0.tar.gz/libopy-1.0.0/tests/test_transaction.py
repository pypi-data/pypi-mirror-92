from unittest.mock import Mock

from libopy import Transaction


def test_sign():
    private_key = bytes.fromhex("2afc5a66b30e7521d553ec8e6f7244f906df97477248c30c103d7b3f2c671fef")
    unordered_sign_message = {
        "chain_id": "main-stake",
        "account_number": "1",
        "fee": {"gas": "21906", "amount": [{"amount": "0", "denom": ""}]},
        "memo": "",
        "sequence": "0",
        "msgs": [
            {
                "type": "cusp-sdk/Send",
                "value": {
                    "inputs": [
                        {
                            "address": "libonomy1qperwt9wrnkg5k9e5gzfgjppzpqhyav5j24d66",
                            "coins": [{"amount": "1", "denom": "flby"}],
                        }
                    ],
                    "outputs": [
                        {
                            "address": "libonomy1yeckxz7tapz34kjwnjxvmxzurerquhtrmxmuxt",
                            "coins": [{"amount": "1", "denom": "flby"}],
                        }
                    ],
                },
            }
        ],
    }
    dummy_num = 1337
    tx = Transaction(
        privkey=private_key,
        account_num=dummy_num,
        sequence=dummy_num,
        fee=dummy_num,
        gas=dummy_num,
    )
    tx._get_sign_message = Mock(return_value=unordered_sign_message)  # type: ignore

    expected_signature = (
        "YjJhlAf7aCnUtLyBNDp9e6LKuNgV7hJC3rmm0Wro5nBsIPVtWzjuobsp/AhR5Kht+HcRF2zBq4AfoNQMIbY6fw=="
    )

    actual_signature = tx._sign()
    assert actual_signature == expected_signature


def test_get_pushable_tx():
    expected_pushable_tx = '{"tx":{"msg":[{"type":"cusp-sdk/MsgSend","value":{"from_address":"libonomy1lgharzgds89lpshr7q8kcmd2esnxkfpwvuz5tr","to_address":"libonomy103l758ps7403sd9c0y8j6hrfw4xyl70j4mmwkf","amount":[{"denom":"flby","amount":"387000"}]}}],"fee":{"gas":"37000","amount":[{"denom":"flby","amount":"1000"}]},"memo":"","signatures":[{"signature":"chbQMmrg18ZQSt3q3HzW8S8pMyGs/TP/WIbbCyKFd5IiReUY/xJB2yRDEtF92yYBjxEU02z9JNE7VCQmmxWdQw==","pub_key":{"type":"aphelion/PubKeySecp256k1","value":"A49sjCd3Eul+ZXyof7qO460UaO73otrmySHyTNSLW+Xn"},"account_number":"11335","sequence":"0"}]},"mode":"sync"}'  # noqa: E501

    _tx_total_cost = 388000
    fee = 1000
    amount = _tx_total_cost - fee

    tx = Transaction(
        privkey=bytes.fromhex("26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59"),
        account_num=11335,
        sequence=0,
        fee=fee,
        gas=37000,
        chain_id="main-stake",
    )
    tx.add_transfer(recipient="libonomy103l758ps7403sd9c0y8j6hrfw4xyl70j4mmwkf", amount=amount)
    pushable_tx = tx.get_pushable()
    assert pushable_tx == expected_pushable_tx
