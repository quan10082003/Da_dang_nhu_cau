import numpy as np
from src.domain.point import Point

def calc_distance(a: Point, b: Point):
    return np.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
