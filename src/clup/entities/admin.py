from dataclasses import dataclass


@dataclass(frozen=True)
class Admin:
    id: ...
    username: ...
    password_hash: ...
