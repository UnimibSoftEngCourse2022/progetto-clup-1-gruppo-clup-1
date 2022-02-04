from dataclasses import dataclass


@dataclass(frozen=True)
class Store:
    id: ...
    categories: ...