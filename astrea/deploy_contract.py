"""Basic contract compiling and deployment process.

- creating account must be unlocked.
- by default, account unlocked for 5 minutes (300s)
- call personal.unlockAccount("acct", "passwd", 0) for no limit
"""

import json
from os.path import dirname
from pathlib import Path

from web3 import Web3, HTTPProvider
from solc import compile_files

SOL_PATH = Path(dirname(__file__))
SOL_FNAME = "verify_model.sol"
SOL_FILE = str(SOL_PATH / SOL_FNAME)
BIN_FILE = str(SOL_PATH / "verify_model.solbin")
CONTRACT_NAME = "ModelVerification"


def get_bin_key(root):
    return "%s:%s" % (str(root / SOL_FNAME), CONTRACT_NAME)


def compile_contract(w3):
    compiled_sol = compile_files([SOL_FILE])
    contract_interface = compiled_sol[get_bin_key(SOL_PATH)]
    return compiled_sol, contract_interface


def instantiate_contract(w3, contract_interface):
    return w3.eth.contract(
        abi=contract_interface["abi"], bytecode=contract_interface["bin"])


def deploy_contract(w3, contract):
    tx_hash = contract.deploy(
        transaction={"from": w3.eth.accounts[0], "gas": 300000})
    return tx_hash


if __name__ == "__main__":
    w3 = Web3(HTTPProvider("http://localhost:8545"))

    compiled_sol, contract_interface = compile_contract(w3)
    with open(BIN_FILE, "w") as f:
        print("writing compiled contract to: %s" % BIN_FILE)
        json.dump(compiled_sol, f)
    contract = instantiate_contract(w3, contract_interface)
    tx_hash = deploy_contract(w3, contract)
    # get transaction receipt and contract address
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    contract_address = tx_receipt["contractAddress"]

    print("transaction recipt: %s" % tx_receipt)
    print("contract address: %s" % contract_address)
