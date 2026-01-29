from src.domain.spot_location import WorkSpot, Hotspot
from src.computation.distance import calc_km_distance

import numpy as np


def calc_attractiveness_of_workspot(workspot: WorkSpot, hotspot_list: list[Hotspot], b=1) -> float:
    """
    Tính độ hấp dẫn của điểm đến từ nhiều điểm nóng CBD ( central business district) dựa trên trọng số mật độ
    """
    density_list = [a.n_pop / (np.pi * a.r * a.r) for a in hotspot_list] # người/ km^2
    # print(density_list)
    total_density = np.sum(density_list)

    synthetic_d_km = 0
    for idx,spot in enumerate(hotspot_list):
        # print(calc_km_distance(workspot.coords, spot.coords) )
        synthetic_d_km += calc_km_distance(workspot.coords, spot.coords) * density_list[idx] / total_density

    attractiveness  = float(np.exp(-synthetic_d_km*b))
    return attractiveness






