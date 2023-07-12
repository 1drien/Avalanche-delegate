import pytest
from brownie import xQI, Qi, interface, accounts, Wei


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
