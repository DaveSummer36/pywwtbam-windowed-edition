import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from stream import QuestionManager

MAX_QUESTIONS = 20  # The maximum number of questions in the game


class PyWWTBAM:

    def __init__(self, root):
        self.root = root
        self.root.title("PyWWTBAM GUI Edition v1.0")
        self.q_manager = QuestionManager()
        self.root.iconbitmap("multi.ico")
        self.current_question_number = 1
        self.pack_number = 1
        self.current_question = None
        self.safety_net_prize = 0  # Initial safety net prize
        self.window_width = 800
        self.window_height = 600

        # Load the first background image
        self.background_images = [
            "back_easy.png",   # Easy Tier background
            "back_mid.png",    # Mid-Tier background
            "back_hard.png",   # Hard Tier background
            "back_final.png",  # Final Tier background
        ]
        self.background_image = None
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.pack(fill="both", expand=True)

        # Create a frame to hold the question number, current prize and safety net prize side by side
        self.info_frame = tk.Frame(self.root, bg="black")
        self.question_num_label = tk.Label(self.info_frame, text=f"Question {self.current_question_number}", font=("Arial", 12), bg="black", fg="white")
        self.prize_label = tk.Label(self.info_frame, text="Current Prize: 0", font=("Arial", 12), bg="black", fg="white")
        self.safety_net_label = tk.Label(self.info_frame, text="Safety Net: 0", font=("Arial", 12), bg="black", fg="white")

        # Question text display
        self.question_label = tk.Label(self.root, text="", wraplength=400, font=("Arial", 14), bg="black", fg="white")

        # Radio buttons for answers
        self.answer_var = tk.StringVar()
        self.radio_a = tk.Radiobutton(self.root, text="", variable=self.answer_var, value="A", bg="black", fg="white")
        self.radio_b = tk.Radiobutton(self.root, text="", variable=self.answer_var, value="B", bg="black", fg="white")
        self.radio_c = tk.Radiobutton(self.root, text="", variable=self.answer_var, value="C", bg="black", fg="white")
        self.radio_d = tk.Radiobutton(self.root, text="", variable=self.answer_var, value="D", bg="black", fg="white")

        # Final answer button
        self.final_button = tk.Button(self.root, text="Final Answer", command=self.final_answer)

        # Bind the keyboard events for 'a', 'b', 'c', 'd' and 'Enter'
        self.root.bind('<a>', lambda events: self.select_option('A'))
        self.root.bind('<b>', lambda events: self.select_option('B'))
        self.root.bind('<c>', lambda events: self.select_option('C'))
        self.root.bind('<d>', lambda events: self.select_option('D'))
        self.root.bind('<Return>', lambda events: self.final_answer())

        # Load the first question
        self.load_next_pack()

    def load_background_image(self):
        """Load and display the appropriate background image based on the question number."""
        if self.current_question_number <= 5:
            img_path = self.background_images[0]
        elif self.current_question_number <= 10:
            img_path = self.background_images[1]
        elif self.current_question_number <= 15:
            img_path = self.background_images[2]
        else:
            img_path = self.background_images[3]

        self.background_image = PhotoImage(file=img_path)
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        # Add widgets on top of the background image
        self.info_frame.place(x=50, y=20)
        self.question_num_label.pack(side="left", padx=10)
        self.prize_label.pack(side="left", padx=10)
        self.safety_net_label.pack(side="left", padx=10)
        self.question_label.place(x=50, y=100)
        self.radio_a.place(x=50, y=200)
        self.radio_b.place(x=50, y=250)
        self.radio_c.place(x=50, y=300)
        self.radio_d.place(x=50, y=350)
        self.final_button.place(x=50, y=450)

    def load_next_pack(self):
        """Load the next question pack and display a random question."""
        if self.current_question_number > MAX_QUESTIONS:
            messagebox.showinfo("Congratulations!", "You've answered all questions correctly!")
            self.root.quit()
            return

        # Update the background image
        self.load_background_image()

        self.q_manager.clearQuestions()
        filename = f"src/questions/q{self.pack_number}.txt"
        self.q_manager.loadQuestions(filename)

        self.current_question = self.q_manager.getRandomQuestion()
        if self.current_question:
            self.display_question()
        else:
            messagebox.showerror("Error", f"No questions available in pack {self.pack_number}.")
            self.root.quit()

    def display_question(self):
        """Display the current question, prize and update the display."""
        self.answer_var.set(str(None))  # Reset answer selection

        # Update the question label
        self.question_label.config(text=self.current_question.questionText)

        # Update the radio buttons with the answer options
        self.radio_a.config(text=f"A: {self.current_question.answerA}")
        self.radio_b.config(text=f"B: {self.current_question.answerB}")
        self.radio_c.config(text=f"C: {self.current_question.answerC}")
        self.radio_d.config(text=f"D: {self.current_question.answerD}")

        # Update the current prize and question number labels
        self.prize_label.config(text=f"Current Prize: {self.current_question.questionPrize}")
        self.question_num_label.config(text=f"Question {self.current_question_number}")

    def select_option(self, option):
        """Set the selected option based on keyboard input (a, b, c, d)."""
        self.answer_var.set(option)

    def final_answer(self):
        """Check the answer and load the next question if correct, or end the game if wrong."""
        selected_answer = self.answer_var.get()

        if selected_answer == "":
            messagebox.showwarning("Warning", "Please select an answer!")
            return

        if self.current_question.is_correct(selected_answer):
            messagebox.showinfo("Correct", "That's the correct answer!")
            # Check if it's Q5, Q10, Q15 and set the safety net if correct
            if self.current_question_number % 5 == 0:  # Q5, Q10, Q15
                self.safety_net_prize = self.current_question.questionPrize
                self.safety_net_label.config(text=f"Safety Net: {self.safety_net_prize}")

            # Proceed to the next question
            self.current_question_number += 1
            self.pack_number += 1
            self.load_next_pack()
        else:
            messagebox.showerror("Wrong", f"The correct answer was {self.current_question.correctAnswer}.")
            self.end_game()

    def end_game(self):
        """End the game and show the final prize based on the safety net."""
        final_prize = self.safety_net_prize
        messagebox.showinfo("Game over", f"Game over! Total winnings: {final_prize}.")
        self.root.quit()


def main():
    root = tk.Tk()
    app = PyWWTBAM(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# TODO!!!: Resize background pictures!!!! - Done!!!