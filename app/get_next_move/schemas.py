from pydantic import BaseModel

class ChessRequest(BaseModel):
    fen_representation: str

class ChessResponse(BaseModel):
    fen_representation: str

