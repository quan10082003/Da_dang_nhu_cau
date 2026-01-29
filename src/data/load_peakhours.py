import yaml

def load_peakhours(config_path: str) -> (list[float], list[float]):
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f) # tạo ra dict

        am_peakhours = [item["hour"] for item in config_data["peakhours"]["am"]]
        pm_peakhours = [item["hour"] for item in config_data["peakhours"]["pm"]]

        return am_peakhours, pm_peakhours


if __name__ == "__main__":
    
    am_peakhours, pm_peakhours = load_peakhours(r'./config/config.yaml')
    print(f"AM peak hours: {am_peakhours}")
    print(f"PM peak hours:  {pm_peakhours}")