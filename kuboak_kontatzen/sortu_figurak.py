import argparse
import os
import random

import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # <--- This is important for 3D plotting
import numpy as np
from tqdm import trange

# Global Variables
REPEATED = 0


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
        pos_list.extend([(x_new, y_new) for x_new, y_new in neighborhood if new_heights[x_new][y_new] == 0])

    return new_heights


def figure_name(heights, shape, specify_layers=False):
    """
    Creates figure filename given its column heights and shape
    :param heights: [x_len, y_len] matrix, each value specifying the number of cubes in a column
    :param shape: (x_len, y_len, z_len) tuple
    :param specify_layers: true if layers will be specified, false otherwise
    :return: filename of figure
    """
    x_len, y_len, z_len = shape
    name = f"fig_{x_len}_{y_len}_{z_len}"

    for row in heights:
        hex_row = [str(hex(elem))[-1] for elem in row]
        name += '_' + ''.join(hex_row)

    if specify_layers:
        name += '_l'

    return name + ".png"


def create_random_figure(args):
    """
    Creates a random figure given input values such as dimension lengths or color palettes
    :param args: input values
    """
    global REPEATED

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
    if random.random() < args.prob_layers:
        specify_layers = True
    else:
        specify_layers = False

    filename = figure_name(heights, shape, specify_layers)
    figure_path = os.path.join(args.output_path, filename)

    if os.path.exists(figure_path) or heights.sum() == 0:
        if REPEATED < args.max_repeats:
            REPEATED += 1
            create_random_figure(args)
    else:

        # D) Create voxels and rearrange them to create the picture
        voxels = []
        for i in range(z_len):
            layer = np.array([[True if elem > i else False for elem in heights[x]] for x in range(x_len)])
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
            str_rgb = '#{:02x}{:02x}{:02x}'.format(int(r * 255), int(g * 255), int(b * 255))
            colors[i][voxels[i]] = str_rgb

        # Swap axes to visualize better
        voxels = np.swapaxes(voxels, 0, 2)
        colors = np.swapaxes(colors, 0, 2)

        # F) Create and save plot
        dpi = 96
        fig = plt.figure(figsize=(600/dpi, 400/dpi), dpi=dpi)

        ax = fig.gca(projection='3d')
        ax.set(xlim=(0, y_len), ylim=(0, x_len), zlim=(0, z_len))  # Little trick to plot cubes correctly

        ax.set_xticks(np.arange(0, x_len, 1))
        ax.set_yticks(np.arange(0, y_len, 1))

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # Define z_ticks
        if specify_layers:
            layer = 1
            z_labels = []
            placeholder_labels = [str(item) for item in ax.get_zticklabels()]
            for i, elem in enumerate(placeholder_labels):
                if i % (len(placeholder_labels) // z_len) == (len(placeholder_labels) // z_len) // 2:
                    z_labels.append(f"{layer}. Geruza")
                    layer += 1
                else:
                    z_labels.append("")
            ax.set_zticks(np.arange(0, z_len, 0.5))
            ax.set_zticklabels(z_labels)
            ax.get_zaxis().set_tick_params(direction='out', pad=9)
        else:
            ax.set_zticks(np.arange(0, z_len, 1))
            ax.set_zticklabels([])

        ax.view_init(35, -125)
        ax.voxels(voxels, facecolors=colors, edgecolor='k')
        ax.set(xlim=(0, y_len), ylim=(0, x_len), zlim=(0, z_len))

        # plt.show()
        fig.tight_layout()
        plt.savefig(os.path.join(args.output_path, filename), bbox_inches='tight')
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
        default=100,
        help="Number of created pictures.",
    )
    parser.add_argument(
        "--prob",
        type=float,
        default=0.75,
        help="Probability to stack a cube on top of another. Value between 0 and 1 (not inclusive).",
    )
    parser.add_argument(
        "--prob_layers",
        type=float,
        default=0.25,
        help="Probability to specify layers in figures (0.25 by default). "
             "Will be set to 0 if z_len is higher than 4.",
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
        default='./figurak',
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

    if args.z_len < 2 or args.z_len > 4:
        args.prob_layers = 0.0
        print("WARNING: Layers will not be listed if z_len is not between 2 and 4.")
    elif args.prob_layers < 0.0 or args.prob_layers > 1.0:
        args.prob_layers = 0.25
        print("WARNING: Probability of specifying layers should be between 0.0 and 1.0 (inclusive). Default: 0.25.")

    return args


def main():

    args = parse_arguments()
    args = check_args(args)

    for _ in trange(args.n, desc="Images"):
        create_random_figure(args)


if __name__ == '__main__':

    main()
