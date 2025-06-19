import json
import random


class Question:
    def __init__(self, text, answers, correct_index, difficulty):
        self.text = text
        self.answers = answers
        self.correct_index = correct_index
        self.difficulty = difficulty


class Game:
    def __init__(self, questions_file):
        self.questions = self.load_questions(questions_file)
        self.current_question_index = 0
        self.used_hints = {"50_50": False, "call": False, "audience": False}
        self.prize_levels = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000,
                             1000000]
        self.safe_levels = [5, 10]  # Несгораемые суммы на 5 и 10 вопросах

    def load_questions(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return [Question(q['question'], q['answers'], q['correct'], q['difficulty']) for q in data]

    def get_current_question(self):
        return self.questions[self.current_question_index]

    def check_answer(self, answer_index):
        correct = self.get_current_question().correct_index == answer_index
        if correct:
            self.current_question_index += 1
        return correct

    def get_prize(self):
        if self.current_question_index == 0:
            return 0
        # Возвращаем последнюю несгораемую сумму
        for level in reversed(self.safe_levels):
            if self.current_question_index >= level:
                return self.prize_levels[level - 1]
        return 0

    def is_game_over(self):
        return self.current_question_index >= len(self.questions)

    def use_50_50(self):
        if self.used_hints["50_50"]:
            return None

        self.used_hints["50_50"] = True
        question = self.get_current_question()
        wrong_answers = [i for i in range(4) if i != question.correct_index]
        remove = random.sample(wrong_answers, 2)
        return [i for i in range(4) if i not in remove]

    def use_call_friend(self):
        if self.used_hints["call"]:
            return None

        self.used_hints["call"] = True
        question = self.get_current_question()
        # 80% вероятность правильного ответа
        if random.random() < 0.8:
            return question.correct_index
        return random.randint(0, 3)

    def use_audience_help(self):
        if self.used_hints["audience"]:
            return None

        self.used_hints["audience"] = True
        question = self.get_current_question()
        # Генерация псевдо-результатов голосования
        correct_percent = random.randint(60, 90)
        remaining = 100 - correct_percent
        wrong_percents = [random.randint(1, remaining - 2) for _ in range(3)]
        total_wrong = sum(wrong_percents)

        # Нормализация
        if total_wrong > 0:
            scale = remaining / total_wrong
            wrong_percents = [int(p * scale) for p in wrong_percents]

        # Создаем распределение
        result = [0] * 4
        result[question.correct_index] = correct_percent

        wrong_indices = [i for i in range(4) if i != question.correct_index]
        for i, idx in enumerate(wrong_indices):
            result[idx] = wrong_percents[i]

        # Корректировка суммы
        total = sum(result)
        if total < 100:
            result[question.correct_index] += 100 - total
        return result
