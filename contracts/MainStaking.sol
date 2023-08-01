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

    xQI public xqi;
    address public immutable QI;
    address public immutable VeQi;
    address public immutable rewardToken;
    BaseRewardPool public rewarder;
    address private _owner;

    uint256 public cooldownPeriod = 1 days;
    mapping(address => uint256) private _lastClaimTime;

    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);
    event ClaimApproved(address indexed user, uint256 amount, bool isApproved);
    event xQIMinted(address user, uint256 xqi_amount);
    event RewardWithdrawed(address user, uint256 avax_amount);

    mapping(address => uint256) public xQIBalance;
    mapping(address => uint256) public claimedReward;

    constructor(
        address _QI,
        address _xQI,
        address _rewardToken,
        address _VeQi
    ) {
        QI = _QI;
        xqi = xQI(_xQI);
        rewardToken = _rewardToken;
        VeQi = _VeQi;
        _owner = msg.sender;
    }

    function setAddressRewarder(BaseRewardPool _rewarder) external onlyOwner {
        rewarder = _rewarder;
    }

    function depositXQI(uint256 _amount) external {
        IERC20(xqi).safeTransferFrom(msg.sender, address(this), _amount);
        xQIBalance[msg.sender] += _amount;
        rewarder.stakeFor(msg.sender, _amount);
        emit Deposit(msg.sender, _amount);
    }

    function withdrawXQI(uint256 _amount) external {
        xQIBalance[msg.sender] -= _amount;
        IERC20(xqi).safeTransfer(msg.sender, _amount);
        rewarder.withdrawFor(msg.sender, _amount, true);
        emit Withdrawal(msg.sender, _amount);
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

    /// @notice Stake QI in VeQi protocol and mint xQI at a 1:1 rate
    /// @param _amount the amount of QI
    function depositQI(uint256 _amount) external {
        IERC20(QI).safeTransferFrom(msg.sender, address(this), _amount);
        IERC20(QI).approve(VeQi, _amount);
        IVeQi(VeQi).deposit(_amount);
        xqi.mintToken(msg.sender, _amount);
        emit xQIMinted(msg.sender, _amount);
    }

    function claim(uint256 amount, address _user) external claimCooldown {
        require(xQIBalance[_user] > 0, "Nothing to claim");
        require(amount > 0, "Claim amount must be strictly positive");
        require(
            xqi.balanceOf(_user) >= amount,
            "Insufficient xQI balance to claim"
        );

        // Deduct the claimed amount from the user's balance
        xQIBalance[_user] -= amount;

        // Update the last claim time
        _lastClaimTime[_user] = block.timestamp;

        emit ClaimApproved(_user, amount, true);

        // Transfer the xQI from this contract to the user
        IERC20(xqi).safeTransfer(_user, amount);

        // Get the reward amount
        uint256 rewardAmount = rewarder.earned(_user, address(rewardToken));

        claimedReward[_user] += rewardAmount;

        // Withdraw reward from the reward pool
        rewarder.withdrawFor(_user, rewardAmount, true);

        // Transfer the reward from this contract to the user
        IERC20(rewardToken).safeTransfer(_user, rewardAmount);
    }
}
