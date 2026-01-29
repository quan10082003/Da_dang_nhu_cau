from dataclasses import dataclass

# x y tính theo km
@dataclass(frozen=True)
class Point:
    x: str
    y: str