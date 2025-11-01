import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, cos, pi, lambdify

x, y, t = symbols("x y t")
fun = (2 + cos(2 * pi * x) * cos(2 * pi * y)) * t

# Convert sympy expression to a function that can be called with numpy arrays
fun_lambdified = lambdify((x, y, t), fun, "numpy")

# Generate x and y values
x_values = np.linspace(0, 1, 100)
y_values = np.linspace(0, 1, 100)

# Choose a value for t
t_value = 1  # replace with your desired value

# Calculate z values
X, Y = np.meshgrid(x_values, y_values)
Z = fun_lambdified(X, Y, t_value)

# Plot the function
plt.imshow(Z, extent=[0, 1, 0, 1], origin="lower", cmap="viridis")
plt.colorbar(label="fun")
plt.xlabel("x")
plt.ylabel("y")
plt.title("2D color plot of fun for x, y in [0, 1]")
plt.grid(True)

# Add three random lines with minimum length of 0.5
for _ in range(3):
    x_start, y_start = np.random.uniform(0.5, 1, 2)
    angle = np.random.uniform(0, 2 * np.pi)
    length = np.random.uniform(0.5, 1)
    x_end = x_start + length * np.cos(angle)
    y_end = y_start + length * np.sin(angle)
    # Ensure the end points are within [0, 1]
    x_end = np.clip(x_end, 0, 1)
    y_end = np.clip(y_end, 0, 1)
    plt.plot([x_start, x_end], [y_start, y_end], color="red")

plt.show()

# Plot the value of fun along the lines
for i in range(3):
    x_start, y_start = np.random.uniform(0.5, 1, 2)
    angle = np.random.uniform(0, 2 * np.pi)
    length = np.random.uniform(0, 0.5)
    x_end = x_start + length * np.cos(angle)
    y_end = y_start + length * np.sin(angle)
    # Ensure the end points are within [0, 1]
    x_end = np.clip(x_end, 0, 1)
    y_end = np.clip(y_end, 0, 1)
    x_line = np.linspace(x_start, x_end, 100)
    y_line = np.linspace(y_start, y_end, 100)
    Z_line = fun_lambdified(x_line, y_line, t_value)
    plt.figure(i)
    plt.plot(x_line, Z_line, color="red")
    plt.xlabel("x")
    plt.ylabel("fun")
    plt.title(
        f"Plot of fun along the line from ({x_start:.2f}, {y_start:.2f}) to ({x_end:.2f}, {y_end:.2f})"
    )
    plt.grid(True)
    plt.show()
