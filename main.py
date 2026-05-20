import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from chess import ChessGame

async def main():
    image_dir = Path(__file__).resolve().parent / "chess"
    game = ChessGame(image_dir)

    while game.is_running():
        game.tick()
        await asyncio.sleep(0)

    game.shutdown()

asyncio.run(main())