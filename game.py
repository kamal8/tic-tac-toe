import random
import copy
from typing import List, Set
from enum import Enum
from dataclasses import dataclass, field



class Player(Enum):
    Computer = 'O'
    You = 'X'

def select_random_player():
    return list(Player)[random.randint(0, 1)]


@dataclass
class GameState:
    current_player: Player = field(default_factory=select_random_player)
    board: List = field(default_factory=list)
    turn: int = 0
    available_options: Set = field(default_factory=set)

    def toggle_user(self):
        self.current_player = Player.Computer if self.current_player == Player.You else Player.You

    def has_winner(self):
        if (self.board[0] == self.board[1] == self.board[2] and self.board[2] != " ") or \
                (self.board[3] == self.board[4] == self.board[5] and self.board[5] != " ") or \
                (self.board[6] == self.board[7] == self.board[8] and self.board[8] != " ") or \
                (self.board[0] == self.board[3] == self.board[6] and self.board[6] != " ") or \
                (self.board[1] == self.board[4] == self.board[7] and self.board[7] != " ") or \
                (self.board[2] == self.board[5] == self.board[8] and self.board[8] != " ") or \
                (self.board[0] == self.board[4] == self.board[8] and self.board[8] != " ") or \
                (self.board[2] == self.board[4] == self.board[6] and self.board[6] != " "):
            return True
        else:
            return False

    def get_winner(self):
        # horizontal
        if self.board[0] == self.board[1] == self.board[2] and self.board[2] != " ":
            return Player(self.board[0])
        elif self.board[3] == self.board[4] == self.board[5] and self.board[5] != " ":
            return Player(self.board[3])
        elif self.board[6] == self.board[7] == self.board[8] and self.board[8] != " ":
            return Player(self.board[6])
        # vertical
        elif self.board[0] == self.board[3] == self.board[6] and self.board[6] != " ":
            return Player(self.board[0])
        elif self.board[1] == self.board[4] == self.board[7] and self.board[7] != " ":
            return Player(self.board[1])
        elif self.board[2] == self.board[5] == self.board[8] and self.board[8] != " ":
            return Player(self.board[2])
        #diagonal
        elif self.board[0] == self.board[4] == self.board[8] and self.board[8] != " ":
            return Player(self.board[0])
        elif self.board[2] == self.board[4] == self.board[6] and self.board[6] != " ":
            return Player(self.board[2])
        else:
            return None


    def is_game_over(self):
        if self.turn < 4:
            return False
        if self.has_winner():
            return True
        if self.turn > 8:
            return True

    def make_move(self, move, show_board=True):
        self.board[move] = self.current_player.value
        self.available_options.remove(move)
        if show_board:
            self.print_board()
        self.turn += 1
        self.toggle_user()

    def set_empty_board(self):
        self.board = [" "] * 9

    def print_board(self):
        print(f"{self.current_player.name} played:\n")
        grid: str = """
                 |          |
            {}    |    {}     |   {}
                 |          |
        ---------+----------+--------
                 |          |
            {}    |    {}     |   {}
                 |          |
        ---------+----------+---------
                 |          |
            {}    |    {}     |   {}
                 |          |
        """
        print(grid.format(*self.board))

def minimax(game_state: GameState, depth: int = 0):
    if game_state.is_game_over():
        if not game_state.has_winner():
            return 0
        return (10 - depth) if game_state.get_winner() == Player.Computer else (-10 + depth)

    best = -1*float('inf') if game_state.current_player == Player.Computer else float('inf')
    operation = max if game_state.current_player == Player.Computer else min
    for option in game_state.available_options:
        gs = GameState(**copy.deepcopy(game_state.__dict__))
        gs.make_move(option, show_board=False)
        best = operation(best, minimax(gs, depth=(depth + 1)))
    return best



def play_computer_turn(game_state: GameState):
    best_score = None
    best_option = None

    for option in game_state.available_options:
        gs = GameState(**copy.deepcopy(game_state.__dict__))
        gs.make_move(option, show_board=False)
        score = minimax(gs)
        if best_option is None or best_score is None:
            best_option = option
            best_score = score
        elif best_score < score:
            best_score = score
            best_option = option
    return best_option


def play_human_turn(game_state: GameState) -> int:
    """
    :param game_state: state of the game
    :return:
    """
    while True:
        choice = input(""" please select between 1 to 9 to mark your box:
1|2|3
-+-+-
4|5|6
-+-+-
7|8|9
""")
        if choice.isnumeric() and (int(choice) - 1) in game_state.available_options:
            return int(choice) - 1
        print("invalid choice please try again")

PLAYER_MOVE_FUNC = {
    Player.Computer: play_computer_turn,
    Player.You: play_human_turn
}

def play_game():
    global PLAYER_MOVE_FUNC
    game_state = GameState(available_options={0, 1, 2, 3, 4, 5, 6, 7, 8})
    game_state.set_empty_board()
    while not game_state.is_game_over():
        move = PLAYER_MOVE_FUNC[game_state.current_player](game_state)
        game_state.make_move(move)

    if game_state.has_winner():
        winner = game_state.get_winner()
        print("!" * 20)
        print(f"{winner.name} won the game!")
        print("!" * 20)
    else:
        print("GAME DRAW!!!")
    return


def prompt_retry():
    """prompt user for retry"""
    choice = input("would you like to retry the game? (Yes / No):")
    return choice.lower().startswith('y')


def main():
    retry: bool = True
    while retry:
        print("Welcome to tic-tac-toe YOu vs. Computer. You will play with mark 'X' while computer will play with 'O'")
        play_game()
        retry = prompt_retry()
    print("Thanks for playing the game. see you later!!")


if __name__ == "__main__":
    main()
