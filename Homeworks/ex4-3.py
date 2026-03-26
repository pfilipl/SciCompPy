def iter_even():
    i = 0
    while True:
        yield i
        i += 2


def iter_odd():
    for i in iter_even():
        yield i + 1


def iter_power(k):
    i = 0
    while True:
        yield k**i
        i += 1


while True:
    try:
        even_max, odd_max, power_max= list(
            map(int, input("Enter maximum number for even, odd, and power generators: ").split(),
            )
        )
    except ValueError as e:
        print(f"ValueError: {e}, try again!")
        continue
    else:
        break
while True:
    try:
        power_base = int(input("Enter maximum number for even, odd, and power generators: "))
    except ValueError as e:
        print(f"ValueError: {e}, try again!")
        continue
    else:
        break

even = []
odd = []
power = []
for n in iter_even():
    if n >= even_max:
        break
    even.append(n)
for n in iter_odd():
    if n >= odd_max:
        break
    odd.append(n)
for n in iter_power(power_base):
    if n >= power_max:
        break
    power.append(n)

print(f'Even natural numbers smaller than {even_max}: {even}.')
print(f'Odd natural numbers smaller than {odd_max}: {odd}.')
print(f'Power natural numbers smaller than {power_max} and with power base {power_base}: {power}.')

'''
Example usage:

Enter maximum number for even, odd, and power generators: 10 14 64                                                                                                                         
Enter maximum number for even, odd, and power generators: 2
Even natural numbers smaller than 10: [0, 2, 4, 6, 8].
Odd natural numbers smaller than 14: [1, 3, 5, 7, 9, 11, 13].
Power natural numbers smaller than 64 and with power base 2: [1, 2, 4, 8, 16, 32].
'''