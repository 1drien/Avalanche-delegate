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

    function deposit(uint256 amount) public {
        require(
            QI.transferFrom(msg.sender, address(this), amount),
            "Transfer failed"
        );
        balances[msg.sender] += amount;
    }

    function withdrawQI(
        uint256 _amount,
        address _user
    ) external returns (bool) {
        require(balances[_user] >= _amount, "Insufficient balance");
        balances[_user] -= _amount;
        return true;
    }

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

    function claim(uint256 amount, address _user) external claimCooldown {
        require(balances[_user] > 0, "Nothing to claim");
        require(amount > 0, "Claim amount must be strictly positive");
        require(
            xQI.balanceOf(_user) >= amount,
            "Insufficient xQI balance to claim"
        );

        // Deduct the claimed amount from the user's balance
        balances[_user] -= amount;

        // Update the last claim time
        _lastClaimTime[_user] = block.timestamp;

        emit ClaimApproved(_user, amount, true);

        // Transfer the xQI from this contract to the user
        xQI.safeTransfer(_user, amount);
    }
}
