from brownie import accounts, config, BallotFactory, network


def deploy_ballot():
    account = get_account()
    ballot_factory = BallotFactory.deploy({"from": account})
    new_proposal = ballot_factory.createBallotContract()
    print(new_proposal)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_ballot()
