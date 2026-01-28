from src.domain.point import Point
from src.domain.spot_location import CircularRingArea, Hotspot
from src.computation.density import calc_circular_ring_density
from dataclasses import asdict
from src.population.genarate_area import genarate_circular_ring_area

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

def genarate_person_around_hotspot(hotspot: Hotspot, width_ring=0.1) -> pd.DataFrame:
    df = pd.DataFrame()

    area_list: list[CircularRingArea] = genarate_circular_ring_area(hotspot=hotspot, width_ring = width_ring)
    for area in area_list:
        person_distribute_list: list[Point] = gen_random_location_in_area(area=area)
        for person in person_distribute_list:  
            data_for_df = [asdict(person)]
            df = pd.concat([df,pd.DataFrame(data_for_df)], ignore_index= True)
            
    return df
                
                

if __name__ ==  "__main__":

    from src.data.load_spots import load_spots_config

    hotspot_list, _ = load_spots_config(r'./config/config_location.yaml')
    df: pd.DataFrame = genarate_person_around_hotspot(hotspot=hotspot_list[0])

    path = "data/interim/home_location/step1_person_location.csv"
    df.to_csv(path, sep=";")
        
        
    
