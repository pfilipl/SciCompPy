name = input("Enter your name: ")
print("Hello {}!".format(name))
for char in name:
    print(char, ord(char))   # ASCII code (Py2) or Unicode code point (Py3)
input("Press any key ...")   # needed on Windows