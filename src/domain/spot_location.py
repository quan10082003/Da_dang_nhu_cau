from dataclasses import dataclass
from src.domain.point import Point

# Các địa điểm dân cư tập trung và số lượng dân cư trong đó
@dataclass 
class Hotspot:
    o: Point
    n_pop: int  

# Các khu vực vanh khăn xung quanh điểm nóng 
@dataclass
class CircularRingArea:
    o: Point
    n_pop: int
    r: float
    w: float
    

# các địa điểm làm việc tập trung và bán kính vùng đó
@dataclass
class WorkSpot: 
    d: Point
    r: float