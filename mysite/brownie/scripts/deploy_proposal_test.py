from brownie import accounts, config, TestProposal, network


def deploy_proposal_test():
    account = get_account()
    proposal_test = TestProposal.deploy({"from": account})
    store_value = proposal_test.getProposalStructure(0)
    print(store_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_proposal_test()

    # brownie run scripts/deploy.py --network rinkeby
