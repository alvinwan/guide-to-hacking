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
from itertools import product
import functools
import csv
import requests
import os
import time


#######
# CLI #
#######


PLAYERS = {}

def register(f):
    PLAYERS[f.__name__] = f

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('agent', default=[], nargs='*', choices=list(PLAYERS.keys()) + ['all'], help="Which agents to run. Use 'user' to play yourself")
    parser.add_argument('-n', '--num_trials', default=10, type=int, help="How many trials to run for each agent. 'user' is only run once.")
    parser.add_argument('-s', '--stat', default=['score', 'largest'], action='append', help="Which statistics to report.")
    parser.add_argument('--seed', type=int, help='Seed first trial with this')
    args = parser.parse_args()

    should_write_headers = False
    if not os.path.exists('results.csv'):
        should_write_headers = True
    else:
        with open('results.csv') as f:
            if not f.read().strip():
                should_write_headers = True

    with open('results.csv', 'a') as f:
        writer = None
        for name, player in PLAYERS.items():
            should_execute = name in args.agent or ('all' in args.agent and name != 'user')
            if not should_execute:
                continue
            num_trials = 1 if name == 'user' else args.num_trials
            statistics = get_play_score(player, num_trials, args.stat, args.seed)
            print(f"{name}: {statistics}")
            if writer is None:
                writer = csv.DictWriter(f, sorted(statistics.keys()))
                if should_write_headers:
                    writer.writeheader()
            writer.writerow(statistics)


def get_play_score(player, num_trials, stats=('score', 'largest'), seed=123):
    """Calculate statistics (min/mean/max)"""
    random.seed(seed)
    final = {
        'name': player.__name__,
        'path': f"out/{player.__name__}-{time.time()}.md",
        'num_trials': num_trials,
        'seed': seed,
    }
    logger = get_game_logger(final['path'], final)
    info = [play(player, callback=logger) for _ in range(num_trials)]
    for stat in stats:
        scores = [item[stat] for item in info]
        final[f"{stat}_avg"] = sum(scores) / float(len(scores))
        final[f"{stat}_max"] = max(scores)
        final[f"{stat}_min"] = min(scores)
    return final


def get_game_logger(path, metadata):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a') as f:
        # write frontmatter
        f.write(f"---\nTime: {time.time()}\nSeed: {metadata['seed']}\n---\n\n")

    def log_game_move(move, board, state):
        # write move data
        with open(path, 'a') as f:
            f.write('---\n\n')
            f.write(f"Game:\n```\n{stringify(board, pretty=True)}```\n\n")
            f.write(f"Move: {move}\n\n")
            f.write(f"Score: {state['score']}\n\n")
            if 'response' in state:
                f.write(f"Justification:\n```\n{state['response']['justification']}\n```\n\n")
    return log_game_move


def stringify(board, pretty=False):
    """Pretty print the board.
    
    >>> board = make_board()
    >>> populate_sample_board(board)
    >>> board[3][3] = 128
    >>> show(board, pretty=True)
    |   |   |   |   |
    |   |2  |   |   |
    |   |   |8  |4  |
    |   |   |2  |128|
    """
    blank = '' if pretty else 0
    hsep = '|' if pretty else ''
    ndigits = ceil(log(largest(board)) / log(10))
    string = ''
    for row in board:
        string += hsep + hsep.join([
            str(item if item != 0 else blank).ljust(ndigits)
            for item in row
        ]) + hsep + '\n'
    return string


def show(board, pretty=False):
    print(stringify(board, pretty))


@register
def user(board, state):
    show(board, pretty=True)
    while (move := input('[wasd]:')) not in ('w', 'a', 's', 'd'):
        pass
    return move


##########
# AGENTS #
##########


@register
def alwaysdown(board, state):
    return 'd'


@register
def cycleas(board, state):
    state['index'] = (state.get('index', 0) + 1) % 2
    return 'sa'[state['index']]


@register
def cyclewasd(board, state):
    state['index'] = (state.get('index', 0) + 1) % 4
    return 'wasd'[state['index']]


@register
def cycleadws(board, state):
    state['index'] = (state.get('index', 0) + 1) % 4
    return 'adws'[state['index']]


@register
def trulyrandom(board, state):
    return random.choice('wasd')


PROMPT = """
Let's play 2048. In your response, the first line is one of four possible commands: 'w' for up, 'a' for left, 's' for down, or 'd' for right. Do not include extraneous text in this first line. After the first line, include justification for your move step-by-step. Be succinct.

Here are examples:

---

Game:
|   |   |   |   |
|   |2  |   |   |
|   |   |8  |4  |
|   |2  |4  |128|

You:
s
There are two 2s that can be merged with an up or down.
If I merge down, I get a 4 that can be merged horizontally, in the last row, on the next turn.

---

Game:
|  |  |  |  |
|  |  |  |4 |
|4 |2 |4 |  |
|16|16|8 |4 |

You:
a
There are two 4s that can be merged with a down or up
There are also two 16s that can be merged with a left or right.
Since 16 > 4, I consider left or right.
If I merge right, this will additionally place 3 4s directly on top of each other.

---

Game:
{board}

You:"""


