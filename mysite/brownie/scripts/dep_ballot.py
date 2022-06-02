from brownie import accounts, config, Ballot, network


def deploy_ballot():
    account = get_account()
    ballot = Ballot.deploy({"from": account})
    test = ballot.getCreatorBallot()
    print(test)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_ballot()

    # brownie run scripts/deploy.py --network rinkeby
