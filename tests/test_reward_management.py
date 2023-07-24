import pytest
import brownie
from brownie import (
    xQI,
    Qi,
    interface,
    accounts,
    Wei,
    Contract,
    chain,
    BaseRewardPool,
    MainStaking,
)


def test_xqi_required(setup_contracts, fn_isolation):
    qi, xqi, mainstaking, user, amount = setup_contracts
    value = Wei("10 ether")

    assert mainstaking.balanceOf(user) == value
    xqi.depositQI(amount, user, {"from": user})
    user_balance = xqi.balanceOf(user)

    ### Test if the require statement passed successfully through the event
    tx = mainstaking.claimApprove(user_balance)
    event_data = tx.events["ClaimApproved"]
    value = event_data[0]["amount"]
    approval = event_data[0]["isApproved"]
    assert value > 0, "Balance must be strictly positive"
    assert approval == True


def test_call_claim(setup_contracts):
    qi, xqi, mainstaking, user, _ = setup_contracts
    other_user = accounts[1]

    with reverts("Only MainStaking can call this function"):
        mainstaking.claim({"from": other_user})


def test_call_claim_by_other(setup_contracts):
    qi, xqi, mainstaking, user, _ = setup_contracts
    other_user = accounts[1]

    with reverts("Permission Denied"):
        mainstaking.someAction({"from": other_user})


def test_multiple_claims(setup_contracts, fn_isolation):
    qi, xqi, mainstaking, user, amount = setup_contracts
    value = Wei("10 ether")

    assert mainstaking.balanceOf(user) == value
    xqi.depositQI(amount, user, {"from": user})
    user_balance = xqi.balanceOf(user)

    ###First claim
    tx1 = mainstaking.claimApprove(user_balance)
    event_data1 = tx1.events["ClaimApproved"]
    value1 = event_data1[0]["amount"]
    approval1 = event_data1[0]["isApproved"]
    assert value1 > 0, "Balance must be strictly positive"
    assert approval1 == True

    # second claim
    with reverts("Claim cooldown not yet passed"):
        tx2 = mainstaking.claimApprove(user_balance)


def test_claim_without_deposit(setup_contracts, fn_isolation):
    qi, xqi, mainstaking, user, _ = setup_contracts
    other_user = accounts[1]

    # Trying to claim without deposit
    with reverts("Nothing to claim"):
        mainstaking.claimApprove(0, {"from": other_user})


def test_claim_after_withdraw(setup_contracts, fn_isolation):
    qi, xqi, mainstaking, user, amount = setup_contracts
    value = Wei("10 ether")

    assert mainstaking.balanceOf(user) == value
    xqi.depositQI(amount, user, {"from": user})

    xqi.withdrawQI(amount, {"from": user})

    # Trying to claim after withdrawal
    with reverts("Nothing to claim"):
        mainstaking.claimApprove(0, {"from": user})


def test_claim_with_incorrect_qi_value(setup_contracts, fn_isolation):
    qi, xqi, mainstaking, user, _ = setup_contracts
    deposit_value = Wei("10 ether")
    incorrect_value = Wei(
        "20 ether"
    )  # This value is incorrect because user only deposited 10 ether

    xqi.depositQI(deposit_value, {"from": user})

    with reverts("Incorrect QI value"):
        mainstaking.claimApprove(incorrect_value, {"from": user})
