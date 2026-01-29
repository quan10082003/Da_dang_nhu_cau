import numpy as np

def get_random_normal(mean_val: float, std_dev: float):
    """
    Đầu vào: mean_val (giá trị trung bình)
    Đầu ra: 1 con số ngẫu nhiên theo phân phối chuẩn
    """
    return np.random.normal(loc=mean_val, scale=std_dev)

# Ví dụ:
if __name__ == "__main__":
    print(get_random_normal(10.0, 1.0))