import numpy as np
from scipy.integrate import quad

def density_function_base_saturation_gradient_method_func(x: float, p0: float, beta_gradient_method: float):
    """
    x là khảng cách từ 1 điển đến tâm
    p0 là mật độ người/ km^2 ở  điểm các tâm là x = 0
    """
    return p0 * np.exp(-beta_gradient_method * x) * 2 * np.pi * x

def calc_circular_ring_density(r: float, denta_r: float, p0: float, beta_gradient_method: float) -> float:
    result, error = quad(lambda x: density_function_base_saturation_gradient_method_func(x=x, p0=p0, beta_gradient_method=beta_gradient_method), r, r + denta_r)
    return result 
    
if __name__ ==  "__main__":
    print(calc_circular_ring_density(r=1.0, denta_r=2.0, p0=100.0, beta_gradient_method=1.0))