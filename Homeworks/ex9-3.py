import matplotlib.pyplot as plt
import numpy as np


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# SIMPLE APPROACH


def simple_ellipse(
    point: tuple[float, float],
    focus1: tuple[float, float],
    focus2: tuple[float, float],
    ) -> float | None:
    """
    The function returns sum of cartesian distances between object 'point' 
    and objects 'focus1' and 'focus2', that is distance('point', 'focus1') 
    \\+ distance('point', 'focus2').
    """
    
    return (
        np.sqrt((focus1[0]-point[0])**2 + (focus1[1]-point[1])**2)
        + np.sqrt((focus2[0]-point[0])**2 + (focus2[1]-point[1])**2)
    )

# End of simple_ellipse(
#     point: tuple[float, float],
#     focus1: tuple[float, float],
#     focus2: tuple[float, float],
#     ) -> float | None:


# Grid preparation
xmin, xmax, nx = -2, 2, 101
ymin, ymax, ny = -2, 2, 101
x = np.linspace(xmin, xmax, nx)
y = np.linspace(ymin, ymax, ny)
xx, yy = np.meshgrid(x, y)
points = np.array([xx, yy]).reshape((2, nx*ny))

# Figure preparation
fig, ax = plt.subplots(1, 1)

# Focus definition and computations
f1, f2 = (-1, 0), (1, 0)
zzz = np.empty((nx*ny))
for idx, point in enumerate(points.transpose()):
    zzz[idx] = simple_ellipse((point[0], point[1]), f1, f2)

# Main image
img = ax.imshow(zzz.reshape((nx, ny)), origin="lower", cmap="viridis_r")

# Additional elements
contours = ax.contour(zzz.reshape(nx, ny), colors='k', alpha=0.5)
ax.clabel(contours)
ax.scatter(
    [(f1[0]-xmin)*nx/(xmax-xmin), (f2[0]-xmin)*nx/(xmax-xmin)],
    [(f1[1]-ymin)*ny/(ymax-ymin), (f2[1]-ymin)*ny/(ymax-ymin)], 
    [30, 30], 'r')
ax.axis("off")
axx = ax.secondary_xaxis(
    "bottom", 
    (
        lambda x: x*((xmax-xmin)/nx)+xmin, 
        lambda x: (x-xmin)*nx/(xmax-xmin)
        ),
    )
axy = ax.secondary_yaxis(
    "left", 
    (
        lambda y: y*(ymax-ymin)/ny+ymin, 
        lambda y: (y-ymin)*ny/(ymax-ymin)
        ),
    )
axx.set_xlabel("x")
axy.set_ylabel("y")
ax.set_title("Homework 9 ex 3 simple")

# Figure saving or showing
fig.savefig("Homeworks/ex9-3-simple.png", dpi=300)
# plt.show()


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ADVANCED APPROACH 


def distance(
    point1: np.ndarray[tuple[int, ...]] | float, 
    point2: np.ndarray[tuple[int, ...]] | float,
    ) -> np.ndarray[tuple[int, ...]] | float | None:
    """
    The function returns cartesian distance between two objects with the same shapes,
    or list of distances for object and a list of objects, and vice versa.

    Test examples:
    assert distance((0, 0), (0, 1)) == 1
    assert distance((0, 0, 0, 0, 0), (1, 1, 1, 1, 1)) == np.sqrt(5)
    assert distance([(0, 0), (0, 0)], [(0, 1), (0, 1)]) == np.sqrt(2)
    assert np.all(distance([(0, 0), (1, 0), (1, 1)], (0, 1)) == [1, np.sqrt(2), 1])
    assert np.all(distance((-1, 0), [(0, 0), (1, 0), (1, 1)]) == [1, 2, np.sqrt(5)])
    try:
        distance([[(0, 0), (1, 0)], [[1, 0], [1, 1]]], (0, 1))
    except ValueError as e:
        print(e)
    try:
        distance((0, 0), (0, 1, 2))
    except ValueError as e:
        print(e)
    """

    if not isinstance(point1, np.ndarray):
        point1 = np.array(point1)
    if not isinstance(point2, np.ndarray):
        point2 = np.array(point2)
    
    if point1.shape == point2.shape:
        return np.sqrt(np.sum((point2-point1)**2))
    if len(point1.shape) - 1 == len(point2.shape): 
        if point1.shape[-1:] == point2.shape:
            return np.sqrt(np.sum((point2[np.newaxis, :]-point1)**2, 1))
        if point1.shape[:1] == point2.shape:
            return np.sqrt(np.sum((point2[:, np.newaxis]-point1)**2, 0))
    elif len(point2.shape) - 1 == len(point1.shape): 
        if point2.shape[-1:] == point1.shape:
            return np.sqrt(np.sum((point2-point1[np.newaxis, :])**2, 1))
        if point2.shape[:1] == point1.shape:
            return np.sqrt(np.sum((point2-point1[:, np.newaxis])**2, 0))
    elif len(point1.shape) == len(point2.shape):
        raise ValueError(
            f"""Shapes of 'point1' {point1.shape} 
            and 'point2' {point2.shape} are different."""
            )
    else:
        raise ValueError(
            f"""
            Absolute difference between shapes of 'point1' 
            and point2' is greater than 1. 
            |len({point1.shape}) - len({point2.shape})| > 1.
            """
            )
        
