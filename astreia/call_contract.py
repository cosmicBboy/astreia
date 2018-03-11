"""Call the contract that we made in basic_deploy_contract.py"""

from argparse import ArgumentParser
import json
from os.path import dirname
from pathlib import Path
import time

from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

from deploy_contract import BIN_FILE, get_bin_key


# mock targets and predictions
def mock_y():
    return [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]


def mock_pred_A():
    return [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]


def mock_pred_B():
    return [1, 1, 1, 1, 0, 0, 0, 0, 0, 0]


def mock_pred_C():
    return [1, 1, 1, 1, 0, 1, 0, 0, 0, 0]


def print_verification_report(verified, accuracy, accuracy_threshold):
    print("-------------------")
    print("verification report")
    print("-------------------")
    print("verified: %s" % verified)
    print("accuracy: %s%%" % accuracy)
    print("accuracy_threshold: %s%%" % accuracy_threshold)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("contract_address", type=str)
    # parser.add_argument("payload", type=str)
    args = parser.parse_args()

    w3 = Web3(HTTPProvider("http://localhost:8545"))

    with open(BIN_FILE, "r") as f:
        compiled_sol = json.load(f)
    contract_interface = compiled_sol[get_bin_key(Path(dirname(__file__)))]

    # contract instance in concise mode
    contract_instance = w3.eth.contract(
        contract_interface["abi"], args.contract_address,
        ContractFactoryClass=ConciseContract)

    # verify model against mock data
    y = mock_y()
    pred_data = [
        # prediction set name, list of predictions, and expected accuracy
        ("A", mock_pred_A(), 100),
        ("B", mock_pred_B(), 90),
        ("C", mock_pred_C(), 80)]
    for pred_name, preds, expected in pred_data:
        print("verifying predictions, expected accuracy: %s%%" % expected)
        tx_hash = contract_instance.verify(
            y, preds, transact={"from": w3.eth.accounts[0], "gas": 300000})

        print("waiting for verification transaction to be mined", end="")
        while w3.eth.getTransactionReceipt(tx_hash) is None:
            print(".", end="")
            time.sleep(0.1)
        print("")

        verified, accuracy, acc_threshold = contract_instance.get_report()
        print_verification_report(verified, accuracy, acc_threshold)
        if accuracy != expected:
            raise AssertionError(
                "verified accuracy != expected accuracy\n"
                "y = %s\npreds = %s" % (str(y), str(preds)))
        print("")
    print("verification complete!")
