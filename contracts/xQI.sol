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
    address public immutable operator;

    constructor(
        address _QI,
        address _VeQi,
        address _operator) 
        ERC20("xQI", "xQI") 
    {
        QI = _QI;
        VeQi = _VeQi;
        operator = _operator;
    }

    modifier onlyOperator() {
        require(msg.sender == operator, "Only Operator");
        _;
    }

    /// @notice Stake QI in VeQi protocol and mint xQI at a 1:1 rate
    /// @param _amount the amount of QI
    function mintToken(address _for, uint256 _amount) external onlyOperator {
        _mint(_for, _amount);
    }
}
