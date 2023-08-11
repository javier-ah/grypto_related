#!/usr/bin/env python
# coding: utf-8


# requirements

#$pip install solana
#$pip install "jsonrpcclient"
import solana
from solana.publickey import PublicKey
from solana.rpc.types import MemcmpOpts
from solana.rpc.api import Client
from jsonrpcclient import request, parse, Ok
import logging
import requests



endpoint = "your_endpoint"


# Querying the latest block

# Initialize Solana client with the endpoint URL
client = Client(endpoint)

# Make RPC request to get the latest blockhash
response_getLatestblockhash = solana_client.get_latest_blockhash()

# Access the `slot` attribute within the Response object
context = response_getLatestblockhash.context
slot = context.slot

# Finallly use getBlock method with the latest slot as a parameter
print(solana_client.get_block(slot, "jsonParsed", max_supported_transaction_version=0))



# Get the dictionary of all validator identities using getBlockProduction method
# result is a JSON object containing byIdentity - a dictionary of validator identities, as base-58 encoded strings
# Value is a two element array containing the number of leader slots and the number of blocks produced.

response_getBlockProduction = requests.post(endpoint, json=request("getBlockProduction"))
parsed = parse(response_getBlockProduction.json())
if isinstance(parsed, Ok):
    print('Request successful')
else:
    logging.error(parsed.message)
    
# Get the list of the public keys of all validators
# validator_dict containing number of blocks produced, which may be of interest

validator_dict = parsed.result['value']['byIdentity']
validator_list = list(validator_dict.keys())
print(validator_list)



response_getVoteAccounts = requests.post(endpoint, json=request("getVoteAccounts"))
parsed = parse(response_getVoteAccounts.json())

if isinstance(parsed, Ok):
    print('Request successful')
else:
    logging.error(parsed.message)
    
# Find the biggest validator (considering the biggest validator as the one linked to the vote account 
# with a biggest share of the stake)
vote_accounts_list = parsed.result['current']

vote_accounts_list.sort(key=lambda x: x['activatedStake'], reverse=True)  # Sort the list in descending order by 'activatedStake'
max_vote_pubkey = vote_accounts_list[0]['votePubkey']  # Get the 'votePubkey' of the first element (highest 'activatedStake')
print(f'Vote account with the highest stake: {max_vote_pubkey}')


# Find the delegators for the biggest validator using getProgramAccounts method

from solana.publickey import PublicKey
from solana.rpc.types import MemcmpOpts
from solana.rpc.api import Client

STAKE_PROGRAM_ID: PublicKey = PublicKey("Stake11111111111111111111111111111111111111")

# Create an instance of the Solana client
client = Client(endpoint)
memcmp_opts = [MemcmpOpts(offset=124, bytes=max_vote_pubkey)] 

response_getProgramAccounts = client.get_program_accounts(
    STAKE_PROGRAM_ID,
    encoding="base64",
    data_size=200,
    memcmp_opts=memcmp_opts
)

# Process the program accounts data as needed
print(response_getProgramAccounts)

