from dataclasses import dataclass


@dataclass
class Admin:
    id: ...
    username: ...
    password: ...
    store: str = "default"