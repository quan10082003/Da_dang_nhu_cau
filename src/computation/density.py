import numpy as np
from scipy.integrate import quad
from src.domain.point import Point

def density_function_base_saturation_gradient_method_func(x: float, p0 = 100, b = 1):
    """
    x là khảng cách từ 1 điển đến tâm
    p0 là mật độ người/ km^2 ở  điểm các tâm là x = 0
    """
    return p0 * np.exp(-b * x) * 2 * np.pi * x

def calc_circular_ring_density(r: float, denta_r: float) -> float:
    result, error = quad(density_function_base_saturation_gradient_method_func, r, r + denta_r)
    return result 
    
if __name__ ==  "__main__":
    print(calc_circular_ring_density(1,2)/2)