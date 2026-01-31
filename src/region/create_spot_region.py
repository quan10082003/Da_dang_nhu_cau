from typing import List, Union
from src.domain.spot_location import Hotspot,WorkSpot
from src.domain.point import Point

import numpy as np

def generate_matsim_objects_in_region(
    prefix_region_id: str,
    object_type: str,  
    subregions_number: int,       
    region_type: str,  
    center_region: Point,     
    min_radian: float,
    max_radian: float,
    **kwargs        
) -> list[Union[Hotspot, WorkSpot]]:
    """
    obj_type: "hotspot" hoặc "workspot"
    region_type: "circle", "rectangle", "ellipse"
    subregions_number: số điểm cần gen
    min_radian, max_radian: khoảng bán kính của từng điểm dân số
    kwargs: center, width, height... tùy theo hình

    Lưu ý: workspot chỉ tạo và chưa tính atraccive, cần phải thêm 1 bước tính sau nũa
    """
    
    x_coords, y_coords = np.zeros(subregions_number), np.zeros(subregions_number)

    # --- 1. Xử lý logic tọa độ theo từng loại Region ---
    if region_type == "circle":
        r_region = kwargs.get('radius_region', 1000)
        safe_r = max(0, r_region - max_radian)
        rad = np.sqrt(np.random.uniform(0, safe_r**2, subregions_number))
        theta = np.random.uniform(0, 2 * np.pi, subregions_number)
        x_coords = center_region.x + rad * np.cos(theta)
        y_coords = center_region.y + rad * np.sin(theta)

    elif region_type == "rectangle":
        w = kwargs.get('width', 2000)
        h = kwargs.get('height', 2000)
        safe_w, safe_h = max(0, w/2 - max_radian), max(0, h/2 - max_radian)
        x_coords = np.random.uniform(center_region.x - safe_w, center_region.x + safe_w, subregions_number)
        y_coords = np.random.uniform(center_region.y - safe_h, center_region.y + safe_h, subregions_number)

    elif region_type == "ellipse":
        a = kwargs.get('axis_a', 2000)
        b = kwargs.get('axis_b', 1000)
        
        safe_a = max(0, a - max_radian)
        safe_b = max(0, b - max_radian)
        
        rho = np.sqrt(np.random.uniform(0, 1, subregions_number))
        phi = np.random.uniform(0, 2 * np.pi, subregions_number)
        
        x_coords = center_region.x + safe_a * rho * np.cos(phi)
        y_coords = center_region.y + safe_b * rho * np.sin(phi)
    
    else:
        raise ValueError(f"Loại vùng '{region_type}' không được hỗ trợ!")

    # --- 2. Xử lý bán kính riêng của từng điểm ---
    point_radii = np.random.uniform(min_radian, max_radian, subregions_number)

    # --- 3. Khởi tạo danh sách Object ---
    objects = []
    if object_type.lower() == "hotspot":
        # Xử lý logic phân bổ Dân số
        population_number = kwargs.get('population_number', 1000)
        weights = np.random.dirichlet(np.ones(subregions_number))
        pop_values = np.round(weights * population_number).astype(int)
        pop_values[np.argmax(pop_values)] += (int(population_number) - pop_values.sum()) 
        # Tạo Hotspot
        for i in range(subregions_number):
            p_obj = Point(x=float(x_coords[i]), y=float(y_coords[i]))          
            objects.append(Hotspot(id=f"{prefix_region_id}_{i}", coords=p_obj, r=point_radii[i], n_pop=pop_values[i]))
    
    elif object_type.lower() == "workspot":
        for i in range(subregions_number):
            p_obj = Point(x=float(x_coords[i]), y=float(y_coords[i]))
            objects.append(WorkSpot(id=f"{prefix_region_id}_{i}", coords=p_obj, r=point_radii[i], attractiveness=0))
            
    return objects

    

