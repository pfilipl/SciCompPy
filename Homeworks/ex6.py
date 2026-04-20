import math


class Vector:
    """
    3D vectors implementation.
    """

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector({self.x!r}, {self.y!r}, {self.z!r})"

    def __str__(self):
        return f"({self.x:.4f}, {self.y:.4f}, {self.z:.4f})"

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __ne__(self, other):
        return not self == other

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector(
            -self.x,
            -self.y,
            -self.z,
        )

    def __add__(self, other):
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            return Vector(self.x * other, self.y * other, self.z * other)

    __rmul__ = __mul__

    def cross(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self):
        return math.hypot(self.x, self.y, self.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z))


# Tests:
v = Vector(math.sqrt(3), math.sqrt(3), math.sqrt(3))
w = Vector(3, 4, 0)
u = Vector(0, 0, 4)
q = Vector(0, 0, -1)

assert v != w
assert w + u == Vector(3, 4, 4)
assert u + w == w + u
assert w - u == Vector(3, 4, -4)
assert u - w == -w + u
assert w * 3 == Vector(9, 12, 0)
assert 2 * w == Vector(6, 8, 0)
assert v * w == 7 * math.sqrt(3)
assert w * v == v * w
assert w * u == 0
assert w.cross(u) == Vector(16, -12, 0)
assert u.cross(w) == -w.cross(u)
assert u.cross(q) == Vector()
assert v.length() == 3
assert len(set([v, v, w])) == 2

print(f"Representation of v is {repr(v)}.")
print(f"Tests for v={v}, w={w}, z={u}, and q={q} passed!")

"""
Results:

Representation of v is Vector(1.7320508075688772, 1.7320508075688772, 1.7320508075688772).                                                                                                 
Tests for v=(1.7321, 1.7321, 1.7321), w=(3.0000, 4.0000, 0.0000), z=(0.0000, 0.0000, 4.0000), and q=(0.0000, 0.0000, -1.0000) passed!
"""
