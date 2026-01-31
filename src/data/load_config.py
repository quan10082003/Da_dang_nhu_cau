from box import Box
from src.domain.spot_location import WorkSpot, Hotspot
from src.computation.attractive import calc_attractiveness_of_workspot
from src.region.create_spot_region import generate_matsim_objects_in_region

def load_config(config_path:str):
    config = Box.from_yaml(filename=config_path)
    return config

def create_hotspots_from_region(config_path:str, beta_gravity_model: float) -> (list[Hotspot], list[WorkSpot]):
    """
    Tamj thời dùng cái này để load từ region ra các vùng hotspot
    """
    scenariocfg = load_config(config_path)
    hotspots_list = []
    for hotspotcfg in scenariocfg.hotspots_region:
        spots_list = generate_matsim_objects_in_region(**hotspotcfg)
        hotspots_list.extend(spots_list)

    workspots_list = []
    for workspotcfg in scenariocfg.workspots_region:
        spots_list = generate_matsim_objects_in_region(**workspotcfg)
        for spot in spots_list:
            attr = calc_attractiveness_of_workspot(workspot=spot, hotspot_list=hotspots_list, b=beta_gravity_model)
            workspots_list.append(WorkSpot(
                id=spot.id, 
                coords=spot.coords, 
                r=spot.r, 
            attractiveness=attr
        ))
    
    return hotspots_list, workspots_list


if __name__ == "__main__":
    config = load_config(r"config\config_scenario.yaml")
    print(config)