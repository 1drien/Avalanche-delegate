// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
// import "@openzeppelinUpgradeable/contracts/proxy/utils/Initializable.sol";

import "./../contracts/xQI.sol";

/// @title MainStaking
/// @notice Mainstaking is the contract that interacts with ALL xQi contract

contract MainStaking {
    using SafeERC20 for IERC20;
    xQI public xqi;
    address public immutable stakingToken;

    constructor (address _stakingToken) {
        stakingToken = _stakingToken;
    }

    event ClaimApproved(address user, uint256 _amount, bool isApproved);

    /// @notice claimApprove checks xQi balance of the sender then call claim in BaseRewardPool
    function claimApprove(uint256 _userBalance) external {
        require(_userBalance > 0, "xQi balance must be positive");
        emit ClaimApproved(msg.sender, _userBalance, true);
    }
}
