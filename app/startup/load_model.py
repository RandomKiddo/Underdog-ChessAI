import keras

def load_chess_model() -> keras.models.Model:
    chess_engine = keras.models.load_model('models/chess_model.keras')

    return chess_engine