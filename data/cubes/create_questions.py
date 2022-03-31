"""This module is used to generate questions for cube figures."""
import argparse
import os
import random
import csv
import numpy as np
from tqdm import tqdm


def parse_filename(filename):
    """
    Create heights matrix and shape tuple given its filename
    :param filename: filename of the figure
    :return: heights and shape of figure
    """
    name = filename[:-4]
    values = name.split('_')
    x_len, y_len, z_len = int(values[1]), int(values[2]), int(values[3])

    heights = np.zeros((x_len, y_len), dtype=int)
    shape = (x_len, y_len, z_len)

    for x in range(x_len):
        for y in range(y_len):
            heights[x][y] = int(values[x + 4][y])

    return heights, shape


def visible_cubes(heights, x_len, y_len):
    """
    Computes how many cubes are visible from our perspective
    :param heights: [x_len, y_len] matrix, each value specifying the number of cubes in a column
    :param x_len: number of rows
    :param y_len: number of columns
    :return: number of visible cubes
    """
    value = 0

    for cur_x in range(x_len):
        for cur_y in range(y_len):

            neighborhood = []
            if cur_x > 0:
                neighborhood.append(heights[cur_x - 1][cur_y])
            else:
                neighborhood.append(0)
            if cur_y > 0:
                neighborhood.append(heights[cur_x][cur_y - 1])
            else:
                neighborhood.append(0)

            if len(neighborhood) > 0:
                value += max([heights[cur_x][cur_y] -
                              min(neighborhood), int(heights[cur_x][cur_y] > 0)])
            else:
                value += heights[cur_x][cur_y]

    return value


def wrong_answers(correct):
    """Create wrong answers for a given correct answer.

    Args:
        correct (int): correct answer.

    Returns:
        list: list of wrong answers.
    """
    answers = [correct]
    wrong_var = round((correct) ** 0.5)
    wrong_var = max(wrong_var, 2)
    while len(answers) < 3:
        wrong = random.randint(
            max(correct - wrong_var, 0), correct + wrong_var)
        if wrong not in answers:
            answers.append(wrong)
    return answers[1], answers[2]


def create_questions(path):
    """
    Creates question(s) for a list of figures in a given path
    :param path: directory of the figures
    :param q_type: specifies which question types are going to be created
    :return: list of question, answers and figure filename (5 values)
    """
    question_list = []
    list_of_images = [file for file in os.listdir(path) if '.png' in file]
    n = len(list_of_images)

    category = "Cubes"

    for file in tqdm(list_of_images, desc='Questions', total=n):

        heights, shape = parse_filename(file)
        x_len, y_len, z_len = shape

        question = "How many cubes in total?"
        correct = int(heights.sum())
        wrong1, wrong2 = wrong_answers(correct)
        question_list.append(
            [category, question, correct, wrong1, wrong2, file])

        question = "How many visible cubes?"
        correct = visible_cubes(heights, x_len, y_len)
        wrong1, wrong2 = wrong_answers(correct)
        question_list.append(
            [category, question, correct, wrong1, wrong2, file])

        question = "How many non visible cubes?"
        correct =  int(heights.sum()) - visible_cubes(heights, x_len, y_len)
        wrong1, wrong2 = wrong_answers(correct)
        question_list.append(
            [category, question, correct, wrong1, wrong2, file])

        for x in range(1, x_len + 1):
            question = f"How many cubes in layer x {x}?"
            correct = int((heights[x - 1, :]).sum())
            wrong1, wrong2 = wrong_answers(correct)
            question_list.append(
                [category, question, correct, wrong1, wrong2, file])

        for y in range(1, y_len + 1):
            question = f"How many cubes in layer y {y}?"
            correct = int((heights[:, y - 1]).sum())
            wrong1, wrong2 = wrong_answers(correct)
            question_list.append(
                [category, question, correct, wrong1, wrong2, file])

        for z in range(1, z_len + 1):
            question = f"How many cubes in layer z {z}?"
            correct = int((heights >= z).sum())
            wrong1, wrong2 = wrong_answers(correct)
            question_list.append(
                [category, question, correct, wrong1, wrong2, file])

    return question_list


def write_questions(question_list, filename):
    """
    Saves questions in a file
    :param question_list: question list to be saved
    :param filename: name of the output filename
    """
    with open(filename, 'w', encoding='UTF-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['type', 'question', 'correct',
                         'wrong1', 'wrong2', 'image'])
        for question in question_list:
            writer.writerow(question)


def parse_arguments():
    """
    Parse input values
    :return: input values
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--image_path",
        type=str,
        default='images',
        help="Path for input images.",
    )

    parser.add_argument(
        "--filename",
        type=str,
        default='questions.csv',
        help="Path for output file.",
    )

    return parser.parse_args()


def main():
    """Main function"""
    args = parse_arguments()
    question_list = create_questions(args.image_path)
    write_questions(question_list, args.filename)


if __name__ == '__main__':
    main()
