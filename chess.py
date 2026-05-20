import pygame
from pathlib import Path

WIDTH = 640
HEIGHT = 640
ROWS = 8
COLS = 8
TILE_SIZE = WIDTH // COLS
FPS = 60

LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)
SELECTED_COLOR = (50, 180, 50)
MOVE_COLOR = (60, 60, 60)


class Piece:
    def __init__(self, color, row, col, image, directions=None):
        self.__color = color
        self.__row = row
        self.__col = col
        self.__image = image
        self.__directions = directions if directions is not None else []

    @property
    def color(self):
        return self.__color

    @property
    def row(self):
        return self.__row

    @property
    def col(self):
        return self.__col

    @property
    def image(self):
        return self.__image

    def move(self, row, col):
        self.__row = row
        self.__col = col

    def draw(self, screen):
        x = self.__col * TILE_SIZE
        y = self.__row * TILE_SIZE
        screen.blit(self.__image, (x, y))

    def get_moves(self, board):
        return self.__get_line_moves(board)

    def __get_line_moves(self, board):
        moves = []

        for dr, dc in self.__directions:
            row = self.row + dr
            col = self.col + dc

            while board.is_inside(row, col):
                target = board.get_piece(row, col)

                if target is None:
                    moves.append((row, col))
                else:
                    if target.color != self.color:
                        moves.append((row, col))
                    break

                row += dr
                col += dc

        return moves


class Pawn(Piece):
    def __init__(self, color, row, col, image):
        super().__init__(color, row, col, image)

    def get_moves(self, board):
        moves = []
        direction = -1 if self.color == "w" else 1
        start_row = 6 if self.color == "w" else 1

        next_row = self.row + direction
        if board.is_inside(next_row, self.col) and board.get_piece(next_row, self.col) is None:
            moves.append((next_row, self.col))

            two_step_row = self.row + 2 * direction
            if self.row == start_row and board.get_piece(two_step_row, self.col) is None:
                moves.append((two_step_row, self.col))

        for dc in [-1, 1]:
            new_row = self.row + direction
            new_col = self.col + dc

            if board.is_inside(new_row, new_col):
                target = board.get_piece(new_row, new_col)
                if target is not None and target.color != self.color:
                    moves.append((new_row, new_col))

        return moves


class Rook(Piece):
    def __init__(self, color, row, col, image):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        super().__init__(color, row, col, image, directions)


class Bishop(Piece):
    def __init__(self, color, row, col, image):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        super().__init__(color, row, col, image, directions)


class Queen(Piece):
    def __init__(self, color, row, col, image):
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        super().__init__(color, row, col, image, directions)


class Knight(Piece):
    def __init__(self, color, row, col, image):
        super().__init__(color, row, col, image)

    def get_moves(self, board):
        moves = []
        steps = [
            (-2, -1), (-2, 1), (2, -1), (2, 1),
            (-1, -2), (-1, 2), (1, -2), (1, 2)
        ]

        for dr, dc in steps:
            new_row = self.row + dr
            new_col = self.col + dc

            if board.is_inside(new_row, new_col):
                target = board.get_piece(new_row, new_col)
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))

        return moves


class King(Piece):
    def __init__(self, color, row, col, image):
        super().__init__(color, row, col, image)

    def get_moves(self, board):
        moves = []

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                new_row = self.row + dr
                new_col = self.col + dc

                if board.is_inside(new_row, new_col):
                    target = board.get_piece(new_row, new_col)
                    if target is None or target.color != self.color:
                        moves.append((new_row, new_col))

        return moves


class Board:
    def __init__(self, images):
        self.__images = images
        self.__grid = [[None for _ in range(8)] for _ in range(8)]
        self.__setup_board()

    @property
    def grid(self):
        return self.__grid

    def __create_piece(self, code, color, row, col):
        image = self.__images[f"{color}{code}"]

        if code == "P":
            return Pawn(color, row, col, image)
        elif code == "R":
            return Rook(color, row, col, image)
        elif code == "N":
            return Knight(color, row, col, image)
        elif code == "B":
            return Bishop(color, row, col, image)
        elif code == "Q":
            return Queen(color, row, col, image)
        elif code == "K":
            return King(color, row, col, image)

    def __setup_board(self):
        order = ["R", "N", "B", "Q", "K", "B", "N", "R"]

        for col in range(8):
            self.__grid[0][col] = self.__create_piece(order[col], "b", 0, col)
            self.__grid[1][col] = self.__create_piece("P", "b", 1, col)
            self.__grid[6][col] = self.__create_piece("P", "w", 6, col)
            self.__grid[7][col] = self.__create_piece(order[col], "w", 7, col)

    def is_inside(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row, col):
        if self.is_inside(row, col):
            return self.__grid[row][col]
        return None

    def move_piece(self, piece, new_row, new_col):
        self.__grid[piece.row][piece.col] = None
        piece.move(new_row, new_col)
        self.__grid[new_row][new_col] = piece

    def draw(self, screen):
        for row in range(8):
            for col in range(8):
                piece = self.__grid[row][col]
                if piece is not None:
                    piece.draw(screen)


class ChessGame:
    def __init__(self, image_dir):
        pygame.init()

        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Mini Chess")
        self.__clock = pygame.time.Clock()
        self.__running = True

        self.__image_dir = Path(image_dir)
        self.__images = self.__load_images()
        self.__board = Board(self.__images)

        self.__selected_piece = None
        self.__valid_moves = []
        self.__turn = "w"

    @property
    def board(self):
        return self.__board

    @property
    def turn(self):
        return self.__turn

    @property
    def is_running(self):
        return self.__running

    def __load_images(self):
        images = {}

        for color in ["w", "b"]:
            for code in ["K", "Q", "B", "N", "R", "P"]:
                name = f"{color}{code}"
                path = self.__image_dir / f"{name}.png"
                image = pygame.image.load(str(path))
                images[name] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

        return images

    def __draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.__screen, color, rect)

    def __draw_highlights(self):
        if self.__selected_piece is not None:
            rect = pygame.Rect(
                self.__selected_piece.col * TILE_SIZE,
                self.__selected_piece.row * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
            pygame.draw.rect(self.__screen, SELECTED_COLOR, rect, 4)

        for row, col in self.__valid_moves:
            center = (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2)
            pygame.draw.circle(self.__screen, MOVE_COLOR, center, 10)

    def __handle_click(self, pos):
        col = pos[0] // TILE_SIZE
        row = pos[1] // TILE_SIZE

        if not self.__board.is_inside(row, col):
            return

        clicked_piece = self.__board.get_piece(row, col)

        if self.__selected_piece is None:
            if clicked_piece is not None and clicked_piece.color == self.__turn:
                self.__selected_piece = clicked_piece
                self.__valid_moves = clicked_piece.get_moves(self.__board)
        else:
            if (row, col) in self.__valid_moves:
                self.__board.move_piece(self.__selected_piece, row, col)
                self.__turn = "b" if self.__turn == "w" else "w"

            self.__selected_piece = None
            self.__valid_moves = []

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.__handle_click(event.pos)

    def __draw(self):
        self.__draw_board()
        self.__draw_highlights()
        self.__board.draw(self.__screen)
        pygame.display.update()


    def tick(self):
        self.__clock.tick(FPS)
        self.__handle_events()
        self.__draw()



    def shutdown(self):
        pygame.quit()

    def run(self):
         while self.__running:
            self.tick()
         self.shutdown()
