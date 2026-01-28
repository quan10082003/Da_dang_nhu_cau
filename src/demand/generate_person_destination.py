from src.domain.spot_location import WorkSpot, Hotspot
from src.computation.distance import calc_distance
from src.domain.point import Point
from src.demand.attractive_destination import calc_attractiveness_of_destination

import random
import numpy as np

def random_location_around_spot(workspot: Workspot) -> Point:
    r = random.uniform(0,workspot.r)
    theta = random.uniform(0, np.pi*2)

    x = workspot.coords.x + r * np.cos(theta)
    y = workspot.coords.y + r * np.sin(theta)

    return Point(x,y)

def genarate_person_destination(hotspot: Hotspot, workspot_list: list[WorkSpot]):
    probability_list = gravity_probability_model_fuc(hotspot = hotspot, workspot_list = workspot_list)    

if __name__ == "__main__":
    from src.data.load_spots import load_spots_config

    hotspot_list, _ = load_spots_config(r'./config/config_location.yaml')
    df: pd.DataFrame = genarate_person_around_hotspots(hotspot_list=hotspot_list)

    path = "data/interim/home_location/step1_person_location.csv"
    df.to_csv(path, sep=";")