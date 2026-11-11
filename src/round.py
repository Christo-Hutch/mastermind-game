from random import choices

from board import Board

"""
This class is used to create and compare Code-maker responses to rows
on the parsed Board object instance. This class also features methods
to print rows of a board along with the related response.
"""
class Round:
    def __init__(self, board: Board):
        self.board: Board = board
        self.responses: list = self.generate_response_list(board.num_of_columns, board.num_of_rows)
        self.first_empty_row: int = 0
        self.remaining_rows: int = board.num_of_rows
        self.code: list = self.generate_random_code()
        self.isWon: bool = False
    
    @staticmethod
    def generate_response_list(column_count: int, row_count: int) -> list:
        return [[' ' for _ in range(column_count)] for _ in range(row_count)]
    
    def generate_random_code(self) -> list:
        available_colors = list(self.board.colors.keys())

        # Remove empty entry from potential colors
        available_colors.remove("  ")
        return choices(available_colors, k = self.board.num_of_columns)
    
    def get_formatted_response_row(self, row_num: int) -> str:
        return f"|" + "|".join(self.responses[row_num]) + "|"
    
    def calculate_response(self, row_guess: list) -> list:
        white_pegs = 0
        black_pegs = 0

        code_remaining = []
        guess_remaining = []

        for c, g in zip(self.code, row_guess):
            if c == g:
                black_pegs += 1
            else:
                code_remaining.append(c)
                guess_remaining.append(g)

        for g in guess_remaining:
            if g in code_remaining:
                white_pegs += 1
                code_remaining.remove(g)

        return (['●'] * black_pegs) + (['○'] * white_pegs) + ([' '] * (self.board.num_of_columns - (black_pegs + white_pegs)))
    
    def get_row_response_formatted(self, row_num: int) -> str:
        return self.board.get_formatted_row(row_num) + "=" + self.get_formatted_response_row(row_num)
    
    def print_round_board(self):
        for r in range(self.board.num_of_rows):
            print(self.get_row_response_formatted(r))

    def attempt_row(self, row_data: list):
        if self.remaining_rows <= 0:
            raise ValueError("No remaining rows for board left!")
        
        self.board.change_row(self.first_empty_row, row_data)
        response = self.calculate_response(row_data)
        self.responses[self.first_empty_row] = response

        self.first_empty_row += 1
        self.remaining_rows -= 1

        if response == (['●'] * self.board.num_of_columns):
            self.isWon = True
    
    def get_score(self) -> int:
        if not self.isWon:
            score = 0
        
        return int(((self.board.num_of_rows - self.first_empty_row + 1) / self.board.num_of_rows) * 100)