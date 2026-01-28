from src.domain.point import Point
from src.domain.spot_location import CircularRingArea, Hotspot
from src.computation.density import calc_circular_ring_density

import numpy as np


def genarate_circular_ring_area(hotspot: Hotspot, width_ring: float) -> list[CircularRingArea]:
    """
    hotpot là điểm nóng trung tâm chứa thông tin số người sống quanh đó
    width_ring là độ dày của các vùng vành khăn tinhs theo km
    """
    area_list: list[CircularRingArea] = []
    total_temp_pop = 0
    last_area_pop = hotspot.n_pop

    for i in np.arange(0,hotspot.r, width_ring):
        temp_pop = calc_circular_ring_density(i, width_ring)
        total_temp_pop += temp_pop
        area = CircularRingArea(hotspot.coords, temp_pop, i, width_ring )
        area_list.append(area)

    # Chuẩn hóa dân số trong các vùng vành khăn
    for i in range(len(area_list)-1):
        area_list[i].n_pop = int(area_list[i].n_pop / total_temp_pop * hotspot.n_pop)
        last_area_pop -= area_list[i].n_pop
    area_list[-1].n_pop = last_area_pop

    return area_list


if __name__ ==  "__main__":

    from src.data.load_spots import load_spots_config

    hotspot_list, _ = load_spots_config("./config/config_location.yaml")
    
    demo_hotspot: Hotspot = hotspot_list[0]
    area_list: list[CircularRingArea] = genarate_circular_ring_area(demo_hotspot,0.1)

    for idx, area in enumerate(area_list):
        print(f" Vung co id {idx}: {area.n_pop} - ban kinh tu {area.r} -> {area.r + area.w}")


