// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract GroupNFT is ERC721, Ownable {
    using Counters for Counters.Counter;
    IERC20 public tokenAddress;
    uint256 public rate = 100 * 10 ** 18;

    Counters.Counter private _tokenIdCounter;

    constructor(address _tokenAddress) ERC721("GroupNFT", "GTK") {
        tokenAddress = IERC20(_tokenAddress);
    }

    function safeMint() public {
        tokenAddress.transferFrom(msg.sender, address(this), rate);
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(msg.sender, tokenId);
    }

    function withdrawToken() public onlyOwner {
        tokenAddress.transfer(msg.sender, tokenAddress.balanceOf(address(this)));
    }
}