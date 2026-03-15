Roman2Arabic = dict(
    zip(
        ["I", "IV", "V", "IX", "X", "XL", "L", "XC", "C", "CD", "D", "CM", "M"],
        [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000],
    )
)

roman = input("Enter correct Roman number: ")

arabic = 0
skip = False
for i in range(len(roman)):
    if skip:
        skip = False
        continue
    if i + 2 < len(roman):
        if (
            roman[i : i + 2] in Roman2Arabic.keys()
            and roman[i + 1 : i + 3] in Roman2Arabic.keys()
        ):
            raise ValueError(
                f"Roman number is incorrect: {roman[i : i + 3]} conversion is undefined."
            )
    if i + 1 < len(roman) and roman[i : i + 2] in Roman2Arabic.keys():
        arabic += Roman2Arabic[roman[i : i + 2]]
        skip = True
    else:
        arabic += Roman2Arabic[roman[i]]

print(f"{roman} in Arabic numbers is: {arabic}")

'''
Example:
XCDXCIX     -> ValueError
MCDXCIX     -> 1499
MCDLXXXIV   -> 1484

'''

'''
Other methods to create Roman2Arabic dictionary:

Roman2Arabic = {
    "I": 1,
    "IV": 4,
    "V": 5,
    "IX": 9,
    "X": 10,
    "XL": 40,
    "L": 50,
    "XC": 90,
    "C": 100,
    "CD": 400,
    "D": 500,
    "CM": 900,
    "M": 1000,
}

Roman2Arabic = dict(
    [
        ("I", 1),
        ("IV", 4),
        ("V", 5),
        ("IX", 9),
        ("X", 10),
        ("XL", 40),
        ("L", 50),
        ("XC", 90),
        ("C", 100),
        ("CD", 400),
        ("D", 500),
        ("CM", 900),
        ("M", 1000),
    ]
)
'''