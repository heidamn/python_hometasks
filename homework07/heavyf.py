import random
import numpy as np

def heavy_computation(data_chunk):
    mass1 = np.array([[random.randint(data_chunk, 1000 * (data_chunk+1)) for _ in range(1000)] for _ in range(1000)])
    mass2 = np.array([[random.randint(-data_chunk, data_chunk) for _ in range(1000)] for _ in range(1000)])
    mass3 = mass1 * mass2