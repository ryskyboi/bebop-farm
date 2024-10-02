from dotenv import load_dotenv
from os import getenv
from eth_account import Account
from enum import Enum
from pathlib import Path

import type_handling.my_types as my_types
import type_handling.addresses as addresses


load_dotenv()

ARBITRUM = my_types.Chain("arbitrum", 42161)

USDC = my_types.Token("USDC", addresses.USDC, 6)
USDT= my_types.Token("USDT", addresses.USDT, 6)
WETH = my_types.Token("WETH", addresses.WETH, 18)

ACCOUNT = Account.from_key(getenv("PRIVATE_KEY"))

PARAM_DOMAIN = {
    "name": "BebopSettlement",
    "version": "2",
    "chainId": ARBITRUM.chain_id,
    "verifyingContract": addresses.BEBOP,
}

PARAM_DOMAIN_JAM = {
    "name": "JamSettlement",
    "version": "1",
    "chainId": ARBITRUM.chain_id,
    "verifyingContract": addresses.BEBOP_JAM_SETTLEMENT,
}

class OrderType(Enum):
    SINGLE_ORDER_TYPES = 1
    MULTI_ORDER_TYPES = 2
    AGGREGATE_ORDER_TYPES = 3


class ApprovalType(Enum):
    Standard = "Standard"
    Permit = "Permit"
    Permit2 = "Permit2"
