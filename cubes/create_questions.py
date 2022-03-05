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

    heights = np.zeros((x_len, y_len))
    shape = (x_len, y_len, z_len)

    for x in range(x_len):
        for y in range(y_len):
            heights[x][y] = int(values[x + 4][y], 16)

    return heights, shape


def visible_cubes(heights, shape):
    """
    Computes how many cubes are visible from our perspective
    :param heights: [x_len, y_len] matrix, each value specifying the number of cubes in a column
    :param shape:  (x_len, y_len, z_len) tuple
    :return: number of visible cubes
    """
    x_len, y_len, z_len = shape
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


def create_answers(heights, shape, question_type, layer=0):
    """
    Creates 3 answers for a given question, the first one being the correct one
    :param heights: [x_len, y_len] matrix, each value specifying the number of cubes in a column
    :param shape:  (x_len, y_len, z_len) tuple
    :param question_type: question that needs to be answered (its ID)
    :param layer: if the question specifies a layer, the number of the layer
    :return: correct answer and two incorrect answers (three value tuple)
    """
    x_len, y_len, z_len = shape

    # compute the correct answer
    if question_type == 0:
        correct_answer = int(heights.sum())
        incorrect_answer_variation = round((x_len * y_len * z_len) ** 0.5)
    elif question_type == 1:
        correct_answer = visible_cubes(heights, shape)
        incorrect_answer_variation = round((x_len * y_len * z_len) ** 0.5)
    elif question_type == 2:
        correct_answer = int(heights.sum()) - visible_cubes(heights, shape)
        incorrect_answer_variation = round((x_len * y_len * z_len) ** 0.5)
    elif question_type == 3:
        correct_answer = int((heights[layer - 1, :]).sum())
        incorrect_answer_variation = round((y_len * z_len) ** 0.5)
    elif question_type == 4:
        correct_answer = int((heights[:, layer - 1]).sum())
        incorrect_answer_variation = round((x_len * z_len) ** 0.5)
    elif question_type == 5:
        correct_answer = int((heights >= layer).sum())
        incorrect_answer_variation = round((x_len * y_len) ** 0.5)
    else:
        # Shouldn't reach here
        raise ValueError(f"ERROR: Question type {question_type} not defined!")

    incorrect_answer_variation = max(incorrect_answer_variation, 2)

    # COMPUTE INCORRECT ANSWERS
    # Choose if the incorrect answer will be both higher, both lower or one higher and another lower
    incorrect_answers = []
    answer_position = random.choice(["lower", "middle", "higher"])

    # Ensure that all answers are positive or zero
    if answer_position == "lower":
        while len(incorrect_answers) < 2:
            if correct_answer == 0:
                sample = random.randint(
                    correct_answer + 1, correct_answer + incorrect_answer_variation)
                while sample in incorrect_answers:
                    sample = random.randint(
                        correct_answer + 1, correct_answer + incorrect_answer_variation)
                incorrect_answers.append(sample)
            if correct_answer == 1:
                incorrect_answers.append([0, 2])
            else:
                sample = random.randint(
                    max([(correct_answer - incorrect_answer_variation), 0]), correct_answer - 1)
                while sample in incorrect_answers:
                    sample = random.randint(
                        max([(correct_answer - incorrect_answer_variation), 0]), correct_answer - 1)
                incorrect_answers.append(sample)
    elif answer_position == "middle":
        sample = random.randint(
            max([(correct_answer - incorrect_answer_variation), 0]), correct_answer - 1)
        incorrect_answers.append(sample)
        sample = random.randint(
            correct_answer + 1, correct_answer + incorrect_answer_variation)
        incorrect_answers.append(sample)
    else:
        while len(incorrect_answers) < 2:
            sample = random.randint(
                correct_answer + 1, correct_answer + incorrect_answer_variation)
            while sample in incorrect_answers:
                sample = random.randint(
                    correct_answer + 1, correct_answer + incorrect_answer_variation)
            incorrect_answers.append(sample)

    return int(correct_answer), int(incorrect_answers[0]), int(incorrect_answers[1])


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
    questions = [
        "How many cubes in total?",
        "How many visible cubes?",
        "How many non visible cubes?",
    ]

    for file in tqdm(list_of_images, desc='Questions', total=n):

        heights, shape = parse_filename(file)
        x_len, y_len, z_len = shape

        for q_type, question in enumerate(questions):
            correct_answer, incorrect_answer_1, incorrect_answer_2 = create_answers(heights, shape,
                                                                                    q_type)
            question_list.append(
                [category, question, correct_answer, incorrect_answer_1, incorrect_answer_2, file])

        for x in range(1, x_len + 1):
            question = f"How many cubes in layer x {x}?"
            correct_answer, incorrect_answer_1, incorrect_answer_2 = create_answers(
                heights, shape, 3, x)
            question_list.append(
                [category, question, correct_answer, incorrect_answer_1, incorrect_answer_2, file])

        for y in range(1, y_len + 1):
            question = f"How many cubes in layer y {y}?"
            correct_answer, incorrect_answer_1, incorrect_answer_2 = create_answers(
                heights, shape, 4, y)
            question_list.append(
                [category, question, correct_answer, incorrect_answer_1, incorrect_answer_2, file])

        for z in range(1, z_len + 1):
            question = f"How many cubes in layer z {z}?"
            correct_answer, incorrect_answer_1, incorrect_answer_2 = create_answers(
                heights, shape, 5, z)
            question_list.append(
                [category, question, correct_answer, incorrect_answer_1, incorrect_answer_2, file])

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
