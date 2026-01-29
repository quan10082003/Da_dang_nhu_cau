from src.data.load_peakhours import load_peakhours
from src.data.load_spots import load_spots_config

from src.population.genarate_person_around_hotspot import genarate_person_around_hotspot
from src.demand.probability_destination import gravity_probability_model_fuc
from src.demand.generate_person_destination import genarate_person_destination
from src.timedeparture.generate_hour_departure import generate_trip_departure
from src.write.generate_OD_matrix_csv import generate_OD_csv

import pandas as pd


if __name__ == "__main__":

    am_peakhours, pm_peakhours = load_peakhours(r".\config\config.yaml")
    hotspots_list, workspots_list = load_spots_config(r".\config\config.yaml")
    output_plan_path = "data/processed/complete_plan.csv"
    output_OD_path = "data/processed/OD.csv"

    complete_df = pd.DataFrame()
    for hotspot in hotspots_list:
        df1: pd.DataFrame = genarate_person_around_hotspot(hotspot=hotspot, width_ring=0.01)

        probability_map = gravity_probability_model_fuc(hotspot= hotspot, workspot_list=workspots_list)
        df2 = genarate_person_destination(df1, probability_map )

        df3 = generate_trip_departure(person_OD_df=df2, name_trip= "home-work", peak_hours_list= am_peakhours, sigma=1.0)
        df4 = generate_trip_departure(person_OD_df=df3, name_trip= "work-home", peak_hours_list= pm_peakhours, sigma=0.5)

        complete_df = pd.concat([complete_df, df4], ignore_index = True)

        del df1,df2,df3,df4
    
    complete_df.index.name = "id"
    OD_df = generate_OD_csv(complete_plan_df=complete_df)

    complete_df.to_csv(output_plan_path, sep=";")
    OD_df.to_csv(output_OD_path, sep = ";")
    



  