from web3 import Web3
import json
from hexbytes import HexBytes

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# print(w3.isConnected())
# print(w3.eth.get_block('latest'))
with open(r"C:\Users\HY\Desktop\anib\marinelink\sol\build\contracts\ContractAuth.json", 'r') as f:
    datastore = json.load(f)
    abi = datastore["abi"]
    contract_address = datastore["networks"]["1638107507843"]["address"]

me = w3.eth.get_accounts()[0]

w3.eth.defaultAccount = w3.eth.accounts[1]
contract = w3.eth.contract(address=contract_address, abi=abi)
contract_id = "992688d677db8a32231ec2418b9971c4df672a7adad63010922a74fcfdeed33d".encode('utf-8')
contract_auth = "5fe0a1dcfc071a92207235c68d43f478d24b6f743f8d2a12369b71fa8c201524".encode('utf-8')
tx_hash = contract.functions.setContractAuthKey([int.from_bytes(contract_id[:32], 'big', signed=False), int.from_bytes(contract_id[32:], 'big', signed=False)], [int.from_bytes(contract_auth[:32], 'big', signed=False), int.from_bytes(contract_auth[32:], 'big', signed=False)]).transact({
  "from": w3.eth.accounts[0],
  "gas": "600000"
})
# tx_hash = contract.functions.setContractAuthKey([int.from_bytes(contract_id[:32], 'big', signed=False), int.from_bytes(contract_id[32:], 'big', signed=False)], [int.from_bytes(contract_auth[:32], 'big', signed=False), int.from_bytes(contract_auth[32:], 'big', signed=False)]).transact()
receipt = w3.eth.waitForTransactionReceipt(tx_hash)
contract_auth = contract.functions.getContractAuthKey(contract_id).call()
print(contract_auth)
