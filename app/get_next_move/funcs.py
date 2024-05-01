import numpy as np
import chess
import keras
from typing import Any

board_positions = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7
}

def square_to_index(square: int) -> tuple:
    letter = chess.square_name(square)
    return 8 - int(letter[1]), board_positions[letter[0]]

def board_to_mtx(board: Any) -> Any:
    board_3d = np.zeros((14, 8, 8), dtype=np.int8)

    for i in chess.PIECE_TYPES:
        for ii in board.pieces(i, chess.WHITE):
            idx = np.unravel_index(ii, (8, 8))
            board_3d[i-1][7-idx[0]][idx[1]] = 1
        for ii in board.pieces(i, chess.BLACK):
            idx = np.unravel_index(ii, (8, 8))
            board_3d[i+5][7-idx[0]][idx[1]] = 1

    aux = board.turn
    board.turn = chess.WHITE
    for i in board.legal_moves:
        i, j = square_to_index(i.to_square)
        board_3d[12][i][j] = 1

    board.turn = chess.BLACK
    for i in board.legal_moves:
        i, j = square_to_index(i.to_square)
        board_3d[13][i][j] = 1
    board.turn = aux

    return board_3d

def minimax_evaluate(board: Any, chess_model: keras.models.Model) -> float:
    board_3d = board_to_mtx(board)
    board_3d = np.expand_dims(board_3d, 0)
    return chess_model.predict(board_3d)[0][0]

def minimax(board: Any, depth: int, alpha: float, beta: float, max_player: bool,
            chess_model: keras.models.Model) -> float:
    if depth == 0 or board.is_game_over():
        return minimax_evaluate(board, chess_model)

    if max_player:
        max_eval = -np.inf
        for i in board.legal_moves:
            board.push(i)
            evaluation = minimax(board, depth - 1, alpha, beta, False, chess_model)
            board.pop()
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = np.inf
        for i in board.legal_moves:
            board.push(i)
            evaluation = minimax(board, depth - 1, alpha, beta, True, chess_model)
            board.pop()
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval

def next_move(board: Any, depth: int, chess_model: keras.models.Model) -> chess.Move:
    max_move = None
    max_eval = -np.inf

    for i in board.legal_moves:
        board.push(i)
        evaluation = minimax(board, depth - 1, -np.inf, np.inf, False, chess_model)
        board.pop()
        if evaluation > max_eval:
            max_eval = evaluation
            max_move = i

    return max_move