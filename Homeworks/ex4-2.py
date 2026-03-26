def reverse_range_iterative(L, left, right):
    for i in range(abs(int((right - left) / 2)) + 1):
        if right - left < 0:
            i *= -1
        L[left + i], L[right - i] = L[right - i], L[left + i]


def reverse_range_recursive(L, left, right):
    if right - left > 2:
        reverse_range_recursive(L, left + 1, right - 1)
    elif right - left < -2:
        reverse_range_iterative(L, left - 1, right + 1)
    L[left], L[right] = L[right], L[left]


L = list(range(10))
print(f"Original L = {L}.")

while True:
    try:
        left, right = list(map(int, input("Enter left and right indexes: ").split()))
    except ValueError as e:
        print(f"ValueError: {e}, try again!")
        continue
    if all(x >= 0 and x < len(L) for x in [left, right]):
        if right - left < 0:
            print("Indexes are inverted, but I will get it!")
        break
    print(f"Wrong indexes, L has {len(L)} elements!")

reverse_range_iterative(L, left, right)
results = f"After iterative inversing L = {L}."

reverse_range_recursive(L, left, right)
results += f"\nAfter recursive inversing L = {L}, which should be equal to original L."

print(results)

"""
Example usage:

Original L = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].                                                                                                                                               
Enter left and right indexes: 5 10
Wrong indexes, L has 10 elements!
Enter left and right indexes: 9 5
Indexes are inverted, but I will get it!
After iterative inversing L = [0, 1, 2, 3, 4, 9, 8, 7, 6, 5].
After recursive inversing L = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], which should be equal to original L.
"""
