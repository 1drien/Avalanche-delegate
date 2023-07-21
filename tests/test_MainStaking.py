import pytest
from brownie import (
    MainStaking,
    BaseRewardPool,
    Qi,
    interface,
    accounts,
    Wei,
    Contract,
    chain,
    BaseRewardPool,
    xQI,
)


def test_deposit_qi(deploy_Mainstaking, fn_isolation):
    mainstaking, qi, user = deploy_Mainstaking
    amount = Wei("10 ether")

    mainstaking.depositQI(amount, {"from": user})
    assert (
        mainstaking.balanceOf(user) == amount
    ), "MainStaking balance is incorrect after deposit"


def test_withdraw(deploy_Mainstaking, fn_isolation):
    mainstaking, qi, user = deploy_Mainstaking
    amount = Wei("10 ether")
    withdraw_amount = Wei("5 ether")

    mainstaking.depositQI(amount, {"from": user})

    initial_balance = qi.balanceOf(user)
    initial_total_staked = mainstaking.totalStaked()

    assert qi.balanceOf(user) == initial_balance + withdraw_amount, "Withdraw failed"
    assert (
        mainstaking.totalStaked() == initial_total_staked - withdraw_amount
    ), "Total staked not updated correctly"


def test_withdraw_more_than_balance(deploy_Mainstaking, fn_isolation):
    mainstaking, qi, user = deploy_Mainstaking
    amount = Wei("10 ether")
    withdraw_amount = Wei("20 ether")

    mainstaking.depositQI(amount, {"from": user})

    # This should fail.
    with reverts("Insufficient balance"):
        mainstaking.withdraw(withdraw_amount, {"from": user})
