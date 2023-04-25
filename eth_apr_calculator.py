#!/usr/bin/env python
# coding: utf-8



# Set the constants and input parameters

base_reward_factor = 64 #constant
base_rewards_per_epoch = 4 #constant
average_effective_balance = 32e9 #constant, for simplicity. In Gwei
percentage_staked = 50 #evolving_factor
total_supply = 120.21e6 * 1e9 #evolving factor. In Gwei
total_active_balance = percentage_staked / 100 * total_supply #7.1e6*1e9 
total_attesting_balance = total_active_balance #assuming 100% participation
proposer_reward_quotient = 8 #constant
number_of_validators = total_active_balance / average_effective_balance
number_of_attestors = number_of_validators / 32 #assuming 100% participation. 1 in 32 of all validators voting in each block
frequency_of_proposer = 1 / number_of_validators #again, oversimplifying
epochs_per_day = 24 * 60 / 6.4 #constant
epochs_per_year = epochs_per_day * 365 #constant


# Calculate base reward

base_reward = (base_reward_factor * average_effective_balance) / (base_rewards_per_epoch * (total_active_balance **(1/2)))



# Calculate rewards per proposer (per epoch)

rewards_per_proposer = (base_reward * number_of_attestors) / (proposer_reward_quotient)


# Calculate rewards per attestor (per epoch)


rewards_per_attestor = (3 * base_reward * total_attesting_balance / total_active_balance) + (7 * base_reward / 8) # oversimplifying the three different categories os a correct attestation


# Calculate total rewards per epoch

rewards_per_epoch = rewards_per_attestor + frequency_of_proposer*rewards_per_proposer


# Calculate rewards per year and APR

reward_per_year = rewards_per_epoch * epochs_per_year
APR = reward_per_year / average_effective_balance *100

print(f'The APR for staking ETH assuming {percentage_staked}% of the supply is staked, with the current supply of {total_supply*1e-9} ETH is approximately: {APR}%')



