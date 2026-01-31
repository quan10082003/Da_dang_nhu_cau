from src.domain.point import Point
from src.domain.spot_location import CircularRingArea, Hotspot
from src.computation.density import calc_circular_ring_density

import numpy as np


def genarate_circular_ring_area(hotspot: Hotspot, width_ring: float, p0 : float, beta_gradient_method : float) -> list[CircularRingArea]:
    """
    hotpot là điểm nóng trung tâm chứa thông tin số người sống quanh đó
    width_ring là độ dày của các vùng vành khăn tinhs theo km
    """
    area_list: list[CircularRingArea] = []
    total_temp_pop = 0
    last_area_pop = hotspot.n_pop

    for i in np.arange(0,hotspot.r, width_ring):
        temp_pop = calc_circular_ring_density(r = i, denta_r = width_ring, p0 = p0, beta_gradient_method = beta_gradient_method)
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

    from src.data.load_config import create_hotspots_from_region
    hotspot_list, workspot_list = create_hotspots_from_region(config_path = './config/config_scenario.yaml', beta_gravity_model = 0.5)
    
    demo_hotspot: Hotspot = hotspot_list[0]
    area_list: list[CircularRingArea] = genarate_circular_ring_area(hotspot=demo_hotspot, width_ring=0.01, p0 = 100.0, beta_gradient_method = 0.5)

    for idx, area in enumerate(area_list):
        print(f" Vung co id {idx}: {area.n_pop} - ban kinh tu {area.r} -> {area.r + area.w}")


