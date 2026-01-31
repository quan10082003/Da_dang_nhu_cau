from src.domain.point import Point
from src.domain.spot_location import CircularRingArea, Hotspot
from src.population.genarate_area import genarate_circular_ring_area

import random
import numpy as np
import pandas as pd

def gen_random_location_in_area(area: CircularRingArea) -> list[Point]:
    points_list: list[Point] = []

    for i in range(area.n_pop):
        r = random.uniform(area.r, area.r + area.w)
        theta = random.uniform(0, 2 * np.pi)
        x = r * np.cos(theta) + area.coords.x
        y = r * np.sin(theta) + area.coords.y

        points_list.append(Point(x,y))

    return points_list

def genarate_person_around_hotspot(hotspot: Hotspot, width_ring: float, p0: float, beta_gradient_method: float) -> pd.DataFrame:
    df = pd.DataFrame()
    id_hotspot = hotspot.id

    area_list: list[CircularRingArea] = genarate_circular_ring_area(hotspot=hotspot, width_ring = width_ring, p0=p0, beta_gradient_method=beta_gradient_method)
    for area in area_list:
        person_distribute_list: list[Point] = gen_random_location_in_area(area=area)
        person_distribute_dict: list[dict] =  [obj.__dict__ for obj in person_distribute_list]

        temp_df = pd.DataFrame(person_distribute_dict)
        df = pd.concat([df,pd.DataFrame(temp_df)], ignore_index= True)
            
    df["idO"] = df.apply(lambda x: id_hotspot, axis=1)
    df.columns = ["xO", "yO", "idO"]
    df.index.name = "id"

    return df
                
                

if __name__ ==  "__main__":

    from src.data.load_config import create_hotspots_from_region
    hotspot_list, workspot_list = create_hotspots_from_region(config_path = './config/config_scenario.yaml', beta_gravity_model = 0.5)

    df: pd.DataFrame = genarate_person_around_hotspot(hotspot=hotspot_list[0], width_ring= 0.01, p0=100.0, beta_gradient_method=0.5)
    output_path = "data/interim/step1_person_location.csv"
    df.to_csv(output_path, sep=";")
        
        
    
