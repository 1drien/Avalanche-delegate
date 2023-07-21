import pytest
import brownie
from brownie import xQI, Qi, interface, accounts, Wei, Contract, chain, BaseRewardPool, MainStaking


def test_xqi_required():

    ### user with qi
    user = accounts.at("0x142eb2ed775e6d497aa8d03a2151d016bbfe7fc2", True)
    parameter = {"from": user}
    amount = Wei("10 ether")

    qi = interface.IMintableERC20("0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5")
    veqi = interface.IMintableERC20("0x7Ee65Fdc1C534A6b4f9ea2Cc3ca9aC8d6c602aBd")
    xqi = xQI.deploy(qi.address, veqi.address,parameter)

    ### Sets amount as the allowance of spender over the owner's tokens
    qi.approve(xqi.address, amount, parameter)

    ### Stakes QI from user on xQI contract
    xqi.depositQI(amount, user, parameter)
    user_balance = xqi.balanceOf(user)

    mainstaking = MainStaking.deploy(xqi.address, parameter)
    
    ### Test if the require statement passed successfully through the event
    tx = mainstaking.claimApprove(user_balance)
    event_data = tx.events['ClaimApproved']
    value = event_data[0]['amount']
    approval = event_data[0]['isApproved']
    assert value > 0, "Balance must be strictly positive"
    assert approval == True

def test_call_claim():
    user = accounts.at("0x142eb2ed775e6d497aa8d03a2151d016bbfe7fc2", True)
    parameter = {"from": user}
    amount = Wei("10 ether")

    qi = interface.IMintableERC20("0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5")
    veqi = interface.IMintableERC20("0x7Ee65Fdc1C534A6b4f9ea2Cc3ca9aC8d6c602aBd")
    xqi = xQI.deploy(qi.address, veqi.address,parameter)

    qi.approve(xqi.address, amount, parameter)

    xqi.depositQI(amount, user, parameter)
    user_balance = xqi.balanceOf(user)

    mainstaking = MainStaking.deploy(xqi.address, parameter)

    ### Test if only MainStaking can call claim for reward









