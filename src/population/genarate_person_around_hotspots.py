from src.domain.point import Point
from src.domain.spot_location import CircularRingArea, Hotspot
from src.computation.density import calc_circular_ring_density

import random
import numpy as np
import pandas as pd

def gen_random_location_in_area(area: CircularRingArea) -> list[Point]:
    points_list: list[Point] = []

    for i in range(area.n_pop):
        r = random.uniform(area.r, area.r + area.w)
        theta = random.uniform(0, 2 * np.pi)
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        points_list.append(Point(x,y))

    return points_list

def genarate_person_around_hotspots(hotspot_list: list[Hotspot]) -> pd.DataFrame:
    for spot in hotspot_list:
        area_list: list[CircularRingArea] = genarate_circular_ring_area(hotspot=spot, r=5)
        for area in area_list:
            person_distribute_list: list[Point] = gen_random_location_in_area(area=area)
            for person in person_distribute_list:  
                data_for_df = [asdict(person)]
                df = pd.DataFrame(data_for_df)
                

if __name__ ==  "__main__":

    from src.population.genarate_area import genarate_circular_ring_area
    from src.data.load_spots import load_spots_config

    hotspot_list, _ = load_spots_config(r'./config/config_location.yaml')
    hotspot_data: dict = hotspot_list[0]
    demo_hotspot: Hotspot = Hotspot(Point(hotspot_data['x'], hotspot_data['y']), hotspot_data['n'])
    area_list: list[CircularRingArea] = genarate_circular_ring_area(demo_hotspot,5)

    point_ls = gen_randomlocation_in_area(area_list[0])
    for i in range(len(point_ls)):
        print( f"id {i}: x: {point_ls[i].x}, y: {point_ls[i].y}")
        
        
    
