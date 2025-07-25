import tkinter as tk
from tkinter import messagebox
import time

class TypingSpeedApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Typing Speed Calculator")
        self.root.geometry("650x500")

        self.start_time = None

        self.prompt_label = tk.Label(root, text="Enter a sentence for typing test:", font=("Arial", 12,"bold"))
        self.prompt_label.pack(pady=5)

        self.prompt_entry = tk.Entry(root, width=60, font=("Arial", 12))
        self.prompt_entry.pack(pady=5)

        self.set_prompt_btn = tk.Button(root, text="SET PROMPT", command=self.set_prompt, bg="blue", fg="white", font=("Arial", 11,"bold"))
        self.set_prompt_btn.pack(pady=5)

        self.sentence_label = tk.Label(root, text="", wraplength=600, font=("Arial", 13), fg="green")
        self.sentence_label.pack(pady=10)

        self.text_entry = tk.Text(root, height=5, width=60, font=("Arial", 12,"bold"))
        self.text_entry.pack(pady=10)
        self.text_entry.bind("<KeyPress>", self.start_typing)

        self.submit_btn = tk.Button(root, text="SUBMIT", command=self.calculate_speed, font=("Arial", 12,"bold"), bg="green", fg="white")
        self.submit_btn.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 13))
        self.result_label.pack(pady=10)

        self.incorrect_label = tk.Label(root, text="", font=("Arial", 11), fg="red", wraplength=600)
        self.incorrect_label.pack(pady=5)

    def set_prompt(self):
        self.sentence = self.prompt_entry.get().strip()
        if not self.sentence:
            messagebox.showwarning("Input Error", "Please enter a sentence.")
            return

        self.sentence_label.config(text=f"Type this: {self.sentence}")
        self.text_entry.delete("1.0", tk.END)
        self.prompt_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.incorrect_label.config(text="")
        self.start_time = None

    def start_typing(self, event):
        if self.start_time is None:
            self.start_time = time.time()

    def calculate_speed(self):
        typed_text = self.text_entry.get("1.0", tk.END).strip()
        if not typed_text:
            messagebox.showwarning("Warning", "Please type the sentence first!")
            return

        if not hasattr(self, 'sentence') or not self.sentence:
            messagebox.showwarning("Warning", "Set a sentence before typing!")
            return

        end_time = time.time()
        time_taken = end_time - self.start_time
        word_count = len(typed_text.split())
        wpm = (word_count / time_taken) * 60

      
        expected_words = self.sentence.split()
        typed_words = typed_text.split()

        correct = 0
        incorrect_words = []

        for ew, tw in zip(expected_words, typed_words):
            if ew == tw:
                correct += 1
            else:
                incorrect_words.append(f"Expected: '{ew}' | Typed: '{tw}'")

        accuracy = (correct / len(expected_words)) * 100

        self.result_label.config(
            text=f"Time: {round(time_taken, 2)} sec | WPM: {int(wpm)} | Accuracy: {round(accuracy)}%"
        )

        if accuracy < 100:
            self.incorrect_label.config(
                text="Incorrect words:\n" + "\n".join(incorrect_words)
            )
            messagebox.showinfo("Try Again", "Some words are incorrect. Please correct them and click Submit again.")
        else:
            self.incorrect_label.config(text="")
            self.root.after(3000, self.reset_for_next)

    def reset_for_next(self):
        self.sentence_label.config(text="")
        self.text_entry.delete("1.0", tk.END)
        self.result_label.config(text="")
        self.start_time = None
root = tk.Tk()
app = TypingSpeedApp(root)
root.mainloop()
