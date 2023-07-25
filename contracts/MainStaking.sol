// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelinUpgradeable/contracts/proxy/utils/Initializable.sol";
import "./../contracts/xQI.sol";
import "./../contracts/QI.sol";
import "./../interfaces/IVeQi.sol";
import "./../interfaces/IMintableERC20.sol";

/// @title MainStaking

contract MainStaking is Initializable {
    using SafeERC20 for IERC20;
    xQI private xqi;
    address public immutable QI;
    address public immutable VeQi;

    constructor(address _QI, address _VeQi, address _xQI) {
        QI = _QI;
        VeQi = _VeQi;
        xqi = xQI(_xQI);
    }

    event xQIMinted(address indexed user, uint256 amount);

    /// @notice Stake QI in VeQi protocol and mint xQI at a 1:1 rate
    /// @param _amount the amount of QI
    function depositQI(uint256 _amount, address _for) external {
        IERC20(QI).safeTransferFrom(msg.sender, address(this), _amount);
        IERC20(QI).approve(VeQi, _amount);
        IVeQi(VeQi).deposit(_amount);
        xqi.mintToken(_for, _amount);
        xqi.transferToMainStaking(address(this), _amount);
        emit xQIMinted(_for, _amount);
    }
}
