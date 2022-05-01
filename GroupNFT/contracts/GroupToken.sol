// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts@4.5.0/token/ERC20/ERC20.sol";

contract GroupToken is ERC20 {
    constructor() ERC20("GroupToken", "GTK") {
        _mint(msg.sender, 10000 * 10 ** decimals());
    }
}