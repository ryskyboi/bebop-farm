SINGLE_ORDER_TYPES = {
    "SingleOrder": [
        { "name": "partner_id", "type": "uint64" },
        { "name": "expiry", "type": "uint256" },
        { "name": "taker_address", "type": "address" },
        { "name": "maker_address", "type": "address" },
        { "name": "maker_nonce", "type": "uint256" },
        { "name": "taker_token", "type": "address" },
        { "name": "maker_token", "type": "address" },
        { "name": "taker_amount", "type": "uint256" },
        { "name": "maker_amount", "type": "uint256" },
        { "name": "receiver", "type": "address" },
        { "name": "packed_commands", "type": "uint256" },
    ]
}

MULTI_ORDER_TYPES = {
    "MultiOrder": [
        { "name": "partner_id", "type": "uint64" },
        { "name": "expiry", "type": "uint256" },
        { "name": "taker_address", "type": "address" },
        { "name": "maker_address", "type": "address" },
        { "name": "maker_nonce", "type": "uint256" },
        { "name": "taker_tokens", "type": "address[]" },
        { "name": "maker_tokens", "type": "address[]" },
        { "name": "taker_amounts", "type": "uint256[]" },
        { "name": "maker_amounts", "type": "uint256[]" },
        { "name": "receiver", "type": "address" },
        { "name": "commands", "type": "bytes" },
    ]
}

AGGREGATE_ORDER_TYPES = {
    "AggregateOrder": [
        { "name": "partner_id", "type": "uint64" },
        { "name": "expiry", "type": "uint256" },
        { "name": "taker_address", "type": "address" },
        { "name": "maker_addresses", "type": "address[]" },
        { "name": "maker_nonces", "type": "uint256[]" },
        { "name": "taker_tokens", "type": "address[][]" },
        { "name": "maker_tokens", "type": "address[][]" },
        { "name": "taker_amounts", "type": "uint256[][]" },
        { "name": "maker_amounts", "type": "uint256[][]" },
        { "name": "receiver", "type": "address" },
        { "name": "commands", "type": "bytes" },
    ]
}

JAM_ORDER_TYPES = {
    "JamOrder": [
        { "name": "taker", "type": "address" },
        { "name": "receiver", "type": "address" },
        { "name": "expiry", "type": "uint256" },
        { "name": "nonce", "type": "uint256" },
        { "name": "executor", "type": "address" },
        { "name": "minFillPercent", "type": "uint16" },
        { "name": "hooksHash", "type": "bytes32" },
        { "name": "sellTokens", "type": "address[]" },
        { "name": "buyTokens", "type": "address[]" },
        { "name": "sellAmounts", "type": "uint256[]" },
        { "name": "buyAmounts", "type": "uint256[]" },
        { "name": "sellNFTIds", "type": "uint256[]" },
        { "name": "buyNFTIds", "type": "uint256[]" },
        { "name": "sellTokenTransfers", "type": "bytes" },
        { "name": "buyTokenTransfers", "type": "bytes" },
    ]
}

PERMIT = {
    "Permit": [
        {"name": "owner", "type": "address"},
        {"name": "spender", "type": "address"},
        {"name": "value", "type": "uint256"},
        {"name": "nonce", "type": "uint256"},
        {"name": "deadline", "type": "uint256"},
    ]
}
