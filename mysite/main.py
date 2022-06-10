from web3 import Web3


def deploy():
    with open(
        os.path.join(settings.BASE_DIR, "brownie/build/contracts/BallotFactory.json")
    ) as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    abi = jsonObject["abi"]
    bytecode = jsonObject["bytecode"]

    # contract_id, contract_interface = compiled_sol.popitem()
    # bytecode = contract_interface["bin"]
    # abi = contract_interface["abi"]

    web3 = Web3(Web3.HTTPProvider(infura_url))

    BallotFactory = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = BallotFactory.createBallotContract().transact()

    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    out = contract.functions.bfGetProposals(0)
