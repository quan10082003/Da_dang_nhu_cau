from src.data.load_config import load_config, create_hotspots_from_region
from src.domain.spot_location import WorkSpot
from src.population.genarate_person_around_hotspot import genarate_person_around_hotspot
from src.demand.probability_destination import gravity_probability_model_fuc
from src.demand.generate_person_destination import genarate_person_destination
from src.timedeparture.generate_hour_departure import generate_trip_departure
from src.write.generate_OD_matrix_csv import generate_OD_csv
from src.write.write_plan_xml import write_PlanXML

from dataclasses import asdict
import pandas as pd

if __name__ == "__main__":

    pathcfg = load_config("config\config_path.yaml")
    scenariocfg = load_config("config\config_scenario.yaml")
    paramcfg = scenariocfg.params
    
    hotspots_list, workspots_list = create_hotspots_from_region(config_path = './config/config_scenario.yaml', beta_gravity_model = paramcfg.gravity_probability_model.attractiveness.beta)

    hs_df = pd.DataFrame([asdict(x) for x in hotspots_list])
    ws_df = pd.DataFrame([asdict(x) for x in workspots_list])
    spot_df = pd.concat([hs_df, ws_df])
    spot_df.to_csv(pathcfg.processed.spot, sep=";")
        
    complete_df = pd.DataFrame()
    for hotspot in hotspots_list:
        df1: pd.DataFrame = genarate_person_around_hotspot(hotspot=hotspot, width_ring=paramcfg.circlering_area.width_ring, p0=paramcfg.saturation_gradient_method.p0, beta_gradient_method=paramcfg.saturation_gradient_method.beta)

        probability_map = gravity_probability_model_fuc(hotspot= hotspot, workspot_list=workspots_list)
        df2 = genarate_person_destination(df1, probability_map )

        df3 = generate_trip_departure(person_OD_df=df2, name_trip= "home-work", peak_hours_list= scenariocfg.peakhours.am.hour, sigma=scenariocfg.params.normal_distribution.std)
        df4 = generate_trip_departure(person_OD_df=df3, name_trip= "work-home", peak_hours_list= scenariocfg.peakhours.pm.hour, sigma=scenariocfg.params.normal_distribution.std)

        complete_df = pd.concat([complete_df, df4], ignore_index = True)

        del df1,df2,df3,df4

    complete_df.index.name = "id"
    OD_df = generate_OD_csv(complete_plan_df=complete_df)
    complete_df.to_csv(pathcfg.processed.plan_csv, sep=";")
    OD_df.to_csv(pathcfg.processed.OD, sep = ";")
    write_PlanXML(pathcfg.processed.plan_csv,pathcfg.processed.plan_xml)



