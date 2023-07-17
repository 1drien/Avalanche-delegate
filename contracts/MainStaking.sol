// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./../contracts/xQI.sol";
import "./../contracts/QI.sol";
import "./../contracts/reward.sol";
import "./../contracts/WAVAX.sol";

/// @title MainStaking

contract MainStaking {
    using SafeERC20 for IERC20;
    address public immutable qi;
    address public immutable xQI;

    mapping(address => bool) public whitelist;

    constructor(address _qi, address _xQI, address _wavax) {
        qi = IERC20(_qi);
        xqi = xQI(_xQI);
        wavax = WAVAX(_wavax);
    }

    function addToWhitelist(address _user) external {
        whitelist[_user] = true;
    }

    function removeFromWhitelist(address _user) external {
        whitelist[_user] = false;
    }

    function stakeQI(uint256 _amount) external {
        require(whitelist[msg.sender] == true, "User not whitelisted");
        qi.safeTransferFrom(msg.sender, address(this), _amount);
        qi.approve(xQi, _amount);
        xqi.depositQI(_amount, msg.sender);
    }

    function getReward() external {
        require(whitelist[msg.sender] == true, "User not whitelisted");
        reward.claimReward(msg.sender);
    }

    function withdrawReward(uint256 _reward) external {
        require(whitelist[msg.sender] == true, "User not whitelisted");
        require(_reward > 0);
        wavax.withdraw(_reward);
    }
}
