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
    reverts,
)


def test_xqi_required(setup_contracts, fn_isolation):
    qi, xqi, mainstaking, user, amount = setup_contracts
    value = Wei("10 ether")

    assert mainstaking.balanceOf(user) == value
    xqi.depositQI(amount, user, {"from": user})
    user_balance = xqi.balanceOf(user)

    ### Test if the require statement passed successfully through the event
    tx = mainstaking.claim(user_balance)
    event_data = tx.events["ClaimApproved"]
    value = event_data[0]["amount"]
    approval = event_data[0]["isApproved"]
    assert value > 0, "Balance must be strictly positive"
    assert approval == True


def test_multiple_claims(setup_contracts, fn_isolation):
    qi, xqi, mainstaking, user, amount = setup_contracts
    value = Wei("10 ether")

    assert mainstaking.balanceOf(user) == value
    xqi.depositQI(amount, user, {"from": user})
    user_balance = xqi.balanceOf(user)

    ###First claim
    tx1 = mainstaking.claim(user_balance)
    event_data1 = tx1.events["ClaimApproved"]
    value1 = event_data1[0]["amount"]
    approval1 = event_data1[0]["isApproved"]
    assert value1 > 0, "Balance must be strictly positive"
    assert approval1 == True

    ### second claim
    with reverts("Claim cooldown not yet passed"):
        tx2 = mainstaking.claim(user_balance)


def test_claim_without_deposit(setup_contracts, fn_isolation):
    qi, xqi, mainstaking, user, _ = setup_contracts
    other_user = accounts[1]

    ### Trying to claim without deposit
    with reverts("Nothing to claim"):
        mainstaking.claim(0, {"from": other_user})


def test_claim_after_withdraw(setup_contracts, fn_isolation):
    qi, xqi, mainstaking, user, amount = setup_contracts
    value = Wei("10 ether")

    assert mainstaking.balanceOf(user) == value
    xqi.depositQI(amount, user, {"from": user})

    xqi.withdrawQI(amount, {"from": user})

    ### Trying to claim after withdrawal
    with reverts("Nothing to claim"):
        mainstaking.claim(0, {"from": user})


def test_claim_with_incorrect_qi_value(setup_contracts, fn_isolation):
    qi, xqi, mainstaking, user, _ = setup_contracts
    deposit_value = Wei("10 ether")
    incorrect_value = Wei(
        "20 ether"
    )  ### This value is incorrect because user only deposited 10 ether

    xqi.depositQI(deposit_value, {"from": user})

    with reverts("Claim amount exceeds available balance"):
        mainstaking.claim(incorrect_value, {"from": user})


def test_claim_after_qi_balance_change(setup_contracts, fn_isolation):
    qi, xqi, mainstaking, user, _ = setup_contracts
    initial_deposit = Wei("10 ether")
    additional_deposit = Wei("5 ether")

    xqi.depositQI(initial_deposit, {"from": user})

    ### User deposits more QI
    xqi.depositQI(additional_deposit, {"from": user})

    claim_tx = mainstaking.claim(initial_deposit + additional_deposit, {"from": user})

    ### Assert the claim was successful
    event_data = claim_tx.events["ClaimApproved"]
    claimed_amount = event_data[0]["amount"]
    approval = event_data[0]["isApproved"]
    assert (
        claimed_amount == initial_deposit + additional_deposit
    ), "Claimed amount is incorrect"
    assert approval == True, "Claim was not approved"
