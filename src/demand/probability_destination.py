from src.domain.spot_location import WorkSpot, Hotspot
from src.computation.distance import calc_distance
from src.domain.point import Point
from src.demand.attractive_destination import calc_attractiveness_of_destination

def gravity_probability_model_fuc(hotspot : Hotspot, workspot_list: list[WorkSpot]) -> list[dict[WorkSpot, float]] :
    """
    dùng mô hình trọng lực để xắc suất người dân trong vùng hottpot đi đến các vùng WorkSpot
    Trả ra số lượng người muốn đi đến các vùng D đã khai báo
    """

    probability_list : list[dict[WorkSpot, float]] = []
    total = 0

    for workspot in workspot_list:
        Fij = calc_distance(hotspot.coords, workspot.coords)
        I = workspot.attractiveness
        temp_prob = p * I / Fij
        total += I / Fij
        probability_list.append({workspot : temp_prob})

    # Chuẩn hóa lại số lượng người đan trong vuingf hotpot đến mỗi vùng workpot
    for idx in range(len(probability_list)):
        probability_list[idx].value = ( probability_list[idx].value / total) *100

    return probability_list


        


     