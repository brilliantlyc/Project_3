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


st.title("Digital Art Registry Appraisal System")
st.write("Choose an account to get started")
accounts = w3.eth.accounts
address = st.selectbox("Select Artwork Owner", options=accounts)
st.markdown("---")

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
    #token_uri = "[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})"
    st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
    #image_uri = artwork_ipfs_hash[1]
    # st.image(f"https://ipfs.io/ipfs/{image_uri}")
st.markdown("---")

################################################################################
# Mint NFT 
################################################################################
# Display: safemint, maxsupply, and balance
st.markdown("## Mint NFT")
#tokens = contract.functions.totalSupply().call()
#token_id = st.selectbox("Choose an Art Token ID", list(range(tokens)))
token_id = st.text_input("Enter a token id")
# Get the token's URI
mint_token_uri = st.text_input("The URI to the artwork")
mint_address = st.selectbox("Select Address to Mint", options=accounts)
# If the "Mint NFT" button is clicked: call contract function using token_id, mint_address, and token_uri 
if st.button("Mint NFT"):

    contract.functions.safeMint(int(token_id), mint_address, mint_token_uri).transact({'from': address, 'gas': 1000000})
st.markdown("---")

################################################################################
# Deutch-Auction Functionality
################################################################################
