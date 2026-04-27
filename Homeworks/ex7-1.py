from ex6 import Vector


def find_axis(v1, v2):
    v0 = Vector()

    if v1 == v0 or v2 == v0:
        raise ValueError("At elast one of the given vectors is zero.")

    v3 = v1.cross(v2)
    if v3 == v0:
        raise ValueError("The given vectors are parallel.")

    return v3.norm()


if __name__ == "__main__":
    # Tests:
    i2 = Vector(2, 0, 0)
    j2 = Vector(0, 2, 0)

    assert find_axis(i2, j2) == Vector(0, 0, 1)
    assert find_axis(j2, i2) == -Vector(0, 0, 1)
    
    u = Vector()
    v = Vector(1, 2, 3)
    w = Vector(-4, 5, 1)
    x = Vector(2, 4, 6)

    try:
        find_axis(u, v)
    except ValueError as e:
        print(e)

    try:
        find_axis(v, x)
    except ValueError as e:
        print(e)

    assert find_axis(v, w) == find_axis(x, w)
    
