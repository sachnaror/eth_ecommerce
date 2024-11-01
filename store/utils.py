from web3 import Web3

# Connect to Ethereum node (e.g., Infura)
infura_url = "https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # Replace with your Infura project ID
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract details
contract_address = "0x1234567890abcdef1234567890abcdef12345678"  # Replace with your deployed contract address
contract_address = web3.toChecksumAddress(contract_address)  # Convert to checksum address

# ABI for the Smart Contract (Replace with your actual contract ABI)
contract_abi = [
    {
        "inputs": [{"internalType": "uint256", "name": "x", "type": "uint256"}],
        "name": "set",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "get",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [],
        "name": "StoredDataUpdated",
        "type": "event"
    }
]

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def set_data(value, account):
    """Set the value in the contract."""
    # Estimate gas required for the transaction
    estimated_gas = contract.functions.set(value).estimateGas({'from': account})

    # Fetch the current gas price
    gas_price = web3.eth.gas_price

    # Calculate total cost of the transaction
    total_cost = estimated_gas * gas_price

    # Check the balance of the account
    balance = web3.eth.get_balance(account)

    # Ensure the account has enough Ether to cover the total cost
    if balance < total_cost:
        raise Exception("Insufficient funds to cover gas fees.")

    # Send the transaction
    tx_hash = contract.functions.set(value).transact({
        'from': account,
        'gas': estimated_gas,
        'gasPrice': gas_price
    })

    # Wait for the transaction receipt
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

def get_data():
    """Get the value from the contract."""
    return contract.functions.get().call()

def create_product(name, price, account):
    """Function to create a new product on the blockchain."""
    try:
        # Ensure price is valid
        price_in_wei = web3.toWei(price, 'ether')
        tx_hash = contract.functions.createProduct(name, price_in_wei).transact({'from': account})
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        raise Exception(f"Error creating product: {str(e)}")

def purchase_product(product_id, account):
    """Function to purchase a product from the blockchain store."""
    try:
        # Assuming you know the price for the product, or retrieve it from the contract
        product_price = web3.toWei(0.01, 'ether')  # Example price in Ether
        tx_hash = contract.functions.purchaseProduct(product_id).transact({
            'from': account,
            'value': product_price
        })
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
    except Exception as e:
        raise Exception(f"Error purchasing product: {str(e)}")
