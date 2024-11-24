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
        moves.pop(moves.index(move))
    assert len(moves) == 0
    board.state[4][5] = "wp"
    moves = board.get_raw_moves((4, 4))
    available_moves = [(5, 5), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (3, 3)]
    for move in available_moves:
        assert move in moves
        moves.pop(moves.index(move))
    assert len(moves) == 0
    board.state[4][5] = "bp"
    moves = board.get_raw_moves((4, 4))
    available_moves = [(5, 5), (5, 4), (5, 3), (4, 5), (4, 3), (3, 5), (3, 4), (3, 3)]
    for move in available_moves:
        assert move in moves
        moves.pop(moves.index(move))
    assert len(moves) == 0

    # queen moves
    board.state = [["bq", "", "", "", "bp", "", "", ""],
                   ["", "", "bp", "bp", "bp", "", "", ""],
                   ["", "bp", "", "bp", "bp", "", "", ""],
                   ["", "bp", "bp", "", "bp", "", "", ""],
                   ["bp", "bp", "bp", "bp", "bp", "", "", ""],
                   ["", "", "", "", "", "", "", ""],
                   ["", "", "", "", "", "", "", ""],
                   ["", "", "", "", "", "", "", ""]]
    available_moves = [(1, 0), (2, 0), (3, 0), (1, 1), (2, 2), (3, 3), (0, 1), (0, 2), (0, 3)]
    moves = board.get_raw_moves((0, 0))
    for move in available_moves:
        assert move in moves
        moves.pop(moves.index(move))
    assert len(moves) == 0

    # bishop moves
    board.state[0][0] = "bb"
    available_moves = [(1, 1), (2, 2), (3, 3)]
    moves = board.get_raw_moves((0, 0))
    for move in available_moves:
        assert move in moves
        moves.pop(moves.index(move))
    assert len(moves) == 0

    # rook moves
    board.state[0][0] = "br"
    available_moves = [(1, 0), (2, 0), (3, 0), (0, 1), (0, 2), (0, 3)]
    moves = board.get_raw_moves((0, 0))
    for move in available_moves:
        assert move in moves
        moves.pop(moves.index(move))
    assert len(moves) == 0

    # knight moves
    board.state[0][0] = "wn"
    available_moves = [(1, 2), (2, 1)]
    moves = board.get_raw_moves((0, 0))
    for move in available_moves:
        assert move in moves
        moves.pop(moves.index(move))
    assert len(moves) == 0


def test_board_get_available_moves():
    pass

def test_board_move_piece():
    pass

def test_board_get_new_state():
    pass

def test_board_is_check():
    pass

def test_board_find_king_position(board):
    board.state = [["" for _ in range(8)] for _ in range(8)]
    print(board.state)
    positions = [(0, 0), (0, 3), (0, 7), (3, 0), (3, 3), (3, 7), (7, 0), (7, 3), (7, 7)]
    colours = ["wk", "bk"]
    for c in colours:
        for pos in positions:
            x, y = pos
            board.state[y][x] = c
            assert board.find_king_position(board.state, (c == "wk")) == pos
            board.state[y][x] = ""
