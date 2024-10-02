from dataclasses import dataclass
import json

@dataclass
class Chain:
    name: str
    chain_id: int

class Token:
    def __init__(self, name: str, address: str, decimals: int) -> None:
        self.name = name
        self.address = address
        self.decimals = decimals

    def to_wei(self, amount: int | float) -> int:
        return int(amount * 10 ** self.decimals)

    def from_wei(self, amount) -> int:
        return amount / 10**self.decimals


@dataclass
class PermitToken:
    token: str
    value: int


@dataclass
class PermitNeeded:
    spender: str
    tokens: list[PermitToken]


@dataclass
class Settings:
    slippage: float
    pause: bool
    pause_time: int
    try_mean: int
    try_bounds: int
    sleep_after: bool
    quit: bool
    pause_after_success: int
    jam: bool
    pmm: bool

    @staticmethod
    def read_settings_from_json(file_path: str = "settings.json") -> 'Settings':
        # Open the JSON file
        with open(file_path, 'r') as file:
            # Load the JSON content
            settings_data = json.load(file)

        # Assuming the JSON structure matches the dataclass fields
        return Settings(**settings_data)

