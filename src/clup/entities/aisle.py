from dataclasses import dataclass


@dataclass(frozen=True)
class Aisle:
    id: ...
    name: ...
    categories: ...
    capacity: int = 5
