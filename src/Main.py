from src.data.load_peakhours import load_peakhours
from src.data.load_spots import load_spots_config, save_spots_to_debug

from src.domain.spot_location import Hotspot,WorkSpot
from src.domain.point import Point
from src.computation.attractive import calc_attractiveness_of_workspot
from src.data.create_spot_region import generate_matsim_objects_in_region
from src.population.genarate_person_around_hotspot import genarate_person_around_hotspot
from src.demand.probability_destination import gravity_probability_model_fuc
from src.demand.generate_person_destination import genarate_person_destination
from src.timedeparture.generate_hour_departure import generate_trip_departure
from src.write.generate_OD_matrix_csv import generate_OD_csv
from src.write.write_plan_xml import write_PlanXML



import yaml
import json
from dataclasses import asdict
import numpy as np
import pandas as pd

def create_spots_list(debug_region_path: str):
    # --- 1. Cấu hình vùng dân cư (Hotspots) ---
    hotspot_configs = [
        {"id": "HS1", "type": "circle", "center": Point(454.031, 5734.395), "points_number":7, "pop": 5000, "radius_region": 1, "min_radian": 0.1, "max_radian": 0.5},
        # {"id": "HS2", "type": "rectangle", "center": Point(457.257, 5793.84), "points_number":3, "pop": 5000, "width": 1, "height": 1, "min_radian": 0.1, "max_radian": 0.5},  
    ]

    hotspots_list = []
    for conf in hotspot_configs:
        spots = generate_matsim_objects_in_region(
            prefix_region_id=conf["id"],
            obj_type="hotspot",
            region_type=conf["type"],
            center_region=conf["center"],
            total_input=conf["pop"],
            num_points=conf["points_number"],
            min_r=conf["min_radian"], 
            max_r=conf["max_radian"],
            **conf
        )
        hotspots_list.extend(spots)

    # --- 2. Cấu hình vùng việc làm (Workspots) ---
    workspot_configs = [
        # {"id": "WS1", "type": "circle", "center": Point(452.257, 5743.84), "points_number":5, "radius_region": 1000, "min_radian": 0.1, "max_radian": 0.5, "pop": 0},
        {"id": "WS2", "type": "rectangle", "center": Point(454.031, 5734.395), "points_number":5, "width": 0.01, "height": 1000, "min_radian": 0.1, "max_radian": 0.5, "pop": 0},
    ]

    workspots_list = []
    for conf in workspot_configs:
        # Bước A: Gen các điểm tạm thời cho vùng này
        temp_spots = generate_matsim_objects_in_region(
            prefix_region_id=conf["id"],
            obj_type="workspot",
            region_type=conf["type"],
            center_region=conf["center"],
            total_input=conf["pop"],
            num_points=conf["points_number"],
            min_r=conf["min_radian"], 
            max_r=conf["max_radian"],
            **conf
        )
        
        # Bước B: Tính attractiveness cho từng điểm vừa gen và thêm vào list chính
        for temp in temp_spots:
            attr = calc_attractiveness_of_workspot(workspot=temp, hotspot_list=hotspots_list)
            # Tạo object WorkSpot hoàn chỉnh
            workspots_list.append(WorkSpot(
                id=temp.id, 
                coords=temp.coords, 
                r=temp.r, 
                attractiveness=attr
            ))

    # --- 3. Lưu Debug ---
    save_spots_to_debug(debug_region_path, hotspots_list, workspots_list)

    return hotspots_list, workspots_list

if __name__ == "__main__":
    output_plan_csv_path = "data/processed/complete_plan.csv"
    output_OD_path = "data/processed/OD.csv"
    output_spots_path = r"data\processed\spot_info.json"
    output_plan_xml_path = "data/processed/plan.xml"


    am_peakhours, pm_peakhours = load_peakhours(r".\config\config.yaml")
    hotspots_list, workspots_list = create_spots_list(output_spots_path)

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

    complete_df.to_csv(output_plan_csv_path, sep=";")
    OD_df.to_csv(output_OD_path, sep = ";")



    write_PlanXML(output_plan_csv_path,output_plan_xml_path)



