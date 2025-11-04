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
            # Calculate the maximum length based on the start point and the domain
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


def lambdafyfunmetal(x_line, y_line, t_value, fun, K):
    x, y, t = symbols("x y t")
    fun_lambdified = lambdify((x, y, t), fun, "numpy")

    fun_lambdified2 = lambdify((x, y, t), fun * K, "numpy")

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
    fun_lambdified3 = lambdify((x, y, t), fun * K, "numpy")
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
    if mms == False:
        Z = np.where(
            (X > 0) & (Y > 0),
            fun_lambdified3(X, Y, t_value),
            fun_lambdified(X, Y, t_value),
        )

    # Plot the function
    plt.imshow(Z, extent=[-0.5, 0.5, -0.5, 0.5], origin="lower", cmap="viridis")
    fun_str = printing.latex(fun)
    # Use the function string as the label in the colorbar
    plt.colorbar(label="$" + fun_str + "$")
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
    plt.text(-0.25, -0.25, "1", color="white", fontdict={"size": 36})
    plt.text(0.25, 0.25, "2", color="white", fontdict={"size": 36})
    plt.xlim([-0.5, 0.5])
    plt.ylim([-0.5, 0.5])
    plt.xlabel("x [m]", fontsize=16)
    plt.ylabel("y [m]", fontsize=16)
    if mms == True:
        plt.savefig("MMS_MS_1.png", dpi=300)
    else:
        plt.savefig("MMS_M_1.png", dpi=300)
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
        xy_line = np.column_stack((x_line, y_line))
        indices = np.where((xy_line[:, 0] > 0) & (xy_line[:, 1] > 0))
        length = ((x_start - x_line) ** 2 + (y_start - y_line) ** 2) ** 0.5
        if mms == True:
            Z_line = lambdafyfunmms(x_line, y_line, t_value, fun, K)
        else:
            Z_line = lambdafyfunmetal(x_line, y_line, t_value, fun, K)
        original_color = to_rgb(color[i])
        h, l, s = colorsys.rgb_to_hls(*original_color)

        # Increase the lightness
        lighter_l = min(l + 0.3, 1)  # increase lightness by 30%, but don't exceed 1

        # Convert the HLS color back to RGB
        lighter_color = colorsys.hls_to_rgb(h, lighter_l, s)
        first_index = indices[0][0] if indices[0].size > 0 else len(length)

        ax2.plot(length[first_index:], Z_line[first_index:], color=lighter_color)
        ax1.plot(length[:first_index], Z_line[:first_index], color=color[i])

        color_line = griddata(
            (x_COMS, y_COMS), color_COMS, (x_line, y_line), method="nearest"
        )  # !!! Due to the "nearest" method, the marker may connect with the nearest mesh point
        # across the boundary, which may be not alligned with the analytical line

        if i == 0:
            ax2.plot(length[first_index:], Z_line[first_index:], color=lighter_color)
            ax1.plot(
                length[:first_index],
                Z_line[:first_index],
                color=color[i],
                label="MMS Solution",
            )
            ax1.scatter(
                length[:first_index:10],
                color_line[:first_index:10],
                color=color[i],
                marker="o",
                s=10,
                label="mHIT data",
            )
            ax2.scatter(
                length[first_index::10],
                color_line[first_index::10],
                color=lighter_color,
                s=10,
                marker="o",
            )
            ax1.tick_params(axis="y")
            ax1.set_xlabel("line length [m]", fontsize=16)
            ax1.set_ylabel("function value in material 1", color="black", fontsize=16)
            ax2.set_ylabel("function value in material 2", color="grey", fontsize=16)
            ax2.tick_params(axis="y", color="grey", labelcolor="grey")
            ax1.spines["top"].set_visible(False)
            ax2.spines["top"].set_visible(False)
            ax1.legend(frameon=False, loc="lower center", fontsize=16)
            ax2.legend(frameon=False, loc="lower center", fontsize=16)
        else:
            ax2.plot(length[first_index:], Z_line[first_index:], color=lighter_color)
            ax1.plot(length[:first_index], Z_line[:first_index], color=color[i])
            ax1.scatter(
                length[:first_index:10],
                color_line[:first_index:10],
                color=color[i],
                marker="o",
                s=10,
            )
        ax2.scatter(
            length[first_index::10],
            color_line[first_index::10],
            color=lighter_color,
            marker="o",
            s=10,
        )
        if mms == True:
            ax2.set_ylim([100, 10000])
        ax1.set_ylim([0, 50])
        if mms == False:
            ax2.set_ylim([0, 200])
    if mms == True:
        fig.savefig("MMS_MS_2.png", dpi=300)
    else:
        fig.savefig("MMS_M_2.png", dpi=300)
