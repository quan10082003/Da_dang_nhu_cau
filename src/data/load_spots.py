import yaml

def load_spots_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config_data = yaml.safe_load(file)
        
        hotspots = config_data.get('hotspots', [])
        workspots = config_data.get('workspots', [])
        
        return hotspots, workspots


if __name__ == "__main__":
    hotspots_list, workspots_list = load_spots_config('.\config\config_location.yaml')
    print("--- Danh sách Hotspots ---")
    for hs in hotspots_list:
        print(f"Toạ độ: x={hs['x']}, y={hs['y']} | Số lượng: {hs['n']}")

    print("\n--- Danh sách Workspots ---")
    for ws in workspots_list:
        print(f"Toạ độ: x={ws['x']}, y={ws['y']} | Bán kính: {ws['r']}")