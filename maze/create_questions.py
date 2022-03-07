"""This module creates questions for maze images."""
import csv
import argparse
import os
import random


def parse_filename(filename):
    """Parse image filename to get figures matrix and lengths.

    Args:
        filename (str): name of the image file

    Returns:
        nx, ny: maze dimensions
        start: maze entry position
        send: maze exit position
    """
    name = filename.split('.')[0]
    values = name.split('_')[1:]
    nx, ny = int(values[1]), int(values[2])
    start, end = int(values[3]), int(values[4])

    return nx, ny, start, end


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


def create_questions(image_path):
    """Create questions for each image in the images_path directory.

    Args:
        image_path (str): path to the directory with images.

    Returns:
        list: list of questions.
    """
    category = "Maze"
    images = os.listdir(image_path)
    questions = []

    for image in images:
        nx, ny, start, end = parse_filename(image)

        question = "How many cells?"
        correct = nx * ny
        wrong1, wrong2 = wrong_answers(correct)
        questions.append([category, question, correct,
                          wrong1, wrong2, image])

        question = "How many colums?"
        correct = nx
        wrong1, wrong2 = wrong_answers(correct)
        questions.append([category, question, correct,
                          wrong1, wrong2, image])

        question = "How many rows?"
        correct = ny
        wrong1, wrong2 = wrong_answers(correct)
        questions.append([category, question, correct,
                          wrong1, wrong2, image])

        question = "Which is the exit starting from green?"
        if end == 1:
            correct, wrong1, wrong2 = "red", "yellow", "blue"
        elif end == 2:
            correct, wrong1, wrong2 = "blue", "red", "yellow"
        elif end == 3:
            correct, wrong1, wrong2 = "yellow", "red", "blue"
        questions.append([category, question, correct,
                          wrong1, wrong2, image])

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
