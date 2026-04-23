import itertools
import random

random.seed()

iter_a = itertools.cycle([0, 1])
iter_b = iter((lambda: random.choice([0, 1])), -1)
iter_c = map(int, map(pow, itertools.cycle([0, -1]), itertools.count(1.5, 0.5)))
iter_c_simple = itertools.cycle([0, 1, 0, -1])

N = 15
results = [[], [], [], []]
for idx, iter in enumerate([iter_a, iter_b, iter_c, iter_c_simple]):
    n = N
    for i in iter:
        if n == 0:
            break
        n -= 1
        results[idx].append(i)

print(f"First {N} elements for:")
print(f"{'iterator a:'.rjust(22)} {results[0]}.")
print(f"{'iterator b:'.rjust(22)} {results[1]}.")
print(f"{'iterator c:'.rjust(22)} {results[2]}.")
print(f"{'iterator c_simple:'.rjust(22)} {results[3]}.")


"""
Examples:

First 10 elements for:                                                                                                                                                                     
           iterator a: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1].
           iterator b: [1, 0, 1, 1, 0, 1, 0, 1, 1, 1].
           iterator c: [0, 1, 0, -1, 0, 1, 0, -1, 0, 1].
    iterator c_simple: [0, 1, 0, -1, 0, 1, 0, -1, 0, 1].

First 15 elements for:                                                                                                                                                                     
           iterator a: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0].
           iterator b: [1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0].
           iterator c: [0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0].
    iterator c_simple: [0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0].
"""
