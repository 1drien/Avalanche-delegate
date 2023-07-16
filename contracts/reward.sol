// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./xQI.sol";

/// @title xQI
/// @notice xQI is a token minted when 1 QI is staked in the VeQi protocol
contract Reward {
    using SafeERC20 for IERC20;

    xQI public xqi;

    mapping(address => uint256) public rewards;

    event RewardPaid(address user, uint256 reward);

    constructor(address _xqi) {
        xqi = xQI(_xqi);
    }

    /// @notice
    /// @param
    function calculateReward(address _account) public view returns (uint256) {
        //defining the percentage of rewards
        return xqi.balanceOf(account);
    }

    /// @notice Stake QI in VeQi protocol and mint xQI at a 1:1 rate
    /// @param _amount the amount of QI
    function claimReward() external {
        uint256 reward = calculateReward(msg.sender);
        require(reward > 0, "No rewards");

        rewards[msg.sender] = 0;
        IERC20(xqi).safeTransfer(msg.sender, reward);

        emit RewardPaid(msg.sender, reward);
    }
}
