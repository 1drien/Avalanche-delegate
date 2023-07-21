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


@pytest.fixture(autouse=True)
def isolation(
    fn_isolation,
):  # TO BE REPLACED BY py_vector.common.testing simple_isolation if issues
    pass


@pytest.fixture
def setup_contracts(accounts, interface, xQI, MainStaking):
    user = accounts.at("0x142eb2ed775e6d497aa8d03a2151d016bbfe7fc2", True)
    parameter = {"from": user}
    amount = Wei("10 ether")

    qi = interface.IMintableERC20("0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5")
    veqi = interface.IMintableERC20("0x7Ee65Fdc1C534A6b4f9ea2Cc3ca9aC8d6c602aBd")
    xqi = xQI.deploy(qi.address, veqi.address, parameter)

    qi.approve(xqi.address, amount, parameter)

    mainstaking = MainStaking.deploy(xqi.address, parameter)

    return qi, xqi, mainstaking, user, amount
