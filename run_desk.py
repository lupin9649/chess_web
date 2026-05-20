from pathlib import Path
from chess import ChessGame

IMAGE_DIR = Path(__file__).resolve().parent / "chess"

game = ChessGame(IMAGE_DIR)
game.run()