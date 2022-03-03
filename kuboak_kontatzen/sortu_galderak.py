import argparse
import os
import random
import csv
import numpy as np
from tqdm import tqdm

# Global variables
TYPE = "Kuboak Kontatzen"
QUESTIONS = [
    "Zenbat kubo daude guztira? (Ikusgai ez daudenak barne)",   # ID: 0
    "Zenbat kubo daude ikusgai?",                               # ID: 1
    "Zenbat kubo EZ daude ikusgai?",                            # ID: 2
    "Zenbat kubo daude %s. geruzan?",                           # ID: 3 (only if layers are specified)
]


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
                value += max([heights[cur_x][cur_y] - min(neighborhood), int(heights[cur_x][cur_y] > 0)])
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

    # COMPUTE VALID ANSWER
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
        correct_answer = int((heights >= layer).sum())
        incorrect_answer_variation = round((x_len * y_len) ** 0.5)
    else:
        raise ValueError(f"ERROR: Question type {question_type} not defined!")  # Shouldn't reach here

    if incorrect_answer_variation < 2:
        incorrect_answer_variation = 2

    # COMPUTE INCORRECT ANSWERS
    # Choose if the incorrect answer will be both higher, both lower or one higher and another lower
    incorrect_answers = []
    answer_position = random.choice(["lower", "middle", "higher"])

    # Ensure that all answers are positive or zero
    if answer_position == "lower":
        while len(incorrect_answers) < 2:
            if correct_answer == 0:
                sample = random.randint(correct_answer + 1, correct_answer + incorrect_answer_variation)
                while sample in incorrect_answers:
                    sample = random.randint(correct_answer + 1, correct_answer + incorrect_answer_variation)
                incorrect_answers.append(sample)
            if correct_answer == 1:
                incorrect_answers.append([0, 2])
            else:
                sample = random.randint(max([(correct_answer - incorrect_answer_variation), 0]), correct_answer - 1)
                while sample in incorrect_answers:
                    sample = random.randint(max([(correct_answer - incorrect_answer_variation), 0]), correct_answer - 1)
                incorrect_answers.append(sample)
    elif answer_position == "middle":
        sample = random.randint(max([(correct_answer - incorrect_answer_variation), 0]), correct_answer - 1)
        incorrect_answers.append(sample)
        sample = random.randint(correct_answer + 1, correct_answer + incorrect_answer_variation)
        incorrect_answers.append(sample)
    else:
        while len(incorrect_answers) < 2:
            sample = random.randint(correct_answer + 1, correct_answer + incorrect_answer_variation)
            while sample in incorrect_answers:
                sample = random.randint(correct_answer + 1, correct_answer + incorrect_answer_variation)
            incorrect_answers.append(sample)

    return int(correct_answer), int(incorrect_answers[0]), int(incorrect_answers[1])


def create_questions(path, q_type):
    """
    Creates question(s) for a list of figures in a given path
    :param path: directory of the figures
    :param q_type: specifies which question types are going to be created
    :return: list of question, answers and figure filename (5 values)
    """
    question_list = []
    question_type = 0
    list_of_images = [file for file in os.listdir(path) if '.png' in file]
    n = len(list_of_images)

    if q_type != "random" and q_type != "all":
        question_type = int(q_type)

    for file in tqdm(list_of_images, desc='Questions', total=n):

        heights, shape = parse_filename(file)
        x_len, y_len, z_len = shape

        if "_l.png" in file:  # if layers are specified in this file

            if q_type != "all":

                layer = random.randint(1, z_len)
                question = QUESTIONS[3] % layer
                correct_answer, incorrect_answer_1, incorrect_answer_2 = create_answers(heights, shape, 3, layer)

                question_list.append([TYPE, question, correct_answer, incorrect_answer_1, incorrect_answer_2, file])

            else:  # q_type == "all"

                for layer in range(1, z_len + 1):
                    question = QUESTIONS[3] % layer
                    correct_answer, incorrect_answer_1, incorrect_answer_2 = create_answers(heights, shape, 3, layer)

                    question_list.append([TYPE, question, correct_answer, incorrect_answer_1, incorrect_answer_2, file])

        else:  # if layers are NOT specified in this file

            if q_type != "all":

                if q_type == "random":
                    question_type = random.randint(0, 2)

                question = QUESTIONS[question_type]
                correct_answer, incorrect_answer_1, incorrect_answer_2 = create_answers(heights, shape, question_type)

                question_list.append([TYPE, question, correct_answer, incorrect_answer_1, incorrect_answer_2, file])

            else:  # q_type == "all"

                for question_type in range(len(QUESTIONS) - 1):

                    question = QUESTIONS[question_type]
                    correct_answer, incorrect_answer_1, incorrect_answer_2 = create_answers(heights, shape,
                                                                                            question_type)

                    question_list.append([TYPE, question, correct_answer, incorrect_answer_1, incorrect_answer_2, file])

    return question_list


def write_questions(question_list, filename):
    """
    Saves questions in a file
    :param question_list: question list to be saved
    :param filename: name of the output filename
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Mota', 'Galdera', 'Erantzun zuzena', 'Erantzun okerra 1', 'Erantzun okerra 2', 'Fitxategia'])
        for q in question_list:
            writer.writerow(q)


def parse_arguments():
    """
    Parse input values
    :return: input values
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--type",
        type=str,
        default="all",
        choices=["all", "random", "0", "1", "2"],
        help="Type of generated questions for figures with no layer listed in image."
    )
    parser.add_argument(
        "--image_path",
        type=str,
        default='./figurak',
        help="Path for input images.",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default='galderak.csv',
        help="Path for output file.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    question_list = create_questions(args.image_path, args.type)
    write_questions(question_list, args.filename)


if __name__ == '__main__':
    main()
