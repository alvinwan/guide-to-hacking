"""
Find initial states that have exactly one path to victory.
"""

from typing import List
from dataclasses import dataclass, field
from collections import defaultdict


##############
# GAME LOGIC #
##############


def get_empty_cells(moves):
    for i in map(str, range(9)):
        if i not in moves:
            yield i


def get_winner(moves):
    """
    >>> get_winner('3065412')
    0
    """
    player0 = ''.join(sorted(moves[::2]))
    player1 = ''.join(sorted(moves[1::2]))
    if is_winner(player0):
        return 0
    if is_winner(player1):
        return 1
    if len(moves) == 9:
        return 2
    return -1


def is_winner(moves):
    moves = set(moves)
    return any(all(move in moves for move in win) for win in (
        '012', '345', '678',  # horizontal
        '036', '147', '258',  # vertical
        '048', '246',  # diagonal
    ))


##########
# AGENTS #
##########


def agent_any(moves):
    yield from get_empty_cells(moves)


def agent_basic(moves, recurse=True):
    """
    >>> list(agent_basic('4208531'))  # must pick 7 to stop playerO from win
    ['7']
    """
    has_winning_move = False
    for move in get_empty_cells(moves):
        _moves = moves + move
        if get_winner(_moves) > -1:
            yield move  # take a winning move if there is one
            has_winning_move = True
    if has_winning_move:
        return

    if recurse:
        # don't make any moves that immediately result in enemy victory
        made_any_move = False
        for move in get_empty_cells(moves):
            _moves = moves + move
            is_losing_move = False
            for _move in agent_basic(_moves, recurse=False):
                __moves = _moves + _move
                if -1 < get_winner(__moves) < 2:
                    is_losing_move = True
            if not is_losing_move:
                made_any_move = True
                yield move
        if made_any_move:
            return

    # if all else fails, try all moves
    yield from get_empty_cells(moves)


###########
# SOLVING #
###########


# Represents a game state achievable by certain combinations of moves
@dataclass
class Node:
    children: dict = field(default_factory=dict) # game states for all possible moves after this state
    moves: str = '' # moves it took to get to this state
    winner: int = -1  # who wins in this state, if either
    counts: List[int] = field(default_factory=lambda: [0, 0, 0])  # counts of 0 win, 1 win, tie


def solve_board(node, agent=agent_basic):
    """Compute all possible moves for both sides."""
    if node.winner > -1:
        return
    for move in agent(node.moves):
        moves = node.moves + move
        child = Node({}, moves, get_winner(moves))
        node.children[move] = child
        solve_board(child)


length_to_moves = defaultdict(set)


def set_win_counts(node):
    """Mark any paths where one winner is guaranteed"""
    if node.winner > -1:
        node.counts[node.winner] += 1
    for child in node.children.values():
        set_win_counts(child)
        for i in range(len(node.counts)):
            node.counts[i] += child.counts[i]
    if (node.counts[0] == 0 or node.counts[1] == 0) and node.counts[2] == 0 and sum(node.counts[:2]) > 0 and node.children:
        length_to_moves[len(node.moves)].add(node.moves)  # add all cases that have definite victories


#######
# GUI #
#######


def print_moves(node):
    player = len(node.moves) % 2
    other = (player + 1) % 2
    for move, child in node.children.items():
        total = sum(child.counts) or 1
        print(f"Move {move}: {child.counts[player] / total * 100.:.2f}% win rate, {child.counts[other] / total * 100.:.2f}% lose rate")


def print_board(moves):
    cells = [' ' for _ in range(9)]
    for i, move in enumerate(moves):
        player = i % 2
        cells[int(move)] = 'O' if player == 0 else 'X'
    print('=' * 15)
    for start in range(0, 9, 3):
        print(cells[start:start + 3])


def agent_min_lose_max_win(node):
    """
    Simple agent that minimizes the number of ways it can lose. If tie, maximize
    number of ways it can win.
    """
    player = len(node.moves) % 2
    other = (player + 1) % 2

    best_move, min_lose, max_win = -1, 100000, 0
    for move, child in node.children.items():
        total = sum(child.counts)
        win, lose = child.counts[player] / total, child.counts[other] / total
        if lose < min_lose or (lose == min_lose and win > max_win):
            best_move, min_lose, max_win = move, lose, win
    yield best_move


def play(node, you=lambda node: input('> '), enemy=lambda node: next(agent_min_lose_max_win(node)), switch=False):
    if switch:
        you, enemy = enemy, you
    while node.winner == -1:
        print_board(node.moves)
        print_moves(node)
        node = node.children[you(node)]

        if node.winner == -1:
            print_board(node.moves)
            print_moves(node)
            node = node.children[enemy(node)]


############
# ANALYSIS #
############


def find_definite_victory():
    # TODO: move global `length_to_moves` into this function
    movess = sorted(length_to_moves[min(length_to_moves)])
    print(f"Shortest definite victory states: {movess}")

    prefixes = {moves[:2] for moves in movess}
    safe = set()
    for i in range(9):
        for j in range(9):
            if i != j:
                if f"{i}{j}" not in prefixes:
                    safe.add(f"{i}{j}")
    print(f"'Safe' prefixes: {sorted(safe)}")


if __name__ == '__main__':
    node = Node()
    # node = Node(moves='30674')
    # node = Node(moves='01234')
    # node = Node(moves='014')
    solve_board(node)
    set_win_counts(node)
    find_definite_victory()
    play(node, switch=True)