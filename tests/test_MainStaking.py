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
    reverts
)

amount = Wei("10 ether")
deposit_amount1 = Wei("10 ether")
deposit_amount2 = Wei("5 ether")


def test_depositXQI(deploy_mainstaking, fn_isolation):
    mainstaking, qi, xqi, user = deploy_mainstaking
    parameter = {"from" : user}

    mainstaking.depositQI(amount, parameter)
    initial_balance = xqi.balanceOf(user)
    xqi.approve(mainstaking, amount, parameter)
    mainstaking.depositXQI(amount, parameter)
    assert(xqi.balanceOf(user) == initial_balance - amount, "User xQI Balance is incorrect")
    assert(xqi.balanceOf(mainstaking) == amount, "MainStaking xQI Balance is incorrect")


def test_withdrawXQI(deploy_mainstaking, fn_isolation):
    mainstaking, qi, xqi, user = deploy_mainstaking
    parameter = {"from" : user}

    mainstaking.depositQI(amount, parameter)
    xqi.approve(mainstaking, amount, parameter)
    mainstaking.depositXQI(amount, parameter)


    mainstaking.withdrawXQI(amount, parameter)
    assert(xqi.balanceOf(user) == amount, "User xQI Balance is incorrect")
    assert(xqi.balanceOf(mainstaking) == 0, "MainStaking xQI Balance is incorrect")


def test_more_than_balance_withdrawXQI(deploy_mainstaking, fn_isolation):
    mainstaking, qi, xqi, user = deploy_mainstaking
    parameter = {"from" : user}

    mainstaking.depositQI(amount, parameter)
    xqi.approve(mainstaking, amount, parameter)
    mainstaking.depositXQI(amount, parameter)

    with reverts("Witdraw amount axceeds balance"):
        mainstaking.withdrawXQI(amount*2, parameter)


def test_only_owner(deploy_mainstaking, fn_isolation):
    user = accounts[0]
    qi = interface.IMintableERC20("0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5")

    veqi = interface.IMintableERC20("0x7Ee65Fdc1C534A6b4f9ea2Cc3ca9aC8d6c602aBd")
    xqi = xQI.deploy(qi.address, veqi.address, {"from": user})
    mainstaking = MainStaking.deploy(qi.address, veqi.address, xqi, {"from": user})
    xqi.setOperator(mainstaking)

    staking_token_address = qi.address
    reward_token_address = "0x1ce0c2827e2ef14d5c4f29a091d735a204794041"
    operator_address = mainstaking
    reward_manager_address = accounts[2]

    base_reward_pool = accounts[0].deploy(
        BaseRewardPool,
        staking_token_address,
        reward_token_address,
        operator_address,
        reward_manager_address,
    )

    with reverts("Only callable by owner / MainStaking"):
        mainstaking.setRewarder(base_reward_pool, {"from" : user})


def test_depositXQI_zero_amount(deploy_mainstaking, fn_isolation):
    mainstaking, qi, xqi, user = deploy_mainstaking
    parameter = {"from" : user}

    mainstaking.depositQI(amount, parameter)
    initial_balance = xqi.balanceOf(user)
    xqi.approve(mainstaking, amount, parameter)
    with reverts("Cannnot deposit 0 token"):
        mainstaking.depositXQI(0, parameter)


def test_withdrawXQI_zero_amount(deploy_mainstaking, fn_isolation):
    mainstaking, qi, xqi, user = deploy_mainstaking
    parameter = {"from" : user}

    mainstaking.depositQI(amount, parameter)
    xqi.approve(mainstaking, amount, parameter)
    mainstaking.depositXQI(amount, parameter)

    with reverts("Cannot withdraw 0 token"):
        mainstaking.withdrawXQI(0, parameter)


# For the first deposit, compares MainStaking balance and deposit amount
def test_deposit_qi(deploy_mainstaking, fn_isolation):
    mainstaking, qi, xqi, user = deploy_mainstaking
    mainstaking.depositQI(amount, {"from": user})
    assert (
        qi.balanceOf(mainstaking.address) == xqi.balanceOf(user)
    ), "MainStaking balance is incorrect after deposit"


# Checks balances during withdraw
def test_withdraw(deploy_mainstaking, fn_isolation):
    mainstaking, qi, user = deploy_mainstaking
    withdraw_amount = Wei("5 ether")

    mainstaking.depositQI(amount, {"from": user})

    initial_balance = qi.balanceOf(user)
    initial_total_staked = mainstaking.totalStaked()

    assert qi.balanceOf(user) == initial_balance + withdraw_amount, "Withdraw failed"
    assert (
        mainstaking.totalStaked() == initial_total_staked - withdraw_amount
    ), "Total staked not updated correctly"


# Asks a withdraw amount above user balance
def test_withdraw_more_than_balance(deploy_mainstaking, fn_isolation):
    mainstaking, qi, user = deploy_mainstaking
    withdraw_amount = Wei("20 ether")

    mainstaking.depositQI(amount, {"from": user})

    # This should fail.
    with reverts("Insufficient balance"):
        mainstaking.withdraw(withdraw_amount, {"from": user})


# Checks balance after multiple QI deposit
def test_multiple_deposits(deploy_mainstaking, fn_isolation):
    mainstaking, qi, user = deploy_mainstaking

    mainstaking.depositQI(deposit_amount1, {"from": user})
    mainstaking.depositQI(deposit_amount2, {"from": user})

    assert (
        mainstaking.balanceOf(user) == deposit_amount1 + deposit_amount2
    ), "Balance is incorrect after multiple deposits"


# Checks balances for multiple users
def test_multiple_users_deposit(deploy_mainstaking, fn_isolation, accounts):
    mainstaking, qi, user1 = deploy_mainstaking
    user2 = accounts[1]
    user2_with_qi_parameters = {"from": user1}

    qi.transfer(user2, deposit_amount2, user2_with_qi_parameters)
    qi.approve(mainstaking.address, deposit_amount2, {"from": user2})

    # User's deposits
    mainstaking.depositQI(deposit_amount1, {"from": user1})
    mainstaking.depositQI(deposit_amount2, {"from": user2})

    assert (
        mainstaking.balanceOf(user1) == deposit_amount1
    ), "Balance of user1 is incorrect after deposit"
    assert (
        mainstaking.balanceOf(user2) == deposit_amount2
    ), "Balance of user2 is incorrect after deposit"



# Throws an error when asking to withdraw zero
def test_withdraw_zero(deploy_mainstaking, fn_isolation):
    mainstaking, qi, user = deploy_mainstaking
    withdraw_amount = Wei("0 ether")

    mainstaking.depositQI(amount, {"from": user})

    # This should fail.
    with reverts("Must withdraw more than zero"):
        mainstaking.withdraw(withdraw_amount, {"from": user})
    