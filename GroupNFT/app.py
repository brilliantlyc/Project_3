from email.mime import image
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Load-Contract function
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/FintechNFT_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract


# Load the contract
contract = load_contract()

# Function to get the COOOL (CoolCoin.sol) token contract
def load_token_contract():

    # Load the contract ABI
    with open(Path('./contracts/compiled/COOOL_abi.json')) as f:
        token_contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    token_contract_address = os.getenv("TOKEN_SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=token_contract_address,
        abi=token_contract_abi
    )

    return contract

# Get the token contract
token_contract = load_token_contract()


################################################################################
# Helper functions to pin files and json to Pinata
################################################################################


def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash


st.title("Digital Art Registry Minting System")
st.write("Choose an account to get started")

accounts = w3.eth.accounts
address = st.selectbox("Select Artwork Owner", options=accounts)
st.markdown("---")

# We will mint some COOOL tokens for the all accounts 
# Check if account_balance is less than the amount we want to give it, then mint COOOL tokens
for account in accounts:
    account_balance = token_contract.functions.balanceOf(account).call()
    if account_balance < (100 * 10 ** 18):
        token_contract.functions.mint(account, 100 * 10 ** 18).transact({'from': account, 'gas': 1000000})

# Set the FintechNFT contract to be approved to use the COOOL token contract
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
contract_owner = contract.functions.owner().call()
approve_amount = token_contract.functions.balanceOf(contract_owner).call()
token_contract.functions.approve(contract_address, approve_amount).transact({'from': address, 'gas': 1000000})

address_balance = token_contract.functions.balanceOf(address).call()

st.write(f"The contract_address is {contract_address}")
st.write(f"The contract_owner is {contract_owner}")
st.write(f"The approve_amount is {approve_amount}")
st.write(f"The address_balance is {address_balance}")

################################################################################
# Register New Artwork
################################################################################
st.markdown("## Register New Digital Artwork")
artwork_name = st.text_input("Enter the name of the digital artwork")
artist_name = st.text_input("Enter the artist name")
created_year = st.text_input("Enter the creation year of the digital artwork")
initial_appraisal_value = st.text_input("Enter the initial appraisal amount")
file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])
if st.button("Register Artwork"):
    artwork_ipfs_hash = pin_artwork(artwork_name, file)
    artwork_uri = f"ipfs://{artwork_ipfs_hash}"
    tx_hash = contract.functions.registerDigitalArtwork(
        address,
        artwork_name,
        artist_name,
        int(created_year),
        int(initial_appraisal_value),
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
    #image_uri = artwork_ipfs_hash[1]
    # st.image(f"https://ipfs.io/ipfs/{image_uri}")
st.markdown("---")

################################################################################
# Display a Token
################################################################################
st.markdown("### Check Balance of an Account")

# Let user select an account address from the list
selected_address = st.selectbox("Select Account", options=accounts)

# Call 'balanceOf' contract function to display the tokens belonging to the selected address
tokens = contract.functions.balanceOf(selected_address).call()
st.write(f"This address owns {tokens} tokens")

st.markdown("### Check  Ownership and Display Token")

total_token_supply = contract.functions.totalSupply().call()

# Show the list of all tokens and let user select one to display its owner and URI 
selected_token_id = st.selectbox("Artwork Tokens", list(range(total_token_supply)))

if st.button("Display"):

    # Get the art token's owner
    owner = contract.functions.ownerOf(selected_token_id).call()
    
    st.write(f"The token is registered to {owner}")

    # Get the art token's URI
    token_uri = contract.functions.tokenURI(selected_token_id).call()

    st.write(f"The tokenURI is {token_uri}")
    #st.image(token_uri)



################################################################################
# Mint NFT 
################################################################################
# Display: safemint, maxsupply, and balance
st.markdown("## Mint NFT")

# Display maxsupply
max_token_supply = contract.functions.maxSupply().call()
st.write(f"Minting max supply is: {max_token_supply}")

# Get the token's URI
mint_token_uri = st.text_input("The URI to the artwork")
mint_address = st.selectbox("Select Address to Mint", options=accounts)

# If the "Mint NFT" button is clicked: call contract function using token_id, mint_address, and token_uri 
if st.button("Mint NFT"):
    # Set token_id equal to the current 'totalSupply' value in the contract 
    token_id = contract.functions.totalSupply().call()
    contract.functions.safeMint(int(token_id), mint_address, mint_token_uri).transact({'from': address, 'gas': 1000000})

# Show updated balance of the address that just minted
updated_tokens = contract.functions.balanceOf(mint_address).call()
st.write(f"New balance of this address: {updated_tokens} tokens")
st.markdown("---")

################################################################################
# Deutch-Auction Functionality
################################################################################
