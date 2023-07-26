// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./../contracts/xQI.sol";
import "./../contracts/QI.sol";
import "./../interfaces/IVeQi.sol";

contract MainStaking {
    using SafeERC20 for IERC20;

    IERC20 public immutable QI;
    IERC20 public immutable xQI;
    address private _owner;

    uint256 public cooldownPeriod = 1 days;
    mapping(address => uint256) private _lastClaimTime;

    event ClaimApproved(address indexed user, uint256 amount, bool isApproved);

    constructor(IERC20 _qi, IERC20 _xqi) {
        QI = _qi;
        xQI = _xqi;
        _owner = msg.sender;
    }

    mapping(address => uint256) public balances;

    // Mock depositQI method
    function depositQI(uint256 _amount, address _user) external returns (bool) {
        balances[_user] += _amount;
        return true;
    }

    // Mock withdrawQI method
    function withdrawQI(
        uint256 _amount,
        address _user
    ) external returns (bool) {
        require(balances[_user] >= _amount, "Insufficient balance");
        balances[_user] -= _amount;
        return true;
    }

    // Mock balanceOf method
    function balanceOf(address _user) external view returns (uint256) {
        return balances[_user];
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

    function claimApprove(
        uint256 amount
    ) external onlyOwner claimCooldown returns (bool) {
        require(amount > 0, "Balance must be strictly positive");
        require(
            xQI.balanceOf(msg.sender) >= amount,
            "Insufficient xQI balance to claim"
        );

        _lastClaimTime[msg.sender] = block.timestamp;

        emit ClaimApproved(msg.sender, amount, true);

        return true;
    }

    function claim(uint256 amount) external onlyOwner {
        require(
            amount <= xQI.balanceOf(msg.sender),
            "Claim amount exceeds available balance"
        );

        // Transfer the xQI from this contract to the owner
        xQI.safeTransfer(msg.sender, amount);
    }
}
