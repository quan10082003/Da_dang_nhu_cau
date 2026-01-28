from dataclasses import dataclass
from src.domain.point import Point

# Các địa điểm dân cư tập trung và số lượng dân cư trong đó,  r là km
@dataclass 
class Hotspot:
    coords: Point
    r: float
    n_pop: int  

# Các khu vực vanh khăn xung quanh điểm nóng ,  r,w là km
@dataclass
class CircularRingArea:
    coords: Point
    n_pop: int
    r: float
    w: float
    

# các địa điểm làm việc tập trung và bán kính vùng đó,  r là km
@dataclass
class WorkSpot: 
    coords: Point
    r: float
    attractiveness: float