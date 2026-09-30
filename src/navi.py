from simple_term_menu import TerminalMenu
import json
from pathlib import Path
import sys

from game import Game
from utils import clear_terminal

current_dir = Path(__file__).resolve().parent

data_dir = current_dir.parent / "data"

single_round_path = data_dir / "single_round_difficulties.json"
multi_round_path = data_dir / "multi_round_modes.json"
guide_path = data_dir / "guide.txt"

"""
This class is used for navigating throughout the game menus. These menus
allow for the starting of different game modes as well as viewing guides
and editing settings.
"""
class MenuNavi:
    def __init__(self, user: str):
        self.user = user
    
    @staticmethod
    def get_single_round_dif():
        with open(single_round_path, "r") as f:
            raw_single_round = json.load(f)

        """
        key: difficulty
        value: tuple of (columns, rows)
        """
        single_round_difficulties = {
            key: tuple(value) 
            for key, value in raw_single_round.items()
        }

        return single_round_difficulties

    @staticmethod
    def get_multi_round_modes():
        with open(multi_round_path, "r") as f:
            raw_multi_round = json.load(f)

        """
        key: difficulty
        value: tuple of (round count, list of round configs)
        """
        multi_round_modes = {
            key: (value["round_count"], value["round_configs"])
            for key, value in raw_multi_round.items()
        }

        return multi_round_modes

    @staticmethod
    def main_menu():
        options = ["Play Game", "Guide", "Exit"]
        terminal_menu = TerminalMenu(options, title="Main Menu")
        menu_entry_index = terminal_menu.show()
        
        match menu_entry_index:
            case 0:
                MenuNavi.select_game_menu()

            case 1:
                MenuNavi.view_guide()
                clear_terminal()

            case 2:
                print("Quitting Mastermind Game!")
                sys.exit()

        MenuNavi.main_menu()

    @staticmethod
    def select_game_menu():
        options = ["Single Round", "Multiple Rounds", "Go Back"]
        terminal_menu = TerminalMenu(options, title="Play Game")
        menu_entry_index = terminal_menu.show()
        
        match menu_entry_index:
            case 0:
                MenuNavi.single_round_menu()

            case 1:
                MenuNavi.multi_round_menu()

            case 2:
                MenuNavi.main_menu()

            case _:
                MenuNavi.select_game_menu()

    @staticmethod
    def view_guide():
        try:
            with open(guide_path, "r", encoding="utf-8") as file:
                content = file.read()
                print(content + "\n")
        except FileNotFoundError:
            print(f"Error: The file at '{guide_path}' was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        input("Press Enter To Continue")

    @staticmethod
    def single_round_menu():
        single_round_difficulties = MenuNavi.get_single_round_dif()
        options = ["Hard", "Medium", "Easy", "Go Back"]
        terminal_menu = TerminalMenu(options, title="Play Single Round")
        menu_entry_index = terminal_menu.show()
        
        match menu_entry_index:
            case 0:
                new_game = Game(1, [{"columns": single_round_difficulties["hard"][0], "rows": single_round_difficulties["hard"][1]}])

                new_game.play_game()

            case 1:
                new_game = Game(1, [{"columns": single_round_difficulties["medium"][0], "rows": single_round_difficulties["hard"][1]}])

                new_game.play_game()

            case 2:
                new_game = Game(1, [{"columns": single_round_difficulties["easy"][0], "rows": single_round_difficulties["hard"][1]}])

                new_game.play_game()

            case 3:
                MenuNavi.select_game_menu()

            case _:
                MenuNavi.single_round_menu()

        MenuNavi.select_game_menu()

    @staticmethod
    def multi_round_menu():
        multi_round_modes = MenuNavi.get_multi_round_modes()
        options = ["Long", "Normal", "Short", "Go Back"]
        terminal_menu = TerminalMenu(options, title="Play Single Round")
        menu_entry_index = terminal_menu.show()
        
        match menu_entry_index:
            case 0:
                new_game = Game(multi_round_modes["long"][0], multi_round_modes["long"][1])

                new_game.play_game()

            case 1:
                new_game = Game(multi_round_modes["normal"][0], multi_round_modes["normal"][1])

                new_game.play_game()

            case 2:
                new_game = Game(multi_round_modes["short"][0], multi_round_modes["short"][1])

                new_game.play_game()

            case 3:
                MenuNavi.select_game_menu()

            case _:
                MenuNavi.multi_round_menu()

        MenuNavi.select_game_menu()