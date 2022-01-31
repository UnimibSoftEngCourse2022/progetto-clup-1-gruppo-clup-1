from dataclasses import dataclass


@dataclass
class Admin:
    id: ...
    password: ...
    store: str = "default"