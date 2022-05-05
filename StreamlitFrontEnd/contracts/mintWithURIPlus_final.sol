// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts@4.5.0/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts@4.5.0/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts@4.5.0/access/Ownable.sol";
import "@openzeppelin/contracts@4.5.0/utils/Counters.sol";

// The FintechNFT contract inherits the following OpenZeppelin:
// * ERC721
// * ERC721URIStorage
// * Ownable
contract FintechNFT is ERC721, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;

    uint256 public totalSupply;
    uint256 public maxSupply;
    IERC20 public tokenAddress;
    uint256 public rate = 5 * 10 ** 18;
    
    Counters.Counter private _tokenIdCounter;

    // Set the constructor to take in the token address of the JoeCoin contract that will be deployed first
    // Set the maxSupply of the FintechNFT token during deployment
    constructor(address _tokenAddress) ERC721("FintechNFT", "FNTCH") {
        tokenAddress = IERC20(_tokenAddress);
        maxSupply = 20;
    }
    // Create struct object for the photography to be registered
    struct Photography {
        string name;
        string photographer;
        uint256 yearCreated; 
    }

    // Create a photography collection that will map a uint256 (tokenId) to a Photography type object
    mapping(uint256 => Photography) public photographyCollection;

    // Allow only the owner of the contract to set the maxSupply of tokens
    function setMaxSupply(uint256 maxSupply_) external onlyOwner {
        maxSupply = maxSupply_;
    }

    // Define safeMint() function that takes in a 'tokenId', a 'to' minting address, and a 'uri' for the token 
    function safeMint(uint256 tokenId, address to, string memory uri) public {
        // Require that the maxSupply exceeds the totalSupply before minting
        require(maxSupply > totalSupply, 'tokens sold out');

        // Transfer tokens from the 'to' address' balance of the token contract (i.e., JoeCoin) to this FintechNFT contract
        // in the amount of 'rate'
        tokenAddress.transferFrom(to, address(this), rate);
        
        // Increment by 1, the totalSupply of FintechNFT tokens
        totalSupply++;
        // Increment the _tokenIdCounter
        _tokenIdCounter.increment();
        // Use the ERC721's _safeMint() function to safely mint a new token that the 'to' address will own
        // The function reverts if the given token ID already exists
        _safeMint(to, tokenId);
        // Set the token's uri using an inherited function
        _setTokenURI(tokenId, uri);
    }

    // Define an onlyOwner withdrawToken() function that takes in a 'to' address and transfers the amount of tokens
    // in the FintechNFT contract to the 'to' address. That is, it withdraws JoeCoin tokens from the FintechNFT contract.
    function withdrawToken(address to) public onlyOwner {
        tokenAddress.transfer(to, tokenAddress.balanceOf(address(this)));
    }

    // Define function to register the photography using the address of the photography owner, the photography name, 
    // the photographer, year it was created (taken), and its uri. The function returns a tokenId.
    function registerPhotography(
        address owner,
        string memory name,
        string memory photographer,
        uint256 yearCreated,
        string memory URI
    ) public returns (uint256) {
        // Get the current value of the _tokenIdCounter and set it equal to the tokenId
        uint256 tokenId = _tokenIdCounter.current();

        // Use the safeMint function defined above to mint the FintechNFT
        safeMint(tokenId, owner, URI);
        
        // Add the new Photography record to the photographyCollection
        photographyCollection[tokenId] = Photography(name, photographer, yearCreated);

        return tokenId;
    }

    // The following functions are overrides required by Solidity. They are necessary in order to be able to use
    // the _setTokenURI() function in solidity version 0.8.4

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
