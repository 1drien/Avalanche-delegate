import pytest
from brownie import Reward, xQI, Contract, accounts, Wei, interface


def test_reward_calculation():
    user = accounts[0]

    reward = 0

    reward_amount = reward.calculateReward(user)
    assert reward_amount == Wei("10 ether"), "Reward amount is incorrect"


def test_reward_claim():
    user = accounts[0]
