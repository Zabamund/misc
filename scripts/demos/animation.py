import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

# Fixing circle radius and n points
r, n = 1, 12
# Fix plot ticks
ticks = np.array(range(-10,11,5)) / 10

# Create new Figure and an Axes which fills it.
fig, ax = plt.subplots(figsize=(4,4), ncols=1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_title(f'Perimeter plot')
ax.grid()

# Create x, y points
x = perimeter(r, n)[:,0]
y = perimeter(r, n)[:,1]

# Initialize alphas and rgba colors
alphas = np.linspace(0.1, 1, n)
rgba_colors = np.zeros((n,4))
rgba_colors[:, 3] = alphas

# Construct the scatter which we will update during animation
scat = ax.scatter(x, y, c=rgba_colors)

# define the function that will be called by `FuncAnimation()`
def rotate(frame_number):
    """rotate the alpha linspace"""
    last = alphas[-1]
    alphas = np.delete(alphas, -1)
    alphas = np.insert(alphas, 0, last)
    scat.set_color(c=rgba_colors)

# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, rotate, interval=500, blit=True, repeat=True)
plt.show()
