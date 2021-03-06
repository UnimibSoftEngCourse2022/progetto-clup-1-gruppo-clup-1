from dataclasses import dataclass


@dataclass(frozen=True)
class StoreManager:
    id: ...
    username: ...
    password_hash: ...
