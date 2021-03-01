import numpy as np

a = np.array([
    [1, 1, 2, 3],
    [0, 2, 0, 0],
    [5, 1, 1, 0],
    [3, 3, 1, 0]
    ])
b = np.kron(a, np.ones((3,3)))
print(b)