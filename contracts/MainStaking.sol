// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./xQI.sol";
import "./QI.sol";
import "./../interfaces/IVeQi.sol";
import "./../interfaces/IMintableERC20.sol";
import "./BaseRewardPool.sol";

/// @title MainStaking

contract MainStaking is Ownable {
    using SafeERC20 for IERC20;
    xQI public xqi;
    address public immutable QI;
    address public immutable VeQi;
    BaseRewardPool public rewarder;
    mapping(address => uint256) public xQIBalance;
    mapping(address => uint256) public claimedReward;

    event xQIMinted(address user, uint256 xqi_amount);
    event RewardWithdrawed(address user, uint256 avax_amount);

    constructor(address _QI, address _VeQi, address _xQI) {
        QI = _QI;
        VeQi = _VeQi;
        xqi = xQI(_xQI);
    }

    function setAddressRewarder(BaseRewardPool _rewarder) external onlyOwner {
        rewarder = _rewarder;
    }

    function depositXQI(uint256 _amount) external {
        IERC20(xqi).safeTransferFrom(msg.sender, address(this), _amount);
        xQIBalance[msg.sender] += _amount;
        rewarder.stakeFor(msg.sender, _amount);
    }

    function withdrawXQI(uint256 _amount) external {
        xQIBalance[msg.sender] -= _amount;
        IERC20(xqi).safeTransfer(msg.sender, _amount);
        rewarder.withdrawFor(msg.sender, _amount, true);
    }




    /// @notice Stake QI in VeQi protocol and mint xQI at a 1:1 rate
    /// @param _amount the amount of QI
    function depositQI(uint256 _amount) external {
        require(_amount > 0, "QI required for deposit");
        IERC20(QI).safeTransferFrom(msg.sender, address(this), _amount);
        IERC20(QI).approve(VeQi, _amount);
        IVeQi(VeQi).deposit(_amount);
        xqi.mintToken(msg.sender, _amount);
        emit xQIMinted(msg.sender, _amount);
    }


    /// @notice User withdraws belonging rewards
    function withdrawReward() external {
        require(xqi.balanceOf(msg.sender) > 0, "xQI required for withdraw");
        uint256 reward = 0;
        claimedReward[msg.sender] += reward;
        emit RewardWithdrawed(msg.sender, reward);
    }
}
