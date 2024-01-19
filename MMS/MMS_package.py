from scipy.interpolate import griddata
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, cos, pi, lambdify, printing
from matplotlib.colors import to_rgb
import colorsys


def generate_random_lines(num_lines=5, min_length=0.5, domain=[-0.5, 0.5]):
    lines = []
    for _ in range(num_lines):
        while True:
            # Generate a random start point
            x_start, y_start = np.random.uniform(
                domain[0],
                domain[1],
                2,
            )

            # Generate a random angle
            angle = np.random.uniform(0, 2 * np.pi)

            # Calculate the maximum length based on the start point and the domain
            max_length_x = min(x_start - domain[0], domain[1] - x_start)
            max_length_y = min(y_start - domain[0], domain[1] - y_start)
            max_length = min(max_length_x, max_length_y) * np.sqrt(2)

            # Generate a random length
            length = 0.5

            # Calculate the end point
            x_end, y_end = np.random.uniform(
                domain[0],
                domain[1],
                2,
            )
            if x_start < 0 and x_end > 0 and y_start < 0 and y_end > 0:
                # If it does, add the line to the list and break the loop
                lines.append(((x_start, y_start), (x_end, y_end)))
                if ((x_start - x_end) ** 2 + (y_start - y_end) ** 2) ** 0.5 > length:
                    break
    return lines


def lambdifyfun(fun):
    x, y, t = symbols("x y t")
    return lambdify((x, y, t), fun, "numpy")


def lambdafyfunmms(x_line, y_line, t_value, fun, K):
    x, y, t = symbols("x y t")
    fun_lambdified = lambdify((x, y, t), fun, "numpy")
    fun_lambdified2 = lambdify((x, y, t), fun**2 * K, "numpy")

    return np.where(
        (x_line > 0) & (y_line > 0),
        fun_lambdified2(x_line, y_line, t_value),
        fun_lambdified(x_line, y_line, t_value),
    )


def plotfun(fun, K, filename, n_lines=3, mms=False):
    x, y, t = symbols("x y t")
    # Create a light source
    fun_lambdified = lambdify((x, y, t), fun, "numpy")
    fun_lambdified2 = lambdify((x, y, t), fun**2 * K, "numpy")
    # Generate x and y values
    x_values = np.linspace(-0.5, 0.5, 100)
    y_values = np.linspace(-0.5, 0.5, 100)

    # Choose a value for t
    t_value = 10  # replace with your desired value

    # Calculate z values
    X, Y = np.meshgrid(x_values, y_values)
    Z = fun_lambdified(X, Y, t_value)
    if mms == True:
        Z = np.where(
            (X > 0) & (Y > 0),
            fun_lambdified2(X, Y, t_value),
            fun_lambdified(X, Y, t_value),
        )

    # Plot the function
    plt.imshow(Z, extent=[-0.5, 0.5, -0.5, 0.5], origin="lower", cmap="viridis")
    fun_str = printing.latex(fun)

    # Use the function string as the label in the colorbar
    plt.colorbar(label=fun_str)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    color = [
        "red",
        "green",
        "blue",
        "yellow",
        "black",
        "pink",
        "orange",
        "purple",
        "brown",
        "grey",
    ]
    # Add three random lines with minimum length of 0.5
    generated_lines = generate_random_lines(
        num_lines=n_lines, min_length=0.5, domain=[-0.5, 0.5]
    )
    for i, line in enumerate(generated_lines):
        (x_start, y_start), (x_end, y_end) = line
        plt.plot([x_start, x_end], [y_start, y_end], color=color[i])
    plt.xlim([-0.5, 0.5])
    plt.ylim([-0.5, 0.5])
    plt.show()
    COMS = np.loadtxt(filename)

    # Split the data into x, y, and color
    x_COMS = COMS[:, 0]
    y_COMS = COMS[:, 1]
    color_COMS = COMS[:, 2]
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    for i in range(len(generated_lines)):
        x_start, y_start = generated_lines[i][0]
        x_end, y_end = generated_lines[i][1]
        # Ensure the end points are within [0, 1]
        x_end = np.clip(x_end, 0, 1)
        y_end = np.clip(y_end, 0, 1)
        x_line = np.linspace(x_start, x_end, 100)
        y_line = np.linspace(y_start, y_end, 100)
        length = ((x_start - x_line) ** 2 + (y_start - y_line) ** 2) ** 0.5
        if mms == True:
            Z_line = lambdafyfunmms(x_line, y_line, t_value, fun, K)
        else:
            Z_line = fun_lambdified(x_line, y_line, t_value)
        original_color = to_rgb(color[i])
        h, l, s = colorsys.rgb_to_hls(*original_color)

        # Increase the lightness
        lighter_l = min(l + 0.3, 1)  # increase lightness by 30%, but don't exceed 1

        # Convert the HLS color back to RGB
        lighter_color = colorsys.hls_to_rgb(h, lighter_l, s)
        mask1 = (Z_line >= 0) & (Z_line <= 50)

        # Use the mask to filter Z_line and length
        Z_line_masked1 = Z_line[mask1]
        length_masked1 = length[mask1]
        mask2 = (Z_line >= 100) & (Z_line <= 10000)

        # Use the mask to filter Z_line and length
        Z_line_masked2 = Z_line[mask2]
        length_masked2 = length[mask2]
        ax1.plot(length_masked1, Z_line_masked1, color=lighter_color)
        ax2.plot(length_masked2, Z_line_masked2, color=color[i])
        ax1.set_xlabel("x [m]")
        ax1.set_ylabel("fun", color=color[1])
        ax1.tick_params(axis="y", labelcolor=color[1])
        color_line = griddata(
            (x_COMS, y_COMS), color_COMS, (x_line[::10], y_line[::10]), method="cubic"
        )
        ax1.scatter(length[::10], color_line, color=lighter_color, marker="x")
        ax2.scatter(length[::10], color_line, color=color[i], marker="x")
        ax2.set_ylabel(
            "color", color=color[2]
        )  # we already handled the x-label with ax1
        ax2.tick_params(axis="y", labelcolor=color[2])
        ax2.set_ylim([100, 10000])
        ax1.set_ylim([1, 50])
        # otherwise the right y-label is slightly clipped
    plt.xlabel("x")
    ax1.set_ylabel("function value in material")
    ax2.set_ylabel("function value in molten salt")

    plt.title("MMS on projected lines")
    plt.show()
