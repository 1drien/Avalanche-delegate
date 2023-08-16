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
    user = accounts[0]
    user_with_qi = accounts.at("0x142eb2ed775e6d497aa8d03a2151d016bbfe7fc2", True)
    parameter = {"from": user}
    amount = Wei("10 ether")

    qi = interface.IMintableERC20("0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5")
    veqi = interface.IMintableERC20("0x7Ee65Fdc1C534A6b4f9ea2Cc3ca9aC8d6c602aBd")
    xqi = xQI.deploy(qi.address, veqi.address, parameter)
    qi.transfer(user, amount, {"from": user_with_qi})
    qi.approve(xqi.address, amount, parameter)
    reward_token = interface.IERC20("0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7")

    mainstaking = MainStaking.deploy(
        qi.address, xqi.address, reward_token.address, veqi.address, {"from": user}
    )

    xqi.setOperator(mainstaking)

    return qi, xqi, mainstaking, user, amount