def huggingface(model_id, prompt, temperature=1.):
    """
    Query an LLM hosted on Huggingface
    
    Source: https://huggingface.co/docs/api-inference/quicktour
    Get token at: https://huggingface.co/settings/tokens
    """
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {os.environ['HUGGINGFACE_API_KEY']}"}
    response = requests.post(url, headers=headers, json={
        'inputs': prompt,
        'parameters': {
            'temperature': temperature,
            'use_cache': False,
        }
    })
    response = response.json()
    if 'error' in response:
        raise RuntimeError(response['error'])
    return response[0]['generated_text'].replace(prompt, '')


def get_move(model, model_id, board):
    """
    Query an LLM hosted on Huggingface for its 2048 move.
    """
    prompt = PROMPT.format(board=stringify(board, pretty=True))
    move, temperature = '', 1.0
    while not move:
        try:
            response = model(model_id, prompt, temperature=temperature)
            move, justification = response.split('---')[0].strip().split('\n', 1)
        except ValueError:  # ran into a parsing error
            temperature *= 0.8
    return {'move': move.strip()[0], 'justification': justification, 'raw': response}


@register
def openchat(board, state):
    state['response'] = get_move(huggingface, 'openchat/openchat-3.5-0106', board)
    return state['response']['move']


@register
def mixtral(board, state):
    state['response'] = get_move(huggingface, 'mistralai/Mixtral-8x7B-Instruct-v0.1', board)
    return state['response']['move']


@register
def mistral(board, state):
    state['response'] = get_move(huggingface, 'mistralai/Mistral-7B-Instruct-v0.2', board)
    return state['response']['move']


def openai(model_id, prompt, temperature):
    """
    Query an LLM hosted by OpenAI

    Source: https://platform.openai.com/docs/api-reference/making-requests
    Get token at: https://platform.openai.com/api-keys
    """
    # ignores temperature for now
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"}
    response = requests.post(url, headers=headers, json={
        'model': model_id,
        'messages': [{'role': 'user', 'content': prompt}],
    })
    response = response.json()
    return response['choices'][0]['message']['content']


@register
def chatgpt3(board, state):
    state['response'] = get_move(openai, 'gpt-3.5-turbo', board)
    return state['response']['move']


@register
def chatgpt4(board, state):
    state['response'] = get_move(openai, 'gpt-4', board)
    return state['response']['move']


########
# GAME #
########


def play(player, callback=lambda move, board, state: None):
    """Play game of 2048 with user."""
    board = make_board()
    state = {'score': 0}
    while not is_full(board):
        spawn(board)
        move = player(board, state)
        callback(move, board, state)
        board = shift(board, move, state)
    state['board'] = board
    state['largest'] = largest(board)
    return state


def largest(board):
    return max(max(row) for row in board)


def make_board():
    """Create empty 4x4 board."""
    return [[0 for _ in range(4)] for _ in range(4)]  # make board


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
    >>> board = make_board()
    >>> populate_sample_board(board)
    >>> show(shift(board, 's'))  # down
    0000
    0000
    0084
    0228
    >>> board = make_board()
    >>> populate_sample_board(board)
    >>> show(shift(board, 'w'))  # up
    0284
    0028
    0000
    0000
    >>> board = make_board()
    >>> populate_sample_board(board)
    >>> show(shift(board, 'd'))  # right
    0000
    0002
    0084
    0028
    """
    directions = {'a': 0, 's': 1, 'd': 2, 'w': 3}
    n = directions[direction.lower()]

    for _ in range(n):  # rotate clockwise until we can shift left
        board = rotate(board)

    board = shift_left(board, state)  # shift left

    for _ in range(n):  # rotate counterclockwise back to original orientation
        board = rotate(board, False)

    return board


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
    for row, col in product(range(4), range(4)):
        nrow = col      if cw else 3 - col  # Calculate new row index
        ncol = 3 - row  if cw else row  # Calculate new col index
        new_board[nrow][ncol] = board[row][col]  # Copy element to new pos
    return new_board


def shift_left(board, state={}):
    """Shifts elements to the left, merging equal adjacent elements.
    
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
    >>> board[1][0] = board[1][2] = board[1][3] = 2
    >>> show(shift_left(board))
    4800
    4200
    0000
    0000
    """
    for row in board:
        col = 0  # Column index, as we move left to right along the row
        merged = False  # Flag to track if merging occurred

        for item in row:
            if not merged and item and col > 0 and row[col - 1] == item:  # Check for merge
                row[col - 1] *= 2  # Merge elements
                state['score'] = state.get('score', 0) + row[col - 1]
                merged = True
            elif item or merged:  # Add non-zero or after merge
                row[col] = item
                merged = False
                col += 1

        for i in range(col, 4):  # Pad the rest with zeros
            row[i] = 0
    return board


def spawn(board):
    """
    Spawn 2 with 90% probability or a 4 with 10% probability in a randomly-
    selected empty cell.
    """
    row, col = random.choice([
        (row, col) for row, col in product(range(4), range(4))
        if board[row][col] == 0
    ])
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


if __name__ == '__main__':
    main()