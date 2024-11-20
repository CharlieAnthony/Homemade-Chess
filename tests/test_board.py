import pytest
from board import Board

@pytest.fixture
def board():
    return Board()

def test_board_get_raw_moves(board):
    # pawn moves
    moves = board.get_raw_moves((0, 6))
    assert (0, 5) in moves
    assert (0, 4) in moves
    board.state[5][0] = "wp"
    assert board.get_raw_moves((0, 5)) == [(0, 4)]

    # king moves
    board.state[6][4] = ""
    moves = board.get_raw_moves((4, 7))
    assert moves == [(4, 6)]
    board.state[4][4] = "wk"
    moves = board.get_raw_moves((4, 4))
    available_moves = [(5, 5), (5, 4), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (3, 3)]
    for move in available_moves:
        assert move in moves
    board.state[4][5] = "wp"
    available_moves = [(5, 5), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (3, 3)]
    for move in available_moves:
        assert move in moves
    board.state[4][5] = "bp"
    available_moves = [(5, 5), (5, 4), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (3, 3)]
    for move in available_moves:
        assert move in moves


def test_board_get_available_moves():
    pass

def test_board_move_piece():
    pass

def test_board_get_new_state():
    pass

def test_board_is_check():
    pass

def test_board_find_king_position():
    pass
