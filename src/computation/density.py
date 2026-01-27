import numpy as np
from scipy.integrate import quad
from src.domain.point import Point

def density_function_base_saturation_gradient_model(x: float, p0 = 100, b = 1):
    return p0 * np.exp(-b * x) * 2 * np.pi * x

def calc_circular_ring_density(r: float, denta_r: float) -> float:
    result, error = quad(density_function_base_saturation_gradient_model, r, r + denta_r)
    return result 
    
if __name__ ==  "__main__":
    print(calc_circular_ring_density(1,2)/2)