number = 0
while number <= 3:
    try:
        number = int(input("Enter a positive integer greater than 3: "))
    except ValueError as e:
        print(f"[ERROR] {e}")
        continue
print(f"1*1 + 3*3 + ... + {number}*{number} = {sum(x*x for x in range(1, number, 2))}")

# for number = 2027 result is 1386011925