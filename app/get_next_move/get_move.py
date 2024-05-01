from fastapi import APIRouter, Request

from .schemas import ChessRequest, ChessResponse
from .funcs import next_move

router = APIRouter(
    prefix='/chess'
)

@router.post('/move')
async def get_chess_move(request: Request, chess_request: ChessRequest):
    chess_model = request.app.state.chess_model

    board = chess_request.fen_representation

    move = next_move(board, 1, chess_model)

    chess_move = move

    return ChessResponse(fen_representation=chess_move)