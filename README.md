# ❄️ QI Staking Contract on Avalanche

## Overview

This smart contract implements a staking mechanism for QI tokens on the Avalanche C-Chain. Users can stake their QI and receive xQI tokens in return, which represent their share in the staking pool. Over time, as rewards are added to the pool, the value of xQI relative to QI increases, allowing users to redeem more QI than they initially deposited.

---

## Features

- ✅ Stake QI tokens and receive xQI.
- 🔁 Redeem QI by burning xQI.
- 📈 Auto-compounding rewards reflected in xQI value.
- 🔒 Designed for long-term staking incentives.
- ⚙️ Built on Avalanche C-Chain using Solidity.

---

## How it Works

1. **Staking QI:**
   - Users call `stake(uint256 _amount)`.
   - QI is transferred to the contract.
   - The user receives xQI calculated as:  
     ```
     xQI = (_amount * totalSupply_xQI) / totalQIinContract
     ```
     (If total xQI is 0, user receives 1:1 xQI)

2. **Unstaking:**
   - Users call `unstake(uint256 _xqiAmount)`.
   - xQI is burned.
   - User receives QI proportional to their share.

3. **Reward Accumulation:**
   - Rewards (e.g., via external functions or admin deposit) increase QI in the contract.
   - xQI value appreciates over time.

---

## Installation & Deployment

```bash
git clone https://github.com/yourusername/qi-staking-avalanche.git
cd qi-staking-avalanche
npm install
