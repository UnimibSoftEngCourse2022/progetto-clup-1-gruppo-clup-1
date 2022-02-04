from dataclasses import dataclass


@dataclass(frozen=True)
class Store:
    id: ...
    name: ...
    address: ...
    secret_key: int = 0