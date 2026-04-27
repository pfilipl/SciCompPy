import itertools
import random

random.seed()


def iter_01():
    while True:
        yield 0
        yield 1


def iter_cycle(sequence):
    while True:
        for item in sequence:
            yield item


def iter_random(sequence):
    while True:
        yield random.choice(sequence)


iter_a = itertools.cycle([0, 1])
iter_b = iter((lambda: random.choice([0, 1])), -1)
iter_c = itertools.cycle([0, 1, 0, -1])
iter_c_fancy = map(int, map(pow, itertools.cycle([0, -1]), itertools.count(1.5, 0.5)))

N = 15
results = [[], [], [], [], [], [], []]
for idx, iter in enumerate(
    [
        iter_a,
        iter_b,
        iter_c,
        iter_c_fancy,
        iter_01(),
        iter_random([0, 1]),
        iter_cycle([0, 1, 0, -1]),
    ]
):
    n = N
    for i in iter:
        if n == 0:
            break
        n -= 1
        results[idx].append(i)

print(f"First {N} elements for:")
print(f"{'iterator a:'.rjust(18)} {results[0]}.")
print(f"{'iterator b:'.rjust(18)} {results[1]}.")
print(f"{'iterator c:'.rjust(18)} {results[2]}.")
print(f"{'iterator c_fancy:'.rjust(18)} {results[3]}.")
print(f"{'iterator a_gen:'.rjust(18)} {results[4]}.")
print(f"{'iterator b_gen:'.rjust(18)} {results[5]}.")
print(f"{'iterator c_gen:'.rjust(18)} {results[6]}.")


"""
Examples:

First 10 elements for:                                                                                                                                                                     
       iterator a: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1].
       iterator b: [1, 1, 0, 1, 0, 0, 0, 1, 0, 1].
       iterator c: [0, 1, 0, -1, 0, 1, 0, -1, 0, 1].
 iterator c_fancy: [0, 1, 0, -1, 0, 1, 0, -1, 0, 1].
   iterator a_gen: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1].
   iterator b_gen: [0, 0, 1, 1, 0, 1, 1, 0, 1, 1].
   iterator c_gen: [0, 1, 0, -1, 0, 1, 0, -1, 0, 1].
   
First 15 elements for:                                                                                                                                                                     
       iterator a: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0].
       iterator b: [1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1].
       iterator c: [0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0].
 iterator c_fancy: [0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0].
   iterator a_gen: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0].
   iterator b_gen: [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1].
   iterator c_gen: [0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0, -1, 0, 1, 0].
"""
