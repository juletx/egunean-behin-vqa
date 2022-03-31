"""This module generates questions for images."""
import argparse
from collections import defaultdict
import os
import csv
import random
import numpy as np
from tqdm import tqdm


def write_questions(questions, filename):
    """Write questions to a csv file.

    Args:
        questions (list): list of questions.
        filename (str): path to the output file.
    """
    with open(filename, 'w', encoding='UTF-8', newline="") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['type', 'question', 'correct',
                             'wrong1', 'wrong2', 'image'])
        for question in questions:
            spamwriter.writerow(question)


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


def parse_filename(filename):
    """Parse image filename to get figures matrix and lengths.

    Args:
        filename (str): name of the image file

    Returns:
        figure_matrix: np.ndarray of figures
        x_len: length of the x axis
        y_len: length of the y axis
    """
    name = filename.split('.')[0]
    values = name.split('_')[1:]
    x_len, y_len = int(values[0]), int(values[1])

    figure_matrix = np.zeros((y_len, x_len), dtype=int)

    for x in range(x_len):
        for y in range(y_len):
            figure_matrix[y][x] = int(values[y + 2][x])

    return figure_matrix, x_len, y_len


def create_questions(image_path):
    """Create questions for each image in the images_path directory.

    18 questions are created for each image. 3 questions about figure, column and row count.
    3 questions about figure shape. 3 questions about figure color. 
    9 questions about figure shape and color.

    Args:
        image_path (str): path to the directory with images.

    Returns:
        list: list of questions.
    """
    figures = ['triangle', 'square', 'circle']
    colors = ['red', 'green', 'blue']
    category = "Figures"
    images = os.listdir(image_path)
    questions = []

    for image in tqdm(images, desc='Questions', total=len(images)):
        figure_matrix, x_len, y_len = parse_filename(image)

        question = "How many figures?"
        correct = x_len * y_len
        wrong1, wrong2 = wrong_answers(correct)
        questions.append([category, question, correct,
                          wrong1, wrong2, image])

        question = "How many columns?"
        correct = x_len
        wrong1, wrong2 = wrong_answers(correct)
        questions.append([category, question, correct,
                          wrong1, wrong2, image])

        question = "How many rows?"
        correct = y_len
        wrong1, wrong2 = wrong_answers(correct)
        questions.append([category, question, correct,
                          wrong1, wrong2, image])

        unique, count = np.unique(figure_matrix, return_counts=True)
        counts = dict(zip(unique, count))
        counts = defaultdict(int, counts)

        for i, figure in enumerate(figures):
            question = f"How many {figure}s?"
            correct = counts[i * 3] + counts[i * 3 + 1] + counts[i * 3 + 2]
            wrong1, wrong2 = wrong_answers(correct)
            questions.append([category, question, correct,
                              wrong1, wrong2, image])

        for i, color in enumerate(colors):
            question = f"How many {color} figures?"
            correct = counts[i] + counts[i + 3] + counts[i + 6]
            wrong1, wrong2 = wrong_answers(correct)
            questions.append([category, question, correct,
                              wrong1, wrong2, image])

        for i, figure in enumerate(figures):
            for j, color in enumerate(colors):
                question = f"How many {color} {figure}s?"
                correct = counts[i * 3 + j]
                wrong1, wrong2 = wrong_answers(correct)
                questions.append(
                    [category, question, correct, wrong1, wrong2, image])

    return questions


def parse_arguments():
    """Parse command line arguments image_path and filename.

    Returns:
        args: parsed arguments.
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
    """Main function."""
    args = parse_arguments()
    questions = create_questions(args.image_path)
    write_questions(questions, args.filename)


if __name__ == '__main__':
    main()
