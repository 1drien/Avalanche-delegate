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
contract MainStaking {
    using SafeERC20 for IERC20;

    IERC20 public immutable QI;
    IERC20 public immutable xQI;
    IERC20 public immutable rewardToken;
    BaseRewardPool public rewarder;
    address private _owner;

    uint256 public cooldownPeriod = 1 days;
    mapping(address => uint256) private _lastClaimTime;

    event ClaimApproved(address indexed user, uint256 amount, bool isApproved);
    event xQIMinted(address user, uint256 xqi_amount);
    event RewardWithdrawed(address user, uint256 avax_amount);
    mapping(address => uint256) public xQIBalance;
    mapping(address => uint256) public claimedReward;

    constructor(IERC20 _qi, IERC20 _xqi, IERC20 _rewardToken) {
        QI = _qi;
        xQI = _xqi;
        rewardToken = _rewardToken;
        _owner = msg.sender;
    }

    function setAddressRewarder(BaseRewardPool _rewarder) external onlyOwner {
        rewarder = _rewarder;
    }

    function depositXQI(uint256 _amount) external {
        xQI.safeTransferFrom(msg.sender, address(this), _amount);
        xQIBalance[msg.sender] += _amount;
        rewarder.stakeFor(msg.sender, _amount);
    }

    function withdrawXQI(uint256 _amount) external {
        xQIBalance[msg.sender] -= _amount;
        xQI.safeTransfer(msg.sender, _amount);
        rewarder.withdrawFor(msg.sender, _amount, true);
    }

    modifier onlyOwner() {
        require(msg.sender == _owner, "Permission Denied");
        _;
    }

    modifier claimCooldown() {
        require(
            block.timestamp >= _lastClaimTime[msg.sender] + cooldownPeriod,
            "Claim cooldown not yet passed"
        );
        _;
    }

    function claim(uint256 amount, address _user) external claimCooldown {
        require(xQIBalance[_user] > 0, "Nothing to claim");
        require(amount > 0, "Claim amount must be strictly positive");
        require(
            xQI.balanceOf(_user) >= amount,
            "Insufficient xQI balance to claim"
        );

        // Deduct the claimed amount from the user's balance
        xQIBalance[_user] -= amount;

        // Update the last claim time
        _lastClaimTime[_user] = block.timestamp;

        emit ClaimApproved(_user, amount, true);

        // Transfer the xQI from this contract to the user
        xQI.safeTransfer(_user, amount);

        // Get the reward amount
        uint256 rewardAmount = rewarder.earned(_user, address(rewardToken));

        claimedReward[_user] += rewardAmount;

        // Withdraw reward from the reward pool
        rewarder.withdrawFor(_user, rewardAmount, true);

        // Transfer the reward from this contract to the user
        rewardToken.safeTransfer(_user, rewardAmount);
    }
}
