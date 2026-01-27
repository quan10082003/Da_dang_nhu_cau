from src.domain.point import Point
from src.domain.spot_location import CircularRingArea, Hotspot
from src.computation.density import calc_circular_ring_density


def genarate_circular_ring_area(hotspot: Hotspot, r: float) -> list[CircularRingArea]:
    """
    hotpot là điểm nóng trung tâm chứa thông tin số người sống quanh đó
    r là bán kính tối đa số người sống quanh hotpot đó
    """
    area_list: list[CircularRingArea] = []
    width_ring = 1
    total_temp_pop = 0
    last_area_pop = hotspot.n_pop

    for i in range(0,r, width_ring):
        temp_pop = calc_circular_ring_density(i, width_ring)
        total_temp_pop += temp_pop
        area = CircularRingArea(hotspot.o, temp_pop, i, width_ring )
        area_list.append(area)

    # Chuẩn hóa dân số trong các vùng vành khăn
    for i in range(len(area_list)-1):
        area_list[i].n_pop = int(area_list[i].n_pop / total_temp_pop * hotspot.n_pop)
        last_area_pop -= area_list[i].n_pop
    area_list[-1].n_pop = last_area_pop

    return area_list


if __name__ ==  "__main__":

    from src.data.load_spots import load_spots_config

    hotspot_list, _ = load_spots_config(r'./config/config_location.yaml')
    hotspot_data: dict = hotspot_list[0]
    demo_hotspot: Hotspot = Hotspot(Point(hotspot_data['x'], hotspot_data['y']), hotspot_data['n'])
    area_list: list[CircularRingArea] = genarate_circular_ring_area(demo_hotspot,5)

    for idx, area in enumerate(area_list):
        print(f" Vung co id {idx}: {area.n_pop} - ban kinh tu {area.r} -> {area.r + area.w}")


