from src.computation.datetime import float_to_time
from src.computation.normal_distributrion import get_random_normal

import random
import pandas as pd


def generate_trip_departure(person_OD_df: pd. DataFrame, name_trip: str, peak_hours_list: list[float], sigma : float) -> pd.DataFrame:
    def random_hours(row, peak_hours_list: list[float] ):
        h = random.choice(peak_hours_list)
        real_h = get_random_normal(h,std_dev=sigma)
        time = float_to_time(real_h)
        return time
        
    person_OD_df[name_trip] = person_OD_df.apply(lambda row : random_hours(row, peak_hours_list ), axis =1)

    return  person_OD_df

if __name__ == "__main__":
    from src.data.load_peakhours import load_peakhours
    from src.data.load_spots import load_spots_config

    am_peakhours, pm_peakhours = load_peakhours(r".\config\config.yaml")
    hotspot_list, workspot_list = load_spots_config(r".\config\config.yaml")

    input_path = "data/interim/step2_person_mapping_destination.csv"
    output_path = "data/interim/step3_adding_departure_time.csv"
    
    df = pd.read_csv(input_path, sep = ";")
    df = generate_trip_departure(person_OD_df=df, name_trip= "home-work", peak_hours_list= am_peakhours, sigma=1.0)
    df = generate_trip_departure(person_OD_df=df, name_trip= "work-home", peak_hours_list= pm_peakhours, sigma=0.5)
    df.to_csv(output_path, sep=";", index=False)

    

        

    
