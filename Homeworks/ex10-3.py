import numpy as np
import pandas as pd

# list from ex2-4b
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

pt = np.array(pt)
periodic_table = pd.DataFrame(
    pt[:, 1:], 
    index = pt[:, 0], 
    columns=["Name", "Symbol", "Weight"]
    )

print(periodic_table)