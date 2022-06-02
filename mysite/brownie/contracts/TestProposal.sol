// SPDX-License-Identifier: MIT
pragma experimental ABIEncoderV2;
pragma solidity ^0.8.0;

contract TestProposal {
    struct Proposal {
        uint256 proposalId;
        uint256 proposalStatus;
        address proposalCreator;
        uint256 proposalNumOfOptions;
        string proposalOptionsString;
        // Option[] options;
        // mapping (uint => Voter) voters;
        // mapping (uint => proposalOption) options;
    }

    mapping(uint256 => Proposal) public proposals;
    // event savingEvent(uint indexed _proposalId);
    uint256 public proposalCount;

    // constructor() public {
    //     proposalCount = 0;
    //     addProposal(
    //         1,
    //         1,
    //         0xB5dea2661dfa4b8f0aaE8Bc1F583369D927c3b06,
    //         3,
    //         "op1-op2-op3"
    //     );
    // }

    function addProposal(
        uint256 _proposalId,
        uint256 _proposalStatus,
        address _proposalCreator,
        uint256 _proposalNumOfOptions,
        string memory _proposalOptionsString
    ) public {
        proposals[proposalCount] = Proposal(
            _proposalId,
            _proposalStatus,
            _proposalCreator,
            _proposalNumOfOptions,
            _proposalOptionsString
        );
        proposalCount++;
    }

    // functions section

    // split string proposalOptions to string[] with all options
    // str: "op1-op2-op3" -> string[0] = op1, string[1] = op2, string[2] = op3
    struct TEST {
        Option[] optionArray;
    }

    struct Option {
        string name;
    }
    // Option[] public abra;

    string[] public opopop;

    function getOptions() public view returns (string[] memory) {
        return opopop;
    }

    // get ? sections

    function getProposalStructure(uint256 _proposalId)
        public
        view
        returns (Proposal memory)
    {
        return proposals[_proposalId];
    }
}
