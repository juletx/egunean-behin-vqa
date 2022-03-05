"""This module contains the functions that create cube figures."""
import argparse
import os
import random

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from tqdm import trange


def neighbors_in_front(x, y, heights, shape):
    """
    Returns the positions of empty neighbors given a current position, those neighbors being in front of that position
    :param x: current row index of dimension x
    :param y: current row index of dimension y
    :param heights: [x_len, y_len] matrix, each value specifying the number of cubes in a column
    :param shape:  (x_len, y_len, z_len) tuple
    :return: empty neighbor positions being in front of the current location
    """
    x_len, y_len, _ = shape
    neighborhood = []
    if x > 0 and heights[x - 1][y] == 0:
        if y == y_len - 1 or heights[x - 1][y + 1] != 0:
            neighborhood.append((x - 1, y))
    if y > 0 and heights[x][y - 1] == 0:
        if x == x_len - 1 or heights[x + 1][y - 1] != 0:
            neighborhood.append((x, y - 1))
    return neighborhood


def sort_by_heights(heights, shape):
    """
    Sorts randomly columns by height, so that each column in front of another is smaller or of equal length
    :param heights: [x_len, y_len] matrix, each value specifying the number of cubes in a column
    :param shape:  (x_len, y_len, z_len) tuple
    :return: sorted 'heights' matrix
    """
    x_len, y_len, z_len = shape

    counts = [(heights == z).sum() for z in range(z_len + 1)]
    new_heights = np.zeros((x_len, y_len), dtype=int)
    pos_list = [(x_len - 1, y_len - 1)]

    h = len(counts) - 1
    while counts[h] == 0:
        counts.pop(h)
        h -= 1

    while len(counts) > 1:
        x, y = pos_list.pop(np.random.randint(0, len(pos_list)))

        h = len(counts) - 1
        new_heights[x][y] = h
        counts[h] -= 1

        while counts[h] <= 0:
            counts.pop(h)
            h -= 1
            if h < 0:
                return new_heights

        neighborhood = neighbors_in_front(x, y, new_heights, shape)
        pos_list.extend([(x_new, y_new) for x_new,
                         y_new in neighborhood if new_heights[x_new][y_new] == 0])

    return new_heights


def figure_name(heights, shape):
    """
    Creates figure filename given its column heights and shape
    :param heights: [x_len, y_len] matrix, each value specifying the number of cubes in a column
    :param shape: (x_len, y_len, z_len) tuple
    :return: filename of figure
    """
    x_len, y_len, z_len = shape
    name = f"fig_{x_len}_{y_len}_{z_len}"

    for row in heights:
        hex_row = [str(hex(elem))[-1] for elem in row]
        name += '_' + ''.join(hex_row)

    return name + ".png"


