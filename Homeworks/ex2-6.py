t = (2, 4)

print(t[2])     # IndexError: tuple index out of range
                # tuple t has two items and its 1st index is zero 
t.append(6)     # AttributeError: 'tuple' object has no attribute 'append'
                # tuples are immutable and they cannot change size

a, b = t ; print(a, b)  # 2 4
                # variables a and b was assigned to t's items and then printed
