from src.domain.spot_location import WorkSpot
from src.domain.point import Point
from src.population.genarate_person_around_hotspot import genarate_person_around_hotspot
from src.demand.probability_destination import gravity_probability_model_fuc


import random
import numpy as np
import pandas as pd

def random_location_around_spot(workspot: WorkSpot) -> Point:
    r = random.uniform(0.0,workspot.r)
    theta = random.uniform(0.0, float(np.pi*2))
    x = workspot.coords.x + r * np.cos(theta)
    y = workspot.coords.y + r * np.sin(theta)
    return Point(x,y)

def genarate_person_destination(people_in_single_hotspot_location_df: pd.DataFrame, probability_map: dict[WorkSpot, float]) -> pd.DataFrame:
    """
    people_in_single_hotspot_location_df là bảng df chứa location của từng người dân trong chỉ 1 vùng hotspot duy nhất
    """
    workspots = list(probability_map.keys())
    weights = list(probability_map.values())
    def get_coords(row, workspots, weights) ->pd.Series:
        selected_workspot: WorkSpot = random.choices(workspots, weights, k=1)[0]
        p = random_location_around_spot(selected_workspot)
        return pd.Series([p.x,p.y, selected_workspot.id])
    people_in_single_hotspot_location_df[["xD","yD","idD"]] = people_in_single_hotspot_location_df.apply(lambda row: get_coords(row,workspots, weights), axis =1 )
    return people_in_single_hotspot_location_df



if __name__ == "__main__":
    from src.data.load_config import create_hotspots_from_region
    hotspot_list, workspot_list = create_hotspots_from_region(config_path = './config/config_scenario.yaml', beta_gravity_model = 0.5)
    probability_map = gravity_probability_model_fuc(hotspot_list[0], workspot_list)

    input_path = "data/interim/step1_person_location.csv"
    output_path = "data/interim/step2_person_mapping_destination.csv"
    df = pd.read_csv(input_path, sep = ";")
    ddf = genarate_person_destination(df, probability_map )
    ddf.to_csv(output_path, sep=";", index=False)

