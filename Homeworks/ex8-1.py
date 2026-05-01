import numpy as np

array_a = np.linspace(0, 1, 11)
array_b = np.zeros((5, 6), "int8")
array_c = np.power(complex(0, 1), np.arange(9))

for name, array in zip(["a", "b", "c"], [array_a, array_b, array_c]):
    print(f"Array {name} [shape={array.shape}, dtype={array.dtype}]:\n{array}")

"""
Results:

Array a [shape=(11,), dtype=float64]:                                                                                                      
[0.  0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1. ]
Array b [shape=(5, 6), dtype=int8]:
[[0 0 0 0 0 0]
 [0 0 0 0 0 0]
 [0 0 0 0 0 0]
 [0 0 0 0 0 0]
 [0 0 0 0 0 0]]
Array c [shape=(9,), dtype=complex128]:
[ 1.+0.j  0.+1.j -1.+0.j -0.-1.j  1.+0.j  0.+1.j -1.+0.j -0.-1.j  1.+0.j]
"""
