<img src="Images_readme/joe-mint-factory.png" width="210" Alt="Joes" class="center">


## **Background**

<span style="text-align:justify">
Joe's discovered the fascinating world of digital tokens and he's looking to build different smart contract applications that will enable him do a number of things:

 - Mint his most memorable pictures onto a blokchain as NFTs.
 - Mint his own art while astutely coding and using his own fungible token to do so and; 
 - Lastly create a dutch auction mechanism to try and sell his NFTs to other blockchain participants!
 
</span>         
  

## **High Level Goals** 
- To showcase to beginner/intermediary smart contract developers the versatility of token contracts.

- To connect ERC20 & ERC721 tokens.

- To show a mechanism that can be used in selling NFTs on a blokchain by using smart contracts



## **Technologies**

### Blockchain related
- **Solidity**: Programming language used to write smart contracts. <img src="Images_juan/solidity.png" width="15" Alt="Joes" class="center">
- **Remix**: IDE used to write smart contracts in Solidity. It contains functionality that enables a user to compile and deploy contracts outside of a blockchain. <img src="Images_juan/remix.png" width="15" Alt="Joes" class="center">
- **MetaMask**: Browser extension of cryptocurrency wallet used to connect and deploy contracts & transactions on a blockchain.<img src="Images_juan/metamask.png" width="15" Alt="Joes" class="center">
- **(Polygon) Testnet**: Testnets allows developers to deploy contracts and transact in a blokchain without incurring gas fees. It is a simulation of a real blokchain which is perfect for developmental puporses <img src="Images_juan/polygon.png" width="15" Alt="Joes" class="center"> 
- **Pinata**:  Pinata's powerful but easy-to-use product allows users to upload, share, and manage files with unmatched speed throughout the IPFS network. <img src="Images_juan/pinata.png" width="15" Alt="Joes" class="center">
- **IPFS**: The InterPlanetary File System is a protocol and peer-to-peer network for storing and sharing data in a distributed file system. <img src="Images_juan/IPFS.png" width="15" Alt="Joes" class="center">
- **Web3.py:** is a Python library for interacting with Ethereum.

### Other
- **Python**: Programming language used to develop the back end of our ""Photo Registry"" UI. <img src="Images_juan/python.png" width="15" Alt="Joes" class="center">
- **Streamlit**: Python package used to develop a UI web application.<img src="Images_juan/streamlit.png" width="20" Alt="Joes" class="center"> 



## **Snapshots of our code**

We compiled a few images of back end code and blockchain transaction history we collected along the way. 

We strongly suggest you check our video demo presentations for a complete overview of our work!

*Videos can be found on the presentation slides.

### **Part I: Register Photography**
We created an easy to use UI that allows any person to mint digital images as NFTs. These NFTs were not minted into a blockchain but were only ran locally.

*Deployment of NFT contract on Remix IDE* 

<img src="Images_readme/claudia-2.png" width="300" Alt="Joes" class="center">

*Deployment of Coin token contract on Remix IDE*

<img src="Images_readme/claudia-4.png" width="300" Alt="Joes" class="center">

*Excerpts from our python/streamlit code behind our web based UI*

<img src="Images_readme/claudia-6.png" width="300" Alt="Joes" class="center">

<img src="Images_readme/claudia-7.png" width="300" height="200" Alt="Joes" class="center">

*loading our token contract (python function)*

<img src="Images_readme/claudia-9.png" width="300" Alt="Joes" class="center">



### **Part II: Minting on the blockchain**
We used an ERC20 contract to create our own fungible token. Then we added functionality to a ERC721 contract to accept our fungible token as payment in order to mint NFTs.   

We minted our tokens to Polygon's testnet and showcased our NFT on Opensea.

*Snapshot of JoeToken deployed on Polygon*

<img src="Images_readme/jalal-1.png" width="400" Alt="Joes" class="center">

*Initializing JoeToken contract address as a state variable on our NFT contract before deploying*

<img src="Images_readme/jalal-2.png" width="300" height="400" Alt="Joes" class="center">

*Polygon transaction record*

<img src="Images_readme/jalal-3.png" width="300" height="400" Alt="Joes" class="center">



### **Part III: Deutch Auction**
We built a smart contract that simulates a dutch auction in order to sell NFTs on a blockchain.

*Ductch Auction Contract*

<img src="Images_readme/nedal-1.png" width="400" height="300" Alt="Joes" class="center">

*NFT contract*

<img src="Images_readme/nedal-2.png" width="400" height="300" Alt="Joes" class="center">

*Functionality embedded on NFT contract*

<img src="Images_readme/nedal-3.png" width="300" height="400" Alt="Joes" class="center">

## **Conclusions**
Using readily available and open-source blockchain technologies and fairly advanced but easy to read Solidity (and Python!) code, we were able to successfully develop standard-meeting tokens and use them in different contexts. From creating a registry of tokenized pictures, to deploying tokens on an actual blockchain, to formulating a way to sell them!