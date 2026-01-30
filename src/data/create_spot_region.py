from typing import List, Union
from src.domain.spot_location import Hotspot,WorkSpot
from src.domain.point import Point

import numpy as np

def generate_matsim_objects_in_region(
    prefix_region_id: str,
    obj_type: str,         
    region_type: str,  
    center_region: Point,     
    num_points: int,
    total_input: float,   
    min_r: float,
    max_r: float,
    **kwargs        
) -> list[Union[Hotspot, WorkSpot]]:
    """
    obj_type: "hotspot" hoặc "workspot"
    region_type: "circle", "rectangle", "ellipse"
    num_points: số điểm cần gen
    total_input: tổng dân số
    min_r, max_r: khoảng bán kính của từng điểm dân số
    kwargs: center, width, height... tùy theo hình

    Lưu ý: workspot chỉ tạo và chưa tính atraccive, cần phải thêm 1 bước tính sau nũa
    """
    
    x_coords, y_coords = np.zeros(num_points), np.zeros(num_points)

    # --- 1. Xử lý logic tọa độ theo từng loại Region ---
    if region_type == "circle":
        r_region = kwargs.get('radius_region', 1000)
        safe_r = max(0, r_region - max_r)
        rad = np.sqrt(np.random.uniform(0, safe_r**2, num_points))
        theta = np.random.uniform(0, 2 * np.pi, num_points)
        x_coords = center_region.x + rad * np.cos(theta)
        y_coords = center_region.y + rad * np.sin(theta)

    elif region_type == "rectangle":
        w = kwargs.get('width', 2000)
        h = kwargs.get('height', 2000)
        safe_w, safe_h = max(0, w/2 - max_r), max(0, h/2 - max_r)
        x_coords = np.random.uniform(center_region.x - safe_w, center_region.x + safe_w, num_points)
        y_coords = np.random.uniform(center_region.y - safe_h, center_region.y + safe_h, num_points)

    # --- PHẦN BỔ SUNG: ELLIPSE ---
    elif region_type == "ellipse":
        # a: bán kính trục ngang, b: bán kính trục dọc
        a = kwargs.get('axis_a', 2000)
        b = kwargs.get('axis_b', 1000)
        
        # Vùng an toàn để tâm điểm + max_r không vượt quá biên elip
        safe_a = max(0, a - max_r)
        safe_b = max(0, b - max_r)
        
        # Sử dụng sqrt của số ngẫu nhiên để đảm bảo phân bổ mật độ đều theo diện tích
        rho = np.sqrt(np.random.uniform(0, 1, num_points))
        phi = np.random.uniform(0, 2 * np.pi, num_points)
        
        # Công thức tham số: x = x0 + a*r*cos(phi), y = y0 + b*r*sin(phi)
        x_coords = center_region.x + safe_a * rho * np.cos(phi)
        y_coords = center_region.y + safe_b * rho * np.sin(phi)
    
    else:
        raise ValueError(f"Loại vùng '{region_type}' không được hỗ trợ!")

    # --- 2. Xử lý logic phân bổ Dân số ---
    weights = np.random.dirichlet(np.ones(num_points))
    values = np.round(weights * total_input).astype(int)
    values[np.argmax(values)] += (int(total_input) - values.sum()) 

    # --- 3. Xử lý bán kính riêng của từng điểm ---
    point_radii = np.random.uniform(min_r, max_r, num_points)

    # --- 4. Khởi tạo danh sách Object ---
    objects = []
    for i in range(num_points):
        p_obj = Point(x=float(x_coords[i]), y=float(y_coords[i]))
        
        if obj_type.lower() == "hotspot":
            objects.append(Hotspot(id=f"{prefix_region_id}_{i}", coords=p_obj, r=point_radii[i], n_pop=values[i]))
        elif obj_type.lower() == "workspot":
            objects.append(WorkSpot(id=f"{prefix_region_id}_{i}", coords=p_obj, r=point_radii[i], attractiveness=0))
            
    return objects

