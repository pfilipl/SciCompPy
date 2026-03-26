import math

eps = 1e-6

point_list = [
    (-1, 0.5),
    (0, 0),
    (0, 0.5),
    (math.sqrt(2) / 2, math.sqrt(2) / 2),
    (1, -2),
]

results = f"Function a:\n{list(filter(lambda p: sum(x * x for x in p) - 1 <= eps, point_list))}"
results += f"\nFunction b:\n{list(filter(lambda p: all(x > 0 for x in p), point_list))}"
results += f"\nFunction c:\n{sorted(point_list, key=lambda p: (-p[1], p[0]))}"
results += f"\nFunction d:\n{sorted(point_list, key=lambda p: sum(abs(x) for x in p))}"

print(results)

'''
Results for point_list above:

Function a:                                                                                                                                                                               
[(0, 0), (0, 0.5), (0.7071067811865476, 0.7071067811865476)]
Function b:
[(0.7071067811865476, 0.7071067811865476)]
Function c:
[(0.7071067811865476, 0.7071067811865476), (-1, 0.5), (0, 0.5), (0, 0), (1, -2)]
Function d:
[(0, 0), (0, 0.5), (0.7071067811865476, 0.7071067811865476), (-1, 0.5), (1, -2)]
'''