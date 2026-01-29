from src.data.load_peakhours import load_peakhours
from src.data.load_spots import load_spots_config

from src.population.genarate_person_around_hotspot import genarate_person_around_hotspot
from src.demand.probability_destination import gravity_probability_model_fuc
from src.demand.generate_person_destination import genarate_person_destination
from src.timedeparture.generate_hour_departure import generate_trip_departure

import pandas as pd

def generate_OD_csv(complete_plan_df: pd.DataFrame) -> pd.DataFrame:
    # 1. Ép kiểu về string để tránh lẫn lộn số và chữ
    df = complete_plan_df.copy()
    df['idO'] = df['idO'].astype(str)
    df['idD'] = df['idD'].astype(str)
    
    # 2. Dùng crosstab
    od_matrix = pd.crosstab(df['idO'], df['idD'])
    return od_matrix

if __name__ == "__main__":
    pass