# End of distance(
#     point1: np.ndarray[tuple[int, ...]] | float, 
#     point2: np.ndarray[tuple[int, ...]] | float,
#     ) -> np.ndarray[tuple[int, ...]] | float | None:


def ellipse(
    point: np.ndarray[tuple[int, ...]], 
    focus1: np.ndarray[tuple[int, ...]], 
    focus2: np.ndarray[tuple[int, ...]],
    ) -> np.ndarray[tuple[int, ...]] | float | None:
    """
    The function returns sum of cartesian distances between object 'point' 
    and objects 'focus1' and 'focus2', that is distance('point', 'focus1') 
    \\+ distance('point', 'focus2'), or list of distances for list of objects 
    'point' and objects 'focus1' and 'focus2', and vice versa.  

    Test examples:
    assert ellipse((0, 0), (-1, 0), (0, 1)) == 2
    assert np.all(ellipse([(0, 0), (0, 1)], (-1, 0), (0, 1)) == [2, np.sqrt(2)])
    assert np.all(ellipse((0, 0), [(-1, 0), (0, 1)], [(0, 1), (-1, 0)]) == [2, 2])
    try:
        ellipse((0, 0), (-1, 0, 1), (0, 1))
    except ValueError as e:
        print(e)
    try:
        ellipse((0, 0), [(-1, 0), (0, 1)], (0, 1))
    except ValueError as e:
        print(e)
    try:
        ellipse([[(0, 0), (0, 1)], [(0, 0), (0, 1)]], (-1, 0), (0, 1))
    except ValueError as e:
        print(e)
    """

    if not isinstance(point, np.ndarray):
        point = np.array(point)
    if not isinstance(focus1, np.ndarray):
        focus1 = np.array(focus1)
    if not isinstance(focus2, np.ndarray):
        focus2 = np.array(focus2)
    
    if focus1.shape == focus2.shape:
        if point.shape == focus1.shape:
            result = distance(
                point, np.array([focus1, focus2])
                )
            if isinstance(result, np.ndarray):
                return np.sum(result)
            else:
                return result
        elif len(point.shape) - 1 == len(focus1.shape):
            return np.sum(
                [
                    distance(point, focus1), 
                    distance(point, focus2)
                ], 
                0)
        elif len(point.shape) + 1 == len(focus1.shape):
            return np.sum(
                [
                    distance(point, focus1), 
                    distance(point, focus2)
                ],
                1
                )
        else:
            raise ValueError(
                f"""
                Absolute difference between shapes of 'point' and 'focus1' 
                is greater than 1. |len({point.shape}) - len({focus1.shape})| > 1.
                """
                )
    else:
        raise ValueError(
            f"""
            Shapes of 'focus1' {focus1.shape} and 'focus2' {focus2.shape} 
            are different.
            """
            )

# End of ellipse(
#     point: np.ndarray[tuple[int, ...]], 
#     focus1: np.ndarray[tuple[int, ...]], 
#     focus2: np.ndarray[tuple[int, ...]],
#     ) -> np.ndarray[tuple[int, ...]] | float | None:


# Grid preparation
xmin, xmax, nx = -2, 2, 101
ymin, ymax, ny = -2, 2, 101
x = np.linspace(xmin, xmax, nx)
y = np.linspace(ymin, ymax, ny)
xx, yy = np.meshgrid(x, y)
points = np.array([xx, yy]).reshape((2, nx*ny))

# Figure preparation
fig, ax = plt.subplots(1, 1)

# Focus definition and computations
f1, f2 = np.array((-1, 0)), np.array((1, 0))
zz = np.array(ellipse(points, f1, f2))

# Main image
img = ax.imshow(zz.reshape(nx, ny), origin="lower", cmap="viridis_r")

# Additional elements
contours = ax.contour(zz.reshape(nx, ny), colors='k', alpha=0.5)
ax.clabel(contours)
ax.scatter(
    [(f1[0]-xmin)*nx/(xmax-xmin), (f2[0]-xmin)*nx/(xmax-xmin)],
    [(f1[1]-ymin)*ny/(ymax-ymin), (f2[1]-ymin)*ny/(ymax-ymin)], 
    [30, 30], 'r')
ax.axis("off")
axx = ax.secondary_xaxis(
    "bottom", 
    (
        lambda x: x*((xmax-xmin)/nx)+xmin, 
        lambda x: (x-xmin)*nx/(xmax-xmin)
        ),
    )
axy = ax.secondary_yaxis(
    "left", 
    (
        lambda y: y*(ymax-ymin)/ny+ymin, 
        lambda y: (y-ymin)*ny/(ymax-ymin)
        ),
    )
axx.set_xlabel("x")
axy.set_ylabel("y")
ax.set_title("Homework 9 ex 3 advanced")

# Figure saving or showing
fig.savefig("Homeworks/ex9-3-advanced.png", dpi=300)
# plt.show()