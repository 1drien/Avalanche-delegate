// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "./../interfaces/IVeQi.sol";
import "./../contracts/QI.sol";

/// @title xQI
/// @notice xQI is a token minted when 1 QI is staked in the VeQi protocol
contract xQI is ERC20 {
    using SafeERC20 for IERC20;
    address public immutable QI;
    address public immutable VeQi;

    event xQIminted(address indexed user, uint256 amount);

    constructor(address _QI, address _VeQi) ERC20("xQI", "xQI") {
        QI = _QI;
        VeQi = _VeQi;
    }

    /// @notice Stake QI in VeQi protocol and mint xQI at a 1:1 rate
    /// @param _amount the amount of QI
    function depositQI(uint256 _amount, address _for) external {
        IERC20(QI).safeTransferFrom(msg.sender, address(this), _amount);
        IERC20(QI).approve(VeQi, _amount);
        IVeQi(VeQi).deposit(_amount);
        _mint(_for, _amount);
        emit xQIminted(_for, _amount);
    }
}
