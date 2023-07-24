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
