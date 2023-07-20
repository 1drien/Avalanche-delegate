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


def test_deposit_qi(fn_isolation):
    amount = Wei("10 ether")

    user = accounts[0]
    user_with_qi = accounts.at("0x142eb2ed775e6d497aa8d03a2151d016bbfe7fc2", True)
    user_with_qi_parameters = {"from": user_with_qi}
    qi = interface.IMintableERC20("0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5")
    qi.transfer(user, amount, user_with_qi_parameters)
    veqi = interface.IMintableERC20("0x7Ee65Fdc1C534A6b4f9ea2Cc3ca9aC8d6c602aBd")
    xqi = xQI.deploy(qi.address, veqi.address, {"from": user})

    staking_token_address = xqi.address
    reward_token_address = "0x1ce0c2827e2ef14d5c4f29a091d735a204794041"
    operator_address = accounts[1]
    reward_manager_address = accounts[2]
    assert qi.balanceOf(user) == amount, "Transfer failed"

    base_reward_pool = accounts[0].deploy(
        BaseRewardPool,
        staking_token_address,
        reward_token_address,
        operator_address,
        reward_manager_address,
    )

    mainstaking = MainStaking.deploy({"from": user})

    qi.approve(mainstaking.address, amount, {"from": user})
    assert qi.allowance(user, mainstaking.address) == amount, "Approval failed"

    mainstaking.depositQI(amount, {"from": user})
    assert (
        mainstaking.balanceOf(user) == amount
    ), "MainStaking balance is incorrect after deposit"


def test_withdraw_more_than_balance(fn_isolation):
    amount = Wei("10 ether")
    withdraw_amount = Wei("20 ether")

    user = accounts[0]
    user_with_qi = accounts.at("0x142eb2ed775e6d497aa8d03a2151d016bbfe7fc2", True)
    user_with_qi_parameters = {"from": user_with_qi}
    qi = interface.IMintableERC20("0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5")
    qi.transfer(user, amount, user_with_qi_parameters)

    staking_token_address = qi.address
    reward_token_address = "0x1ce0c2827e2ef14d5c4f29a091d735a204794041"
    operator_address = accounts[1]
    reward_manager_address = accounts[2]

    base_reward_pool = accounts[0].deploy(
        BaseRewardPool,
        staking_token_address,
        reward_token_address,
        operator_address,
        reward_manager_address,
    )

    mainstaking = MainStaking.deploy({"from": user})

    qi.approve(mainstaking.address, amount, {"from": user})
    mainstaking.depositQI(amount, {"from": user})

    # This should fail.
    with reverts("Insufficient balance"):
        mainstaking.withdraw(withdraw_amount, {"from": user})