def create_random_figure(args, repeated):
    """
    Creates a random figure given input values such as dimension lengths or color palettes
    :param args: input values
    :param repeated: number of times we tried to create a figure that already exists
    """
    x_len = args.x_len
    y_len = args.y_len
    z_len = args.z_len

    prob = args.prob

    # A) Decide height of each column of cubes
    heights = np.zeros((x_len, y_len))

    for i in range(z_len):
        for x in range(x_len):
            for y in range(y_len):
                if i == heights[x][y] and np.random.rand() < prob:
                    heights[x][y] += 1

    # B) Sort cubes by height (the higher, the farther from the viewer)
    shape = (x_len, y_len, z_len)
    heights = sort_by_heights(heights, shape)

    # C) Check if this figure has already been created or has no cubes (by checking its filename)
    filename = figure_name(heights, shape)
    figure_path = f"{args.output_path}\\{filename}"

    if os.path.exists(figure_path) or heights.sum() == 0:
        if repeated < args.max_repeats:
            repeated += 1
            create_random_figure(args, repeated)
    else:
        # D) Create voxels and rearrange them to create the picture
        voxels = []
        for i in range(z_len):
            layer = np.array(
                [[True if elem > i else False for elem in heights[x]] for x in range(x_len)])
            voxels.append(layer)
        voxels = np.array(voxels)

        # E) Choose colors for each plane of cubes
        colors = np.empty(voxels.shape, dtype=object)
        if args.colormap == 'random':
            cmap = cm.get_cmap(random.choice(['rainbow', 'viridis', 'cool', 'twilight_shifted', 'brg', 'terrain',
                                              'ocean', 'winter', 'spring', 'cividis']))
        else:
            cmap = cm.get_cmap(args.colormap)

        # Assign colors to each voxel
        for i in range(z_len):
            r, g, b, a = cmap(i / z_len)
            str_rgb = '#{:02x}{:02x}{:02x}'.format(
                int(r * 255), int(g * 255), int(b * 255))
            colors[i][voxels[i]] = str_rgb

        # Swap axes to visualize better
        voxels = np.swapaxes(voxels, 0, 2)
        colors = np.swapaxes(colors, 0, 2)

        # F) Create and save plot
        dpi = 96
        fig = plt.figure(figsize=(600/dpi, 400/dpi), dpi=dpi)

        ax = fig.add_subplot(projection='3d')
        # Little trick to plot cubes correctly
        ax.set(xlim=(0, y_len), ylim=(0, x_len), zlim=(0, z_len))

        # set up the axes labels for the plot
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        # set up the axes ticks for the plot
        ax.set_xticks(np.arange(0, x_len + 1, 1))
        ax.set_yticks(np.arange(0, y_len + 1, 1))
        ax.set_zticks(np.arange(0, z_len + 1, 1))

        # set up the axes tick labels for the plot
        ax.set_xticklabels(np.arange(0, x_len + 1, 1))
        ax.set_yticklabels(np.arange(0, y_len + 1, 1))
        ax.set_zticklabels(np.arange(0, z_len + 1, 1))

        ax.get_xaxis().set_tick_params(direction='out', pad=0)
        ax.get_yaxis().set_tick_params(direction='out', pad=0)
        ax.get_zaxis().set_tick_params(direction='out', pad=0)

        ax.view_init(35, -125)
        ax.voxels(voxels, facecolors=colors, edgecolor='k')

        fig.canvas.draw()
        fig.tight_layout()
        plt.savefig(figure_path, bbox_inches='tight')
        plt.close()


def parse_arguments():
    """
    Parse input values
    :return: input values
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--x_len",
        type=int,
        default=4,
        help="Number of cubes in axis X.",
    )

    parser.add_argument(
        "--y_len",
        type=int,
        default=4,
        help="Number of cubes in axis Y.",
    )

    parser.add_argument(
        "--z_len",
        type=int,
        default=3,
        help="Number of cubes in axis Z.",
    )

    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="Number of created pictures.",
    )

    parser.add_argument(
        "--prob",
        type=float,
        default=0.75,
        help="Probability to stack a cube on top of another. Value between 0 and 1 (not inclusive).",
    )

    parser.add_argument(
        "--max_repeats",
        type=int,
        default=20,
        help="How many times do we try to create another figure if we create an existing one.",
    )

    parser.add_argument(
        "--colormap",
        type=str,
        default='random',
        choices=['rainbow', 'viridis', 'cool', 'twilight_shifted', 'brg', 'terrain', 'ocean', 'winter', 'spring',
                 'cividis', 'random'],
        help="Colormap of the cubes.",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        default='images',
        help="Path for output files.",
    )

    return parser.parse_args()


def check_args(args):
    """
    Check input values
    :param args: input values
    :return: corrected input values
    """
    bool_value = False
    if args.x_len > 14:
        args.x_len = 14
        bool_value = True
    if args.y_len > 14:
        args.y_len = 14
        bool_value = True
    if args.z_len > 14:
        args.z_len = 14
        bool_value = True

    if bool_value:
        print("WARNING: Maximum number of cubes in a given dimension is 14! Larger values have been set to 14.")

    bool_value = False
    if args.x_len < 1:
        args.x_len = 1
        bool_value = True
    if args.y_len < 1:
        args.y_len = 1
        bool_value = True
    if args.z_len < 1:
        args.z_len = 1
        bool_value = True

    if bool_value:
        print("WARNING: Each dimension should have at least one cube! Lower values have been set to 1.")

    if args.prob <= 0.0 or args.prob >= 1.0:
        args.prob = 0.75
        print("WARNING: Probability of spawning a cube should be between 0.0 and 1.0 (not inclusive). Default: 0.75.")

    return args


def main():
    """Main function"""
    args = parse_arguments()
    args = check_args(args)

    for _ in trange(args.n, desc="Images"):
        create_random_figure(args, repeated=0)


if __name__ == '__main__':

    main()
