from brownie import accounts, config, BallotFactory, network


def deploy_ballot():
    account = get_account()
    ballot_factory = BallotFactory.deploy({"from": account})
    
    print(f"Lenght is: {ballot_factory.bfGetBallotsLenght()}")
    
    new_proposal = ballot_factory.bfCreateBallot(0, ["op1", "op2"])
    
    print(f"Lenght is: {ballot_factory.bfGetBallotsLenght()}")


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_ballot()
