import numpy as np
from src.domain.point import Point

# khoảng các là km
def calc_km_distance(a: Point, b: Point):
    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
