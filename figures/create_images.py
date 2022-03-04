"""This module generate figure images"""
import random
import argparse
from PIL import Image, ImageDraw

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


def create_image(output_path, x_len, y_len):
    """Create an image of figures with given parameters.

    Args:
        output_path (str): path for output files.
        x_len (int): number of figures in axis X.
        y_len (int): number of figures in axis Y.
    """
    figures = ['triangle', 'square', 'circle']
    colors = ['red', 'green', 'blue']

    canvas = (600, 400)
    r = 32
    scale = 2
    thumb = canvas[0]/scale, canvas[1]/scale
    image = Image.new('RGBA', canvas, (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    # 0 triangle, 1 square, 2 circle
    # 0 red, 1 green, 2 blue
    c = {'00': 0, '01': 0, '02': 0, '10': 0,
         '11': 0, '12': 0, '20': 0, '21': 0, '22': 0}

    x_step = thumb[0]/(x_len+1)
    y_step = thumb[1]/(y_len+1)

    for y1 in range(1, y_len + 1):
        for x1 in range(1, x_len + 1):
            x = x1 * x_step
            y = y1 * y_step
            figure = random.randint(0, 2)
            color = random.randint(0, 2)
            draw_figure(draw, figures[figure], colors[color], x, y, r)
            c[str(figure)+str(color)] += 1

    image.thumbnail(thumb)
    filename = f"{output_path}/fig_{c['00']}_{c['01']}_{c['02']}_{c['10']}_{c['11']}_{c['12']}_{c['20']}_{c['21']}_{c['22']}.png"
    image.save(filename)


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
        "--n",
        type=int,
        default=5,
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
        create_image(args.output_path, args.x_len, args.y_len)


if __name__ == '__main__':
    main()
