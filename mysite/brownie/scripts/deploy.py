from brownie import accounts, config, SimpleStorage, network

def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    store_value = simple_storage.retrieve()
    print(store_value)

def get_account():
    if(network.show_active() == "development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    deploy_simple_storage()
    
    # brownie run scripts/deploy.py --network rinkeby