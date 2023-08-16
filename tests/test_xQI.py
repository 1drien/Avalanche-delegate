import pytest
import brownie
from brownie import xQI, Qi, interface, accounts, Wei, Contract, chain


def test_deposit_qi(fn_isolation):
    amount = Wei("10 ether")

    user = accounts[0]
    user_with_qi = accounts.at("0x142eb2ed775e6d497aa8d03a2151d016bbfe7fc2", True)
    user_with_qi_parameters = {"from": user_with_qi}
    qi = interface.IMintableERC20("0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5")
    qi.transfer(user, amount, user_with_qi_parameters)

    assert qi.balanceOf(user) == amount, "Transfer failed"

    veqi = interface.IMintableERC20("0x7Ee65Fdc1C534A6b4f9ea2Cc3ca9aC8d6c602aBd")
    xqi = xQI.deploy(qi.address, veqi.address, {"from": user})

    qi.approve(xqi.address, amount, {"from": user})
    assert qi.allowance(user, xqi.address) == amount, "Approval failed"

    xqi.depositQI(amount, user, {"from": user})
    assert xqi.balanceOf(user) == amount, "xQI balance is incorrect after deposit"


# PASS

# def test_insufficient_balance():
#     user = accounts[0]
#     amount = Wei("10 ether")
#     qi_address = "0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5"
#     veqi_address = "0x7Ee65Fdc1C534A6b4f9ea2Cc3ca9aC8d6c602aBd"

#     qi = Contract.from_abi(
#         "IMintableERC20", qi_address, abi=interface.IMintableERC20.abi, owner=user
#     )
#     veqi = Contract.from_abi(
#         "IMintableERC20", veqi_address, abi=interface.IMintableERC20.abi, owner=user
#     )
#     xqi = xQI.deploy(qi.address, veqi.address, {"from": user})

#     qi.mint(user, amount)

#     qi.transfer(user, amount / 2)

#     qi.approve(xqi.address, amount, {"from": user})

#     with pytest.raises(Exception):
#         xqi.depositQI(amount, user, {"from": user})


# def test_deposit_qi_for_other_account():

#     user = accounts[0]
#     recipient = accounts[1]

#     qi_address = "0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5"
#     veqi_address = "0x7Ee65Fdc1C534A6b4f9ea2Cc3ca9aC8d6c602aBd"

#     qi = Contract.from_abi(
#         "IMintableERC20", qi_address, abi=interface.IMintableERC20.abi, owner=user
#     )
#     veqi = Contract.from_abi(
#         "IMintableERC20", veqi_address, abi=interface.IMintableERC20.abi, owner=user
#     )
#     xqi = xQI.deploy(qi.address, veqi.address, {"from": user})

#     amount = Wei("10 ether")

#     qi.mint(user, amount)
#     qi.approve(xqi.address, amount, {"from": user})

#     xqi.depositQI(amount, recipient, {"from": user})
#     assert xqi.balanceOf(recipient) == amount

#     assert xqi.balanceOf(user) == 0
