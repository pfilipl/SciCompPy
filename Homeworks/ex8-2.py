import numpy as np

rng = np.random.default_rng()

v1 = np.arange(rng.integers(20))
v2 = v1[1::2]
v3 = v1[::-1]

for idx, array in enumerate([v1, v2, v3]):
    print(f"v{idx + 1} [shape={array.shape}]: {array}")

"""
Example:

v1 [shape=(15,)]: [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14]                                                                           
v2 [shape=(7,)]: [ 1  3  5  7  9 11 13]
v3 [shape=(15,)]: [14 13 12 11 10  9  8  7  6  5  4  3  2  1  0]
"""
