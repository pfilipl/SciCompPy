x = 5

x == 5 and 3 + 8  # 11          # 1st condition is true, 
                                # result of 2nd condition is returned

x == 4 and 3 + 8  # False       # 1st condition is false, 
                                # 2nd condition is not chcecked and returned

3 + 8 and x == 5  # True        # 1st condition is true (not zero, None, etc.), 
                                # result od 2nd condition is returned

3 + 8 and x == 4  # False       # 1st condition is true (not zero, None, etc.),
                                # 2nd condition is checked and returned

isinstance(True, int)  # True   # bool class is inherited from int class
isinstance(True, bool)  # True  # True is an instance of bool class
