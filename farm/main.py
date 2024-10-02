import argparse

from type_handling.my_types import Token, Settings
import datetime as dt
from random import randint
from time import sleep
from dataclasses import dataclass
from random import randint
from pprint import pprint
from type_handling.instances import ARBITRUM, USDC, WETH, ACCOUNT, USDT
from computation.rpc import RPC, ApprovalType
from computation.chain_tx import Signer, OrderType

HOUR = 3600

@dataclass
class Amount:
    WETH: float | None
    USDC: float | None
    
    @property
    def WETH_wei(self) -> int:
        if self.WETH == None: return 0
        return WETH.to_wei(self.WETH)  # type: ignore
    
    @property
    def USDC_wei(self) -> int:
        if self.USDC == None: return 0
        return USDC.to_wei(self.USDC) # type: ignore
    

class Main:
    def __init__(self) -> None:
        self.counter = 0
        self.rpc = RPC(ARBITRUM, ACCOUNT)
        self.signer = Signer(ACCOUNT)
        self.settings = Settings.read_settings_from_json()
        self.max_count = self.settings.try_mean

    def _check_min_amount(self, min_amount: float, end_token: Token, amounts: Amount) -> bool:
        if (amounts.WETH == None) or (amounts.USDC == None): return False
        if (self.counter >= self.max_count) and self.settings.quit:
            self.counter = 0
            self.max_count = randint(max(self.settings.try_mean - self.settings.try_bounds, 0), self.settings.try_mean + self.settings.try_bounds)
            print("Quitting")
            return False
        if end_token == WETH:
            if min_amount < amounts.WETH_wei * (1 - self.settings.slippage):  # type: ignore
                print(f"min amount is {WETH.from_wei(min_amount)} WETH need {WETH.from_wei(amounts.WETH_wei * (1 - self.settings.slippage))}")  # type: ignore
                if self.settings.pause: sleep(self.settings.pause_time)
                self.counter += 1
                return True  # type: ignore
        else:
            if min_amount < amounts.USDC_wei * (1 - self.settings.slippage):  # type: ignore
                print(f"min amount is {USDC.from_wei(min_amount)} USDC need {USDC.from_wei(amounts.USDC_wei * (1 - self.settings.slippage))}")   # type: ignore
                if self.settings.pause: sleep(self.settings.pause_time)
                self.counter += 1
                return True  # type: ignore
        return False

    def main(self, trade_amount: float, times: int, start_token: Token, rounds: int, stable: Token):
        amounts = Amount(trade_amount if start_token == WETH else None, trade_amount if (start_token == USDC or start_token == USDT) else None)
        for _ in range(rounds):
            for _ in range(times):
                self.settings = Settings.read_settings_from_json()  ## This is a hack to update the settings
                trade_amount, start_token = self.trade(start_token, trade_amount, amounts, stable)
            if self.settings.sleep_after: sleep(randint(int(HOUR * (1 / 4)), 1 * HOUR))

    def trade(self, start_token: Token, trade_amount: float, amounts: Amount, stable: Token) -> tuple[float, Token]:
        end_token = WETH if (start_token == USDC or start_token == USDT) else stable
        quote_id, to_sign, min_amount, jam, _ = self.rpc.request_quote_important_data(end_token, start_token, trade_amount, ApprovalType.Standard, self.settings.pmm, self.settings.jam)
        if self._check_min_amount(min_amount, end_token, amounts): return trade_amount, start_token
        signature = self.signer.sign_order(OrderType.SINGLE_ORDER_TYPES, to_sign, jam)
        err = self.rpc.send_transaction(signature, quote_id, jam, None)
        if err: return trade_amount, start_token
        sleep(self.settings.pause_after_success)
        if end_token == WETH: amounts.WETH = WETH.from_wei(min_amount)
        else: amounts.USDC = USDC.from_wei(min_amount)
        return end_token.from_wei(min_amount), end_token

if __name__ == "__main__":
    _main = Main()
    _main.main(7200, 3000, WETH, 3, USDT)


# parser = argparse.ArgumentParser()
# parser.add_argument("trade_amount", type=float, help='The amount of USDC to trade')
# args = parser.parse_args()


# def main_with_permit(trade_amount: float):
#     rpc = RPC(ARBITRUM, ACCOUNT)
#     signer = Signer(ACCOUNT)
#     quote_id, to_sign, permit = rpc.request_quote_important_data(WETH, USDC, trade_amount, ApprovalType.Standard)
#     if permit is not None:
#         permit_token = USDC if permit.tokens[0].token == USDC.address else WETH
#         deadline = int((dt.datetime.now() + dt.timedelta(weeks=4)).timestamp())
#         permit_signature = signer.sign_permit(permit.spender, permit.tokens[0].value, deadline, permit_token, ARBITRUM)
#         _permit = (permit_signature, deadline)
#     else: _permit = None
#     signature = signer.sign_order(OrderType.SINGLE_ORDER_TYPES, to_sign)
#     pprint(rpc.send_transaction(signature, quote_id, _permit))
