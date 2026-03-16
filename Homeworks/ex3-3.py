import math

n = 2022
x = math.pi
word = "Python"
polish = "książka"

with open("ex3-3-vars.txt", "w", encoding="utf-8") as file:
    file.write(f'{n}\n{x:.5f}\n{word}\n{polish}')
    
with open("ex3-3-vars.txt", 'r', encoding="utf-8") as file:
    for line in file:
        print(line, end='')
