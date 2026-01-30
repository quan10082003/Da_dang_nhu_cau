from src.domain.spot_location import Hotspot,WorkSpot
from src.domain.point import Point
from src.computation.attractive import calc_attractiveness_of_workspot
from src.data.create_spot_region import generate_matsim_objects_in_region

import yaml
import json
from dataclasses import asdict
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

def save_spots_to_debug(path: str, hotspots: list, workspots: list):
    data = {
        "hotspots": [asdict(h) for h in hotspots],
        "workspots": [asdict(w) for w in workspots]
    }
    with open(path, 'w', encoding='utf-8') as f:
        # Thêm cls=NumpyEncoder vào đây
        json.dump(data, f, indent=4, ensure_ascii=False, cls=NumpyEncoder)
    print(f"--- Đã lưu dữ liệu debug vào: {path} ---")


def load_spots_config(file_path) -> (list[Hotspot], list[WorkSpot]):
    with open(file_path, 'r', encoding='utf-8') as file:
        config_data = yaml.safe_load(file)
        
        hotspots_list = [Hotspot(item["id"], Point(item["x"], item["y"]), item["r"], item["n_pop"]) for item in config_data.get('hotspots', [])]
        temp_workspots_list = [WorkSpot(item["id"], Point(item["x"], item["y"]), item["r"], 0) for item in config_data.get('workspots', [])]

        workspots_list = []
        for temp in temp_workspots_list:
            attractiveness = calc_attractiveness_of_workspot(workspot=temp, hotspot_list=hotspots_list)
            workspots_list.append(WorkSpot(temp.id, temp.coords, temp.r, attractiveness))
     
        return hotspots_list, workspots_list


if __name__ == "__main__":
    # hotspots_list, workspots_list = load_spots_config('.\config\config.yaml')
    # print("--- Danh sách Hotspots ---")
    # for hs in hotspots_list:
    #     print(f"ID: {hs.id} | Toạ độ: x={hs.coords.x}, y={hs.coords.y} | Bán kính: {hs.r} | Số lượng: {hs.n_pop}")

    # print("\n--- Danh sách Workspots ---")
    # for ws in workspots_list:
    #     print(f"ID: {ws.id} | Toạ độ: x={ws.coords.x}, y={ws.coords.y} | Bán kính: {ws.r} | Độ hấp dẫn: {ws.attractiveness}")
    path = r"data\interim\step0_spot_info.json"
    hs, ws = create_spots_list(path)