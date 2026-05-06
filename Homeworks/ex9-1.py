import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 1000)

fig, ax = plt.subplots(1, 1)

ax.plot(x, np.sin(x), '-r', label="sin(x)")
ax.plot(x, np.cos(x), '--g', label="cos(x)")
ax.plot(x, np.exp(-x), ':b', label="exp(-x)")

ax.set_title("Homework 9 ex 1")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()

fig.savefig("Homeworks/ex9-1.png", dpi=300)
# plt.show()
