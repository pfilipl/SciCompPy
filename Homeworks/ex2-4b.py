pt = [
    (1, "Hydrogen", "H", 1),
    (2, "Helium", "He", 4),
    (3, "Lithium", "Li", 7),
    (4, "Berylium", "Be", 9),
    (5, "Boron", "B", 11),
    (6, "Carbon", "C", 12),
    (7, "Nitrogen", "N", 14),
    (8, "Oxygen", "O", 16),
    (9, "Fluorine", "F", 19),
    (10, "Neon", "Ne", 20),
]

print(f'+{"-"*3}+{"-"*20}+{"-"*6}+{"-"*10}+')
print(f'|{"No.".rjust(3)}|{"Name (en)".ljust(20)}|{"Symbol".center(6)}|{"Weight (u)".rjust(10)}|')
print(f'+{"-"*3}+{"-"*20}+{"-"*6}+{"-"*10}+')

for (Z, name, symbol, A) in pt:
    print(f'|{str(Z).rjust(3)}|{name.ljust(20)}|{symbol.center(6)}|{str(A).rjust(10)}|')

print(f'+{"-"*3}+{"-"*20}+{"-"*6}+{"-"*10}+')

'''
Result:

+---+--------------------+------+----------+                                                                                                                                               
|No.|Name (en)           |Symbol|Weight (u)|
+---+--------------------+------+----------+
|  1|Hydrogen            |  H   |         1|
|  2|Helium              |  He  |         4|
|  3|Lithium             |  Li  |         7|
|  4|Berylium            |  Be  |         9|
|  5|Boron               |  B   |        11|
|  6|Carbon              |  C   |        12|
|  7|Nitrogen            |  N   |        14|
|  8|Oxygen              |  O   |        16|
|  9|Fluorine            |  F   |        19|
| 10|Neon                |  Ne  |        20|
+---+--------------------+------+----------+
'''