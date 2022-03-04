"""This module generates questions for images."""
import argparse
import os
import csv
import random


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
    answers.append(random.choice([i for i in range(1, 10) if i not in answers]))
    answers.append(random.choice([i for i in range(1, 10) if i not in answers]))
    return answers[1:]


def create_questions(image_path):
    """Create questions for each image in the images_path directory.

    15 questions are created for each image. 3 questions about figure shape.
    3 questions about figure color. 9 questions about figure shape and color.

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

    for image in images:
        counts = list(map(int, image.split('.')[0].split('_')[1:]))

        for i, figure in enumerate(figures):
            question = f"How many {figure}s?"
            correct = sum(counts[i * 3:(i+1) * 3])
            wrong = wrong_answers(correct)
            questions.append([category, question, correct,
                              wrong[0], wrong[1], image])

        for i, color in enumerate(colors):
            question = f"How many {color} figures?"
            correct = counts[i] + counts[i + 3] + counts[i + 6]
            wrong = wrong_answers(correct)
            questions.append([category, question, correct,
                              wrong[0], wrong[1], image])

        for i, figure in enumerate(figures):
            for j, color in enumerate(colors):
                question = f"How many {color} {figure}s?"
                correct = counts[i * 3 + j]
                wrong = wrong_answers(correct)
                questions.append(
                    [category, question, correct, wrong[0], wrong[1], image])

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
