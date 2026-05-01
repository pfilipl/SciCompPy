import numpy as np

m1 = np.arange(4)[:, np.newaxis] * 10 + np.arange(5)
m2 = m1[:, ::-1]
m3 = m1[::-1, :]
m4 = m1[1:-1, 1:-1]

for idx, array in enumerate([m1, m2, m3, m4]):
    print(f"m{idx + 1} [shape={array.shape}]:\n{array}")

"""
Results:

m1 [shape=(4, 5)]:                                                                                                                         
[[ 0  1  2  3  4]
 [10 11 12 13 14]
 [20 21 22 23 24]
 [30 31 32 33 34]]
m2 [shape=(4, 5)]:
[[ 4  3  2  1  0]
 [14 13 12 11 10]
 [24 23 22 21 20]
 [34 33 32 31 30]]
m3 [shape=(4, 5)]:
[[30 31 32 33 34]
 [20 21 22 23 24]
 [10 11 12 13 14]
 [ 0  1  2  3  4]]
m4 [shape=(2, 3)]:
[[11 12 13]
 [21 22 23]]
"""
