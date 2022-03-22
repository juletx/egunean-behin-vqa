"""This module generate figure images"""
import random
import argparse
from PIL import Image, ImageDraw
import numpy as np


def draw_figure(draw, figure, color, x, y, r):
    """Draw a figure with given color, position and radius.

    Args:
        draw (ImageDraw): ImageDraw object.
        figure (str): figure name.
        color (str): color name.
        x (int): x position.
        y (int): y position.
        r (int): radius.
    """
    if figure == 'triangle':
        draw.polygon([(x-r, y+r), (x+r, y+r), (x, y-r)], fill=color)
    if figure == 'square':
        draw.rectangle([x-r, y-r, x+r, y+r], fill=color)
    if figure == 'circle':
        draw.ellipse((x-r, y-r, x+r, y+r), fill=color)


def figure_name(figure_matrix, x_len, y_len):
    """
    Creates figure filename given its column heights and shape

    Args:
        figure_matrix (numpy.ndarray): matrix of figures.
        x_len (int): number of figures in axis X.
        y_len (int): number of figures in axis Y.
    
    Returns:
        str: figure name.
    """
    name = f"fig_{x_len}_{y_len}"

    for row in figure_matrix:
        row_str = [str(elem) for elem in row]
        name += '_' + ''.join(row_str)

    return name + ".png"


def create_image(output_path, x_len, y_len, r):
    """Create an image of figures with given parameters.

    Args:
        output_path (str): path for output files.
        x_len (int): number of figures in axis X.
        y_len (int): number of figures in axis Y.
        r (int): radius of figures.
    """
    figures = ['triangle', 'square', 'circle']
    colors = ['red', 'green', 'blue']

    canvas = (600, 400)
    scale = 1
    thumb = canvas[0]/scale, canvas[1]/scale
    image = Image.new('RGBA', canvas, (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 0 red triangle, 1 green triangle, 2 blue triangle
    # 3 red square, 4 green square, 5 blue square
    # 6 red circle, 7 green circle, 8 blue circle
    figure_matrix = np.zeros((y_len, x_len), dtype=int)

    x_step = thumb[0]/(x_len+1)
    y_step = thumb[1]/(y_len+1)

    for y1 in range(1, y_len + 1):
        for x1 in range(1, x_len + 1):
            x = x1 * x_step
            y = y1 * y_step
            figure = random.randint(0, 2)
            color = random.randint(0, 2)
            draw_figure(draw, figures[figure], colors[color], x, y, r)
            figure_matrix[y1-1][x1-1] = figure * 3 + color

    image.thumbnail(thumb)
    fig_name = figure_name(figure_matrix, x_len, y_len)
    image.save(f"{output_path}/{fig_name}")


def parse_arguments():
    """Parse command line arguments.

    Returns:
        args: parsed arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--x_len",
        type=int,
        default=6,
        help="Number of figures in axis X.",
    )

    parser.add_argument(
        "--y_len",
        type=int,
        default=4,
        help="Number of figures in axis Y.",
    )

    parser.add_argument(
        "--r",
        type=int,
        default=32,
        help="Radius of figures.",
    )

    parser.add_argument(
        "--n",
        type=int,
        default=1,
        help="Number of images created.",
    )

    parser.add_argument(
        "--output_path",
        type=str,
        default='images',
        help="Path for output files.",
    )

    return parser.parse_args()


def main():
    """Main function."""
    args = parse_arguments()
    for _ in range(args.n):
        create_image(args.output_path, args.x_len, args.y_len, args.r)


if __name__ == '__main__':
    main()
