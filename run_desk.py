from pathlib import Path
from web.chess import ChessGame

IMAGE_DIR = Path(__file__).resolve().parent / "web" / "chess"

game = ChessGame(IMAGE_DIR)
game.run()