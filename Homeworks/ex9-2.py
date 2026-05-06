import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng()

points = rng.random((100, 2))
x= np.linspace(0, 1, 100)

fig, ax = plt.subplots(1, 1)

marker_size = np.sum(30*np.abs(points), 1)
marker_color = np.full(points.shape[0], "r")
marker_color[np.sqrt(np.sum(points**2, 1)) < 1] = "g"

ax.plot(x, np.sqrt(1-x**2), '--', color="grey")
ax.scatter(points[:, 0], points[:, 1], marker_size, marker_color)

ax.set_title("Homework 9 ex 2")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.axis("equal")

fig.savefig("Homeworks/ex9-2.png", dpi=300)
# plt.show()