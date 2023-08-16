from brownie import xQI, Qi, accounts


def main():
    deployer = accounts[0]
    qi_address = "0x8729438EB15e2C8B576fCc6AeCdA6A148776C0F5"
    veqi_address = "0x7Ee65Fdc1C534A6b4f9ea2Cc3ca9aC8d6c602aBd"

    xqi = xQI.deploy(qi_address, veqi_address, {"from": deployer})

    print(f"xQI deployed at: {xqi.address}")
