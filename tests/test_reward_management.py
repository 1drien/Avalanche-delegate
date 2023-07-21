import pytest
import brownie
from brownie import xQI, Qi, interface, accounts, Wei, Contract, chain, BaseRewardPool, MainStaking


def test_xqi_required():
    ### User with 0 qi
    user1 = accounts[0]
    parameter = {'from':user1}
    
    ### user1 with qi
    user12 = accounts.at("0x142eb2ed775e6d497aa8d03a2151d016bbfe7fc2", True)
    user12_parameters = {"from": user12}
    qi = interface.IMintableERC20("0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5")
   
    ### Transfers amount from user2 to user1
    amount = Wei("10 ether")
    qi.transfer(user1, amount, user12_parameters)

    veqi = interface.IMintableERC20("0x7Ee65Fdc1C534A6b4f9ea2Cc3ca9aC8d6c602aBd")
    xqi = xQI.deploy(qi.address, veqi.address, {"from": user1})

    qi.approve(xqi.address, amount, {"from": user1})

    xqi.depositQI(amount, user1, {"from": user1})
    user1_balance = xqi.balanceOf(user1)
    # avax address : 0x1ce0c2827e2ef14d5c4f29a091d735a204794041

    mainstaking = MainStaking.deploy(xqi.address, parameter)
    
    ### Test if the require statement passed successfully
    # with pytest.raises(brownie.exceptions.VirtualMachineError):
    #     mainstaking.claimApprove(user1_balance, parameter)


