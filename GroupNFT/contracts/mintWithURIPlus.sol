// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts@4.5.0/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts@4.5.0/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts@4.5.0/access/Ownable.sol";
import "@openzeppelin/contracts@4.5.0/utils/Counters.sol";

contract FintechNFT is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;

    uint256 public totalSupply;
    uint256 public maxSupply;
    bool public isMintEnabled;
    IERC20 public tokenAddress;
    uint256 public rate = 100 * 10 ** 18;
    mapping(address => uint256) public mintedWallets;

    Counters.Counter private _tokenIdCounter;

    constructor(address _tokenAddress) ERC721("fintechNFT", "FNTCH") {
        tokenAddress = IERC20(_tokenAddress);
        maxSupply = 2;
    }

    struct digitalArtwork {
        string name;
        string artist;
        uint256 yearCreated; // Additional information about the artwork NFT
        uint256 appraisalValue;
    }

    mapping(uint256 => digitalArtwork) public digitalArtCollection;

    event Appraisal(uint256 tokenId, uint256 appraisalValue, string reportURI);

    function toggleIsMintEnabled() external onlyOwner {
        isMintEnabled = !isMintEnabled;
    }

    function setMaxSupply(uint256 maxSupply_) external onlyOwner {
        maxSupply = maxSupply_;
    }

    function safeMint(uint256 tokenId, address to, string memory uri) public onlyOwner {
        //uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }

    function withdrawToken() public onlyOwner {
        tokenAddress.transfer(msg.sender, tokenAddress.balanceOf(address(this)));
    }

    function registerDigitalArtwork(
        address owner,
        string memory name,
        string memory artist,
        uint256 yearCreated,
        uint256 initialAppraisalValue,
        string memory URI
    ) public returns (uint256) {
        uint256 tokenId = _tokenIdCounter.current();

        safeMint(tokenId, owner, URI);
        
        digitalArtCollection[tokenId] = digitalArtwork(name, artist, yearCreated, initialAppraisalValue);

        return tokenId;
    }

    // The following functions are overrides required by Solidity.

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

}
