for x in range(1, 40+1):
    if x == 13:
        continue
    elif x % 5 == 0 and x % 7 == 0:
        print(f'{x} is divided by 5 and 7')
    elif x % 5 == 0:
        print(f'{x} is divided by 5')
    elif x % 7 == 0:
        print(f'{x} is divided by 7')
    else:
        print(f'{x} is not iportant')

x = 1
while x <= 40:
    if x == 13:
        pass
    elif x % 5 == 0 and x % 7 == 0:
        print(f'{x} is divided by 5 and 7')
    elif x % 5 == 0:
        print(f'{x} is divided by 5')
    elif x % 7 == 0:
        print(f'{x} is divided by 7')
    else:
        print(f'{x} is not iportant')
    x += 1