"""This module creates maze images"""
import os
import random
import argparse
from cairosvg import svg2png
from tqdm import tqdm

# Create a maze using the depth-first algorithm described at
# https://scipython.com/blog/making-a-maze/
# Christian Hill, April 2017.


class Cell:
    """A cell in the maze.

    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.

    """

    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self):
        """Does this cell still have all its walls?"""

        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """Knock down the wall between cells self and other."""

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False

    def build_wall(self, other, wall):
        """Build the wall between cells self and other."""

        self.walls[wall] = True
        other.walls[Cell.wall_pairs[wall]] = True


class Maze:
    """A Maze, represented as a grid of cells."""

    def __init__(self, nx, ny, ix=0, iy=0):
        """Initialize the maze grid.
        The maze consists of nx x ny cells and will be constructed starting
        at the cell indexed at (ix, iy).

        """

        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def cell_at(self, x, y):
        """Return the Cell object at (x,y)."""

        return self.maze_map[x][y]

    def __str__(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['-' * self.nx*2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def write_svg(self, filename):
        """Write an SVG image of the maze to filename."""

        aspect_ratio = self.nx / self.ny
        # Pad the maze all around by this amount.
        padding = 0
        # Height and width of the maze image (excluding padding), in pixels
        height = 400
        width = int(height * aspect_ratio)
        height_pad = height + 2 * padding
        width_pad = width + 2 * padding
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ny, width / self.nx

        # Write the SVG image file for maze
        with open(filename, 'w', encoding='UTF-8') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('	xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print(f'	width="{width_pad}" height="{height_pad}" viewBox="{-padding} {-padding} {width_pad} {height_pad}">', file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('	stroke: #000000;\n	stroke-linecap: square;', file=f)
            print('	stroke-width: 5;\n}', file=f)
            print(']]></style>\n</defs>', file=f)
            # Draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).
            for x in range(self.nx):
                for y in range(self.ny):
                    if self.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x*scx, (y+1)*scy, (x+1)*scx, (y+1)*scy
                        print(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>', file=f)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x+1)*scx, y*scy, (x+1)*scx, (y+1)*scy
                        print(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>', file=f)
            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            print(f'<line x1="0" y1="0" x2="{width}" y2="0"/>', file=f)
            print(f'<line x1="0" y1="0" x2="0" y2="{height}"/>', file=f)
            print(
                '<circle cx="25" cy="25" r="15" stroke="black" stroke-width="3" fill="green" />', file=f)
            print(
                '<circle cx="575" cy="25" r="15" stroke="black" stroke-width="3" fill="blue" />', file=f)
            print(
                '<circle cx="25" cy="375" r="15" stroke="black" stroke-width="3" fill="red" />', file=f)
            print(
                '<circle cx="575" cy="375" r="15" stroke="black" stroke-width="3" fill="yellow" />', file=f)
            print('</svg>', file=f)

    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        """Build a maze using the Depth-First-Search algorithm."""
        # Total number of cells.
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1

    def check_road(self, start):
        """Check if the maze has a valid road from start to finish.

        Args:
            start (array(int)): The start cell of the road.

        Returns:
            int: The end point of the road, or 0 if no road is found.
        """
        exits = [[0, self.ny-1], [self.nx-1, 0], [self.nx-1, self.ny-1]]
        x, y = start[0], start[1]
        road = []
        nor = ["N", "S", "E", "W"]
        rotate = {'W': "S",
                  'S': "E",
                  'E': "N",
                  'N': "W"}
        antirotate = {'W': "N",
                      'S': "W",
                      'E': "S",
                      'N': "E"}
        delta = {'W': [-1, 0],
                 'E': [1, 0],
                 'S': [0, 1],
                 'N': [0, -1]}

        #print(self.cell_at(x, y).walls["S"])
        #print(self.cell_at(x, y).walls["N"])
        #print(self.cell_at(x, y).walls["W"])
        #print(self.cell_at(x, y).walls["E"])
        nora = 0
        for n in nor:
            if not self.cell_at(x, y).walls[n]:
                nora = n
                x += delta[nora][0]
                y += delta[nora][1]
                #print(f"Lenengoa {x},{y}")
                break
        i = 0
        while [x, y] != [0, 0] and i < 100000:
            if not self.cell_at(x, y).walls[nora]:  # if paretarik ez
                #print(f"{x} {y} {nora}")
                # if [x,y,nora] not in road: #if cell horretatik norazko hori hartu gabe
                road.append([x, y, nora])
                x += delta[nora][0]
                y += delta[nora][1]
                nora = rotate[nora]
            else:
                nora = antirotate[nora]
            i += 1
        # print(road)
        results = [0, 0, 0]
        for cell in road:
            for i, ex in enumerate(exits):
                if [cell[0], cell[1]] == ex:
                    results[i] += 1
        # print(results)
        if results.count(0) == 2:
            # print(results)
            if 0 < results[0] < 3:
                return 1
            elif 0 < results[1] < 3:
                return 2
            elif 0 < results[2] < 3:
                return 3
        else:
            return 0

    def close_road(self):
        """Close the road by adding a random wall so that there is only one option."""
        end = 0
        k = 0
        while not end:
            if k == 4:
                end = 1
                # print("oker")
                return (self, 0)
            rx = random.randint(0, self.nx-1)
            ry = random.randint(0, self.ny-1)
            cell = self.cell_at(rx, ry)
            nora = random.choice(["N", "S", "E", "W"])
            if not cell.walls[nora]:
                cell.walls[nora] = True  # horma bat sortu
                road = self.check_road([0, 0])
                if road:  # Zuzena bada, sortu galdera... 0,0 = Beti berdetik hasi
                    end = 1
                    # print("Zuzen")
                    return (self, road)
                k += 1


def create_image(output_path, i, nx, ny, start):
    """Create an image of the maze.

    Args:
        output_path (str): path for the output images.
        i (int): index of the maze.
        nx (int): number of cells in axis x.
        ny (int): number of cells in axis y.
        start (int): start position.
    """
    if start == 0:
        ix, iy = 0, 0
    elif start == 1:
        ix, iy = nx-1, 0
    elif start == 2:
        ix, iy = 0, ny-1
    elif start == 3:
        ix, iy = nx-1, ny-1

    end = start
    while end == start:
        maze = Maze(nx, ny, ix, iy)
        maze.make_maze()
        maze, end = maze.close_road()

    mazename = f"{output_path}\\maze_{i}_{nx}_{ny}_{start}_{end}.svg"
    mazename_png = f"{output_path}\\maze_{i}_{nx}_{ny}_{start}_{end}.png"
    maze.write_svg(mazename)
    svg2png(url=mazename, write_to=mazename_png)
    os.remove(mazename)


def parse_arguments():
    """Parse command line arguments.

    Returns:
        args: parsed arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--nx",
        type=int,
        default=12,
        help="Number of figures in axis X.",
    )

    parser.add_argument(
        "--ny",
        type=int,
        default=8,
        help="Number of figures in axis Y.",
    )

    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="Number of figures in axis Y.",
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
    for i in tqdm(range(args.n), total=args.n, desc="Images"):
        create_image(args.output_path, i, args.nx, args.ny, args.start)


if __name__ == '__main__':
    main()
