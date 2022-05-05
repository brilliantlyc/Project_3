pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";

contract JoeCoin is ERC20, ERC20Detailed {
    constructor() ERC20Detailed("JoeCoin", "JOE", 4) public {
        // Mint JoeCoin tokens for the owner of the contract
        _mint(msg.sender, 100 * 10 ** 18);
    }

    // Create mint() function to allow account addresses in front end app (streamlit) to mint and transfer tokens to 
    // the FintechNFT contract
    function mint(address to, uint256 amount) public {
        _mint(to, amount);
    }
}

