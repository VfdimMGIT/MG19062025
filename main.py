import tkinter as tk
from gui import MainMenu, GameWindow


class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Кто хочет стать миллионером")
        self.root.geometry("600x400")
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()
        self.current_window = MainMenu(self.root, self.start_game)

    def start_game(self):
        from game_logic import Game
        self.clear_window()
        game = Game("questions.json")
        self.current_window = GameWindow(self.root, game)

    def clear_window(self):
        if hasattr(self, 'current_window'):
            for widget in self.root.winfo_children():
                widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MillionaireGame(root)
    root.mainloop()
