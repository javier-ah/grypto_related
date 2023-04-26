#!/usr/bin/env python
# coding: utf-8


# requirements

# $pip install web3
# $pip install eth-abi
from web3 import Web3
from eth_abi import abi
import moralis
from moralis import evm_api
import json
from eth_abi import decode


# test moralis endpoint
api_key = "YOUR_API_KEY"
print(moralis.utils.web3_api_version(api_key))



# get all Deposit events for the Cake Pool contract
# address -> the address of the contract
# topic0 -> the topic of the Deposit event, as found in Pancakeswap


params = {
  "chain": "bsc",
  "topic0": "0x7162984403f6c73c8639375d45a9187dfd04602231bd8e587c415718b5f7e5f9",
  "address": "0x45c54210128a065de780C4B0Df3d16664f7f859e"
}

result = evm_api.events.get_contract_logs(
  api_key=api_key,
  params=params,
)

result['result']


# get all Deposit events for the Cake Pool contract for a specific block
# address -> the address of the contract
# topic0 -> the topic of the Deposit event, as found in Pancakeswap
# block_number -> an arbitrary block

block_number = "27315030"

params = {
  "chain": "bsc",
  "block_number": block_number,
  "topic0": "0x7162984403f6c73c8639375d45a9187dfd04602231bd8e587c415718b5f7e5f9",
  "address": "0x45c54210128a065de780C4B0Df3d16664f7f859e"
}

result2 = evm_api.events.get_contract_logs(
  api_key=api_key,
  params=params,
)

events_in_block = result2['result'] 
events_in_block


# Sum the amounts staked in the Cake Pool contract (sum of the amount staked in every Deposit event)

total_sum = 0

for dictionary in events_in_block:
    data = dictionary['data']
    decoded_data = decode(['uint256', 'uint256'], bytes.fromhex(data[2:]))
    total_sum += decoded_data[0]

total_sum_decimals = total_sum*1e-18   
    
print(f'Amount of CAKE staked in the block {block_number}: {total_sum_decimals}')





