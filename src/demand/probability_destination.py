from src.domain.spot_location import WorkSpot, Hotspot
from src.computation.distance import calc_km_distance
from src.domain.point import Point
from src.computation.attractive import calc_attractiveness_of_workspot

def gravity_probability_model_fuc(hotspot : Hotspot, workspot_list: list[WorkSpot]) -> dict[WorkSpot, float] :
    """
    dùng mô hình trọng lực để xắc suất người dân trong vùng hottpot đi đến các vùng WorkSpot
    Trả ra số lượng người muốn đi đến các vùng D đã khai báo
    """

    probability_map : dict[WorkSpot, float] = {}
    total = 0.0

    for workspot in workspot_list:
        Fij = calc_km_distance(hotspot.coords, workspot.coords)
        I = workspot.attractiveness
        temp_prob = I / Fij
        total += temp_prob
        probability_map[workspot] =  temp_prob

    # Chuẩn hóa lại số lượng người đan trong vuingf hotpot đến mỗi vùng workpot
    for workspot in probability_map:
        probability_map[workspot] = ( probability_map[workspot] / total)

    return probability_map

if __name__ == "__main__":
    from src.data.load_spots import load_spots_config
    hotspot_list, workspot_list = load_spots_config("./config/config.yaml")
    for spot in hotspot_list:
        prob_map = gravity_probability_model_fuc(spot, workspot_list=workspot_list)
        print(prob_map)

        


     