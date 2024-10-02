from datetime import datetime

from type_handling.instances import PARAM_DOMAIN, OrderType, PARAM_DOMAIN_JAM
from type_handling.order_types import SINGLE_ORDER_TYPES, MULTI_ORDER_TYPES, AGGREGATE_ORDER_TYPES, PERMIT, JAM_ORDER_TYPES
from type_handling.my_types import Chain, Token
from eth_account.signers.local import LocalAccount
from eth_account import Account


class Signer:
    def __init__(self, account: LocalAccount):
        self.account = account

    def _permit_data(self, spender: str, value: int, deadline: int) -> dict:
        return {
            "owner": self.account.address,
            "spender": spender,
            "value": value,
            "nonce": self._get_nonce(),
            "deadline": deadline,
        }

    def _get_nonce(self) -> int:
        with open("nonce.txt", 'r+') as file:
            nonce = int(file.read())
            file.seek(0)
            file.write(str(nonce + 1))
        return nonce

    def _permit_domain(self, name: str, version: str, chain: Chain, address: str) -> dict:
        return {
            "name": name,
            "version": version,
            "chainId": chain.chain_id,
            "verifyingContract": address,
        }

    def sign_order(self, order_type: OrderType, msg_data: dict, jam: bool) -> str:
        if order_type == OrderType.SINGLE_ORDER_TYPES:
            if jam: msg_types = JAM_ORDER_TYPES
            else: msg_types = SINGLE_ORDER_TYPES
        else:
            raise ValueError("Unsupported order type")
        return Account.sign_typed_data(self.account._private_key, PARAM_DOMAIN_JAM if jam else PARAM_DOMAIN, msg_types, msg_data).signature.hex()

    def sign_permit(self, spender: str, value: int, deadline: int, token: Token, chain: Chain) -> str:
        permit_domain = self._permit_domain(token.name, "1", chain, token.address)
        return Account.sign_typed_data(self.account._private_key, permit_domain, PERMIT, self._permit_data(spender, value, deadline)).signature.hex()