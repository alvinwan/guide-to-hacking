"""Implementation of 2048 in Python. Written as CLI.

Other implementations of 2048 in Python:
https://github.com/yangshun/2048-python/tree/master
https://gist.github.com/wynand1004/5e06ce54a430619785e355fd9b60fff3

Integrations with AI (received poorly: https://news.ycombinator.com/item?id=35785005)
https://github.com/riley-ball/2048ai
https://github.com/inishchith/2048
"""
import random
from math import log, ceil
import argparse
import functools
import csv


PLAYERS = {}

def register(f):
    PLAYERS[f.__name__] = f

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--agent', default=[], action='append')
    parser.add_argument('-n', '--num_trials', default=10, type=int)
    parser.add_argument('-s', '--stat', default=['score', 'largest'], action='append')
    args = parser.parse_args()

    if not args.agent or 'user' in args.agent:
        play(player=lambda board: input('[wasd]:'), ui=True)
        return

    with open('results.csv', 'w') as f:
        writer = None
        for name, player in PLAYERS.items():
            statistics = get_play_score(player, args.num_trials, args.stat)
            print(f"{name}: {statistics}")
            if writer is None:
                writer = csv.DictWriter(f, sorted(statistics.keys()))
                writer.writeheader()
            writer.writerow(statistics)


def get_play_score(player, num_trials, stats=('score', 'largest')):
    """Calculate statistics (min/mean/max)"""
    final = {}
    info = [play(player, ui=False) for _ in range(num_trials)]
    for stat in stats:
        scores = [item[stat] for item in info]
        final[f"{stat}_avg"] = sum(scores) / float(len(scores))
        final[f"{stat}_max"] = max(scores)
        final[f"{stat}_min"] = min(scores)
    return final


def play(player, ui=True):
    """Play game of 2048 with user."""
    board = make_board()
    state = {'score': 0}
    while not is_full(board):
        spawn(board)
        if ui:
            show(board, pretty=True)
        while (move := player(board)) not in ('w', 'a', 's', 'd'):
            pass
        board = shift(board, move, state)
    state['board'] = board
    state['largest'] = largest(board)
    return state


def make_board(D=4):
    """Create empty DxD board. 4 is hard-coded everywhere, so really D=4."""
    return [[0 for _ in range(D)] for _ in range(D)]  # make board


def is_full(board):
    """Check if the board is full. If so, terminate the game."""
    return all([all([item != 0 for item in row]) for row in board])


def shift(board, direction, state={}):
    """
    Shift all items in a certain cardinal direction, merging any neighboring
    identical numbers after the shift.

    >>> board = make_board()
    >>> populate_sample_board(board)
    >>> show(shift(board, 'a'))  # left
    0000
    2000
    8400
    2800
    >>> show(shift(board, 's'))  # down
    0000
    0000
    0084
    0228
    >>> show(shift(board, 'w'))  # up
    0284
    0028
    0000
    0000
    >>> show(shift(board, 'd'))  # right
    0000
    0002
    0084
    0028
    """
    direction = direction.lower()
    if direction == 'a':  # left
        return shift_left(board, state)
    if direction == 'w':  # up
        return rotate(shift_left(rotate(board, False), state))
    if direction == 'd':  # right
        return rotate(rotate(shift_left(rotate(rotate(board)), state), False), False)
    if direction == 's':  # down
        return rotate(shift_left(rotate(board), state), False)
    raise NotImplementedError('Invalid move')


def largest(board):
    return max(max(row) for row in board)


def show(board, pretty=False):
    """Pretty print the board.
    
    >>> board = make_board()
    >>> populate_sample_board(board)
    >>> board[3][3] = 128
    >>> show(board, pretty=True)
    |0  |0  |0  |0  |
    |0  |2  |0  |0  |
    |0  |0  |8  |4  |
    |0  |0  |2  |128|
    """
    hsep = '|' if pretty else ''
    ndigits = ceil(log(largest(board)) / log(10))
    for row in board:
        print(hsep + hsep.join([str(item).ljust(ndigits) for item in row]) + hsep)


def rotate(board, cw=True):
    """
    Rotate the board by 90˚. By default, clockwise.

    >>> board = make_board()
    >>> populate_sample_board(board)
    >>> board = rotate(board)
    >>> show(board)
    0000
    0020
    2800
    8400
    >>> board = rotate(board, cw=False)
    >>> show(board)
    0000
    0200
    0084
    0028
    """
    new_board = make_board()
    for row in range(4):
        for col in range(4):
            nrow = col      if cw else 3 - col
            ncol = 3 - row  if cw else row
            new_board[nrow][ncol] = board[row][col]
    return new_board


def shift_left(board, state={}):
    """
    >>> board = make_board()
    >>> populate_sample_board(board)
    >>> show(shift_left(board))
    0000
    2000
    8400
    2800
    >>> board = make_board()  # test merge
    >>> board[0][0] = board[0][1] = 2
    >>> board[0][2] = board[0][3] = 4
    >>> show(shift_left(board))
    4800
    0000
    0000
    0000
    """
    new_board = []
    for row in board:
        new_row = []
        candidate = 0
        for item in row:
            if candidate != 0 and item == candidate:
                new_row.append(candidate * 2)
                state['score'] = state.get('score', 0) + candidate * 2
                candidate = 0
            else:
                if candidate != 0:
                    new_row.append(candidate)
                candidate = item

        if candidate != 0:
            new_row.append(candidate)

        for _ in range(len(new_row), 4):
            new_row.append(0)
        
        new_board.append(new_row)
    return new_board


def spawn(board):
    cells = []
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                cells.append((row, col))
    row, col = random.choice(cells)
    board[row][col] = 2 if random.random() <= 0.9 else 4


###########
# TESTING #
###########
    
def populate_sample_board(board):
    """
    Populate a sample board. Used for testing, mainly.
    
    >>> board = make_board()
    >>> populate_sample_board(board)
    >>> show(board)
    0000
    0200
    0084
    0028
    """
    board[1][1] = board[3][2] = 2
    board[2][3] = 4
    board[2][2] = board[3][3] = 8


##########
# AGENTS #
##########


state = {}


@register
def alwaysdown(board):
    return 'd'


@register
def alwaysbottomdown(board):
    state['index'] = (state.get('index', 0) + 1) % 2
    return 'sa'[state['index']]


@register
def cyclewasd(board):
    state['index'] = (state.get('index', 0) + 1) % 4
    return 'wasd'[state['index']]


@register
def cycleadws(board):
    state['index'] = (state.get('index', 0) + 1) % 4
    return 'adws'[state['index']]


@register
def trulyrandom(board):
    return random.choice('wasd')


if __name__ == '__main__':
    main()