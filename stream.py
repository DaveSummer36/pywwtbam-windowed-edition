import random
from pathlib import Path


class Question:

    def __init__(self, num, text, a, b, c, d, correct, prize):
        self.questionNumber = num
        self.questionText = text
        self.answerA = a
        self.answerB = b
        self.answerC = c
        self.answerD = d
        self.correctAnswer = correct.lower()  # Ensure answers are case-insensitive
        self.questionPrize = prize

    def display(self):
        """Display the question and answers."""
        print(f"Question: {self.questionNumber} - ${self.questionPrize}:\n")
        print(f"{self.questionText}")
        print(f"A: {self.answerA}")
        print(f"B: {self.answerB}")
        print(f"C: {self.answerC}")
        print(f"D: {self.answerD}")

    def is_correct(self, answer):
        """Check if the given answer is correct"""
        return answer.lower() == self.correctAnswer


class QuestionManager:

    def __init__(self):
        self.questions = []  # List to hold all questions

    def loadQuestions(self, filename):
        """Load questions from a file."""
        path = Path(filename)

        if not path.exists():
            print(f"Error: {filename} not found.")
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split('|')

                    if len(data) == 8:  # Ensure the line contains valid data
                        # Create a Question object and add it to the list
                        question = Question(
                            num=int(data[0]),
                            text=data[1],
                            a=data[2],
                            b=data[3],
                            c=data[4],
                            d=data[5],
                            correct=data[6],
                            prize=int(data[7])
                        )
                        self.questions.append(question)
                    else:
                        print("Incorrect question format, skipping this line.")
        except Exception as e:
            print(f"Error processing the file: {e}")

    def getRandomQuestion(self):
        """Return a random question."""
        if not self.questions:
            print("No questions loaded.")
            return None
        return random.choice(self.questions)

    def clearQuestions(self):
        """Clear the current question list when loading a new question pack."""
        self.questions = []
