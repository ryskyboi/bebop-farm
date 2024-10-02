from typing import Any, Dict, Tuple, Union
from eth_account.signers.local import LocalAccount
from pathlib import Path
import json
from requests import get, post
from time import sleep
from pprint import pprint
from requests import Response
from type_handling.my_types import Chain, Token
from type_handling.instances import ApprovalType
from type_handling.my_types import PermitToken, PermitNeeded


class RPC:
    def __init__(self, chain: Chain, account: LocalAccount) -> None:
        self.chain: Chain = chain
        self.account: LocalAccount = account

    def _params(self, buy_tokens: Token, sell_tokens: Token, sell_amounts: Union[int, float], approval_type: ApprovalType) -> Dict[str, Union[str, int]]:
        return {
            "buy_tokens": buy_tokens.address,
            "sell_tokens": sell_tokens.address,
            "sell_amounts": sell_tokens.to_wei(sell_amounts),
            "taker_address": self.account.address,
            "approval_type": approval_type.value,
        }

    def _quote_url(self, is_quote: bool, jam: bool=False) -> str:
        if jam: return f"https://api.bebop.xyz/jam/{self.chain.name}/v1/{'quote' if is_quote else 'order'}"
        return f"https://api.bebop.xyz/pmm/{self.chain.name}/v3/{'quote' if is_quote else 'order'}"

    def _send_tx(self, data: dict, is_get: bool, is_quote: bool, jam: bool) -> dict[str, Any]:
        response: Response
        if is_get: response = get(self._quote_url(is_quote, jam), params=data)
        else: response = post(self._quote_url(is_quote, jam), json=data, headers = {'Content-Type': 'application/json; charset=utf-8'} if jam else None)
        if response.status_code != 200:
            if is_get: raise Exception(f"Failed to get quote: {response.text}")
            print("Failed to send transaction")
            pprint(response)
            sleep(60)
            return self._send_tx(data, is_get, is_quote, jam)
        return response.json()

    def _permit(self, data: Dict[str, Union[str, Dict[str, Union[str, int]]]], permit: Union[Tuple[str, int], None] = None) -> dict[str, Union[str, Dict[str, Union[str, int]]]]:
        data["permit"] = {
            "signature": permit[0],  # type: ignore
            "approvals_deadline": permit[1], # type: ignore
        }
        return data

    def request_quote(self, buy_tokens: Token, sell_tokens: Token, sell_amounts: Union[int, float], approval_type: ApprovalType, jam: bool) -> Dict[str, Any]:
        data = self._send_tx(data=self._params(buy_tokens, sell_tokens, sell_amounts, approval_type), jam=jam, is_get=True, is_quote=True)
        return data

    def _request_quote_important_data(self, buy_tokens: Token, sell_tokens: Token, sell_amounts: Union[int, float], approval_type: ApprovalType, jam: bool, pmm_too: bool) -> Tuple[str, Dict[str, Any], int, Union[PermitNeeded, None]]:
        quote: Dict[str, Any] = self.request_quote(buy_tokens, sell_tokens, sell_amounts, approval_type, jam)
        if not jam:
            try:
                if quote['onchainOrderType'] != 'SingleOrder':
                    print("Only SingleOrder is supported")
                    sleep(120)
                    return self._request_quote_important_data(buy_tokens, sell_tokens, sell_amounts, approval_type, pmm_too, jam)
            except KeyError:
                if quote['error']['errorCode'] == 102:
                    print(quote)
                    sleep(120)
                    return self._request_quote_important_data(buy_tokens, sell_tokens, sell_amounts, approval_type, pmm_too, jam)
                else:
                    pprint(quote)
                    return self._request_quote_important_data(buy_tokens, sell_tokens, sell_amounts, approval_type, pmm_too, jam)
        permit: Union[PermitNeeded, None] = None
        return quote["quoteId"], quote["toSign"], int(quote["buyTokens"][buy_tokens.address]["minimumAmount"]), permit
    
    def request_quote_important_data(self, buy_tokens: Token, sell_tokens: Token, sell_amounts: Union[int, float], approval_type: ApprovalType, pmm: bool, jam: bool) -> Tuple[str, Dict[str, Any], int, bool, Union[PermitNeeded, None]]:
        if pmm and jam:
            _pmm_quote_id, _pmm_to_sign, _pmm_amount, _permit = self._request_quote_important_data(buy_tokens, sell_tokens, sell_amounts, approval_type, False, pmm)
            _jam_quote_id, _jam_to_sign, _jam_amount, _permit = self._request_quote_important_data(buy_tokens, sell_tokens, sell_amounts, approval_type, True, pmm)
            if _pmm_amount > _jam_amount: return _pmm_quote_id, _pmm_to_sign, _pmm_amount, False, _permit
            return _jam_quote_id, _jam_to_sign, _jam_amount, True, _permit
        if pmm:
            print("pmm")
            _pmm_quote_id, _pmm_to_sign, _pmm_amount, _permit = self._request_quote_important_data(buy_tokens, sell_tokens, sell_amounts, approval_type, False, pmm)
            return _pmm_quote_id, _pmm_to_sign, _pmm_amount, False, _permit
        _jam_quote_id, _jam_to_sign, _jam_amount, _permit = self._request_quote_important_data(buy_tokens, sell_tokens, sell_amounts, approval_type, True, pmm)
        return _jam_quote_id, _jam_to_sign, _jam_amount, True, _permit
    

    def send_transaction(self, signature: str, quote_id: str, jam: bool, permit: Union[Tuple[str, int], None] = None) -> bool:
        data: Dict[str, Union[str, Dict[str, Union[str, int]]]] = {
            "signature": signature,
            "quote_id": quote_id,
            "sign_scheme": "EIP712",
        }
        if permit is not None: data = self._permit(data, permit)
        json_response = self._send_tx(data, is_get=False, is_quote=False, jam=jam)
        pprint(json_response)
        return self.check_last_look(json_response)

    def check_last_look(self, response: Dict[str, Any]) -> bool:
        try:
            if response["error"]['errorCode'] == 202: return True
        except KeyError: pass
        return False