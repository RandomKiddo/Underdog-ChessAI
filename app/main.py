from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .get_next_move import get_move
from .startup.load_model import load_chess_model

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.state.chess_model = load_chess_model()

app.include_router(get_move.router)