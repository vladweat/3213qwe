from brownie import BallotFactory, accounts, config, network


def read_contract():
    ballot_factory = BallotFactory[-1]
    new_proposal = ballot_factory.createBallotContract()
    new_proposal.bfCreateBallot(["sdfg", "sdfaf"])

    print(new_proposal.bfGetCreatorBallot(0))
    print(new_proposal.bfGetStatus(0))


def main():
    read_contract()
