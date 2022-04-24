pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract DigitalArtRegistry is ERC721Full {
    constructor() public ERC721Full("DigitalArtRegistryToken", "DRRT") {}

    struct digitalArtwork {
        string name;
        string artist;
        uint256 yearCreated; // Additional information about the artwork NFT
        uint256 appraisalValue;
    }

    mapping(uint256 => digitalArtwork) public digitalArtCollection;

    event Appraisal(uint256 tokenId, uint256 appraisalValue, string reportURI);

    function registerDigitalArtwork(
        address owner,
        string memory name,
        string memory artist,
        uint256 yearCreated,
        uint256 initialAppraisalValue,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        digitalArtCollection[tokenId] = digitalArtwork(name, artist, yearCreated, initialAppraisalValue);

        return tokenId;
    }

    function newAppraisal(
        uint256 tokenId,
        uint256 newAppraisalValue,
        string memory reportURI
    ) public returns (uint256) {
        digitalArtCollection[tokenId].appraisalValue = newAppraisalValue;

        emit Appraisal(tokenId, newAppraisalValue, reportURI);

        return digitalArtCollection[tokenId].appraisalValue;
    }
}