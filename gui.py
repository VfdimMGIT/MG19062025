import tkinter as tk
from tkinter import messagebox, Frame, Label, Button
from game_logic import Game


class MainMenu:
    def __init__(self, root, start_game_callback):
        self.root = root
        self.root.title("Кто хочет стать миллионером")
        self.root.geometry("600x400")

        frame = Frame(self.root)
        frame.pack(expand=True)

        Label(frame, text="Кто хочет стать миллионером", font=("Arial", 24)).pack(pady=50)

        Button(frame, text="Играть", font=("Arial", 18),
               command=start_game_callback, width=15).pack(pady=10)
        Button(frame, text="Выход", font=("Arial", 18),
               command=self.root.quit, width=15).pack(pady=10)


class GameWindow:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.root.title("Игра")
        self.root.geometry("800x600")

        # Основные фреймы
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Фрейм для вопроса
        self.question_frame = Frame(self.main_frame)
        self.question_frame.pack(fill=tk.X, padx=20, pady=20)

        # Фрейм для ответов
        self.answers_frame = Frame(self.main_frame)
        self.answers_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Фрейм для подсказок
        self.hints_frame = Frame(self.main_frame)
        self.hints_frame.pack(fill=tk.X, padx=20, pady=10)

        # Шкала выигрышей
        self.prize_frame = Frame(self.root, width=150)
        self.prize_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.create_widgets()
        self.show_question()

    def create_widgets(self):
        # Вопрос
        self.question_label = Label(
            self.question_frame,
            text="",
            font=("Arial", 14),
            wraplength=600,
            justify="center"
        )
        self.question_label.pack(fill=tk.X)

        # Кнопки ответов
        self.answer_buttons = []
        for i in range(4):
            btn = Button(
                self.answers_frame,
                text="",
                font=("Arial", 12),
                command=lambda idx=i: self.check_answer(idx),
                height=2,
                wraplength=300
            )
            btn.pack(fill=tk.BOTH, expand=True, pady=5)
            self.answer_buttons.append(btn)

        # Кнопки подсказок
        Button(self.hints_frame, text="50/50",
               command=self.use_50_50, state=tk.NORMAL).pack(side=tk.LEFT, padx=5)
        Button(self.hints_frame, text="Звонок другу",
               command=self.use_call_friend).pack(side=tk.LEFT, padx=5)
        Button(self.hints_frame, text="Помощь зала",
               command=self.use_audience_help).pack(side=tk.LEFT, padx=5)

        # Шкала выигрышей
        for i, prize in enumerate(self.game.prize_levels):
            level = i + 1
            bg = "gold" if level in self.game.safe_levels else "white"
            lbl = Label(
                self.prize_frame,
                text=f"{level}. {prize:,} ₽",
                font=("Arial", 10),
                bg=bg,
                width=15,
                anchor="w"
            )
            lbl.pack(fill=tk.X, pady=2)
            if level == self.game.current_question_index + 1:
                lbl.config(bg="lightgreen")

    def show_question(self):
        if self.game.is_game_over():
            self.show_final(True)
            return

        question = self.game.get_current_question()
        self.question_label.config(text=question.text)

        for i, btn in enumerate(self.answer_buttons):
            btn.config(text=question.answers[i], state=tk.NORMAL, bg="SystemButtonFace")

    def check_answer(self, answer_index):
        if self.game.check_answer(answer_index):
            if self.game.is_game_over():
                self.show_final(True)
            else:
                self.show_question()
        else:
            self.show_final(False)

    def use_50_50(self):
        indices = self.game.use_50_50()
        if indices is None:
            return

        for i, btn in enumerate(self.answer_buttons):
            if i not in indices:
                btn.config(state=tk.DISABLED)

    def use_call_friend(self):
        answer = self.game.use_call_friend()
        if answer is None:
            return

        messagebox.showinfo(
            "Звонок другу",
            f"Друг считает, что правильный ответ: {self.game.get_current_question().answers[answer]}"
        )

    def use_audience_help(self):
        result = self.game.use_audience_help()
        if result is None:
            return

        question = self.game.get_current_question()
        help_text = "Результаты голосования зала:\n"
        for i, percent in enumerate(result):
            help_text += f"{question.answers[i]}: {percent}%\n"

        messagebox.showinfo("Помощь зала", help_text)

    def show_final(self, win):
        prize = self.game.prize_levels[-1] if win else self.game.get_prize()
        message = (f"Поздравляем! Вы выиграли {prize:,} ₽!" if win
                   else f"Игра окончена. Ваш выигрыш: {prize:,} ₽")

        messagebox.showinfo("Игра окончена", message)
        self.root.destroy()


class EndWindow:
    def __init__(self, root, message):
        self.root = root
        self.root.title("Игра окончена")
        self.root.geometry("400x200")

        Label(root, text=message, font=("Arial", 14)).pack(pady=50)
        Button(root, text="Закрыть", command=root.destroy).pack()
