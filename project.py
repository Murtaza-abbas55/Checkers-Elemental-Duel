import pygame
import sys
import numpy as np
import copy

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

BOARD_LIGHT = (240, 217, 181)
BOARD_DARK = (181, 136, 99)
HIGHLIGHT_COLOR = (255, 215, 0)
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
OUTLINE_COLOR = (50, 50, 50)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)


pygame.font.init()
LABEL_FONT = pygame.font.SysFont("arial", 18, bold=True)
KING_FONT = pygame.font.SysFont("arial", 20, bold=True)

ELEMENTS = ['fire', 'water', 'earth', 'air']
ELEMENT_COLORS = {
    'fire': RED,
    'water': BLUE,
    'earth': GREEN,
    'air': YELLOW
}

def elemental_advantage(attacker, defender):
    wins = {
        'fire': ['air'],
        'water': ['fire'],
        'earth': ['water'],
        'air': ['earth']
    }
    if attacker == defender:
        return 0
    elif defender in wins[attacker]:
        return 1
    elif attacker in wins[defender]:
        return -1
    else:
        return 0

class Piece:
    def __init__(self, row, col, color, element, is_king=False):
        self.row = row
        self.col = col
        self.color = color
        self.element = element
        self.is_king = is_king

    def make_king(self):
        self.is_king = True

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - 8
        x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

        pygame.draw.circle(win, OUTLINE_COLOR, (x, y), radius + 3)
        pygame.draw.circle(win, ELEMENT_COLORS[self.element], (x, y), radius)

        label = LABEL_FONT.render(self.element[0].upper(), True, TEXT_COLOR)
        label_rect = label.get_rect(center=(x, y))
        win.blit(label, label_rect)

        if self.is_king:
            king = KING_FONT.render("👑", True, TEXT_COLOR)
            win.blit(king, king.get_rect(center=(x, y - 20)))

        if self.color == BLACK:
            ai_text = LABEL_FONT.render("AI", True, BLACK)
            win.blit(ai_text, ai_text.get_rect(center=(x, y + 20)))

class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row + col) % 2 != 0:
                    if row < 3:
                        element = np.random.choice(ELEMENTS)
                        self.board[row].append(Piece(row, col, BLACK, element))
                    elif row > 4:
                        element = np.random.choice(ELEMENTS)
                        self.board[row].append(Piece(row, col, WHITE, element))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        win.fill(BACKGROUND_COLOR)
        for row in range(ROWS):
            for col in range(COLS):
                color = BOARD_LIGHT if (row + col) % 2 == 0 else BOARD_DARK
                pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if isinstance(piece, Piece):
                    piece.draw(win)

    def get_valid_moves(self, piece):
        moves = {}
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if not piece.is_king:
            directions = directions[:2] if piece.color == WHITE else directions[2:]

        for dx, dy in directions:
            x, y = piece.row + dx, piece.col + dy
            if 0 <= x < ROWS and 0 <= y < COLS:
                target = self.board[x][y]
                if target == 0:
                    moves[(x, y)] = None
                elif isinstance(target, Piece) and target.color != piece.color:
                    if elemental_advantage(piece.element, target.element) >= 0:
                        jump_x, jump_y = x + dx, y + dy
                        if 0 <= jump_x < ROWS and 0 <= jump_y < COLS and self.board[jump_x][jump_y] == 0:
                            moves[(jump_x, jump_y)] = (x, y)
        return moves

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = 0, piece
        piece.row, piece.col = row, col
        if (piece.color == WHITE and row == 0) or (piece.color == BLACK and row == ROWS - 1):
            piece.make_king()

    def remove(self, positions):
        for row, col in positions:
            self.board[row][col] = 0

class Agent:
    def __init__(self, color):
        self.color = color

    def minimax(self, position, depth, alpha, beta, max_player):
        if depth == 0:
            return self.evaluate(position), position

        if max_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_all_moves(position, WHITE):
                evaluation = self.minimax(move, depth-1, alpha, beta, False)[0]
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_all_moves(position, BLACK):
                evaluation = self.minimax(move, depth-1, alpha, beta, True)[0]
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate(self, board):
        white_score, black_score = 0, 0
        for row in board.board:
            for piece in row:
                if isinstance(piece, Piece):
                    score = 2 if piece.is_king else 1
                    element_score = ELEMENTS.index(piece.element)
                    score += element_score * 0.1
                    if piece.color == WHITE:
                        white_score += score
                    else:
                        black_score += score
        return white_score - black_score

    def get_all_moves(self, board, color):
        moves = []
        for row in board.board:
            for piece in row:
                if isinstance(piece, Piece) and piece.color == color:
                    valid_moves = board.get_valid_moves(piece)
                    for move, skipped in valid_moves.items():
                        temp_board = copy.deepcopy(board)
                        temp_piece = temp_board.board[piece.row][piece.col]
                        temp_board.move(temp_piece, move[0], move[1])
                        if skipped:
                            temp_board.remove([skipped])
                        moves.append(temp_board)
        return moves

def draw_game_over(win, message):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    win.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 60)
    text = font.render(message, True, TEXT_COLOR)
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    win.blit(text, rect)

    sub = pygame.font.SysFont(None, 36).render("Closing...", True, GRAY)
    win.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

    pygame.display.update()
    pygame.time.delay(3000)

class Game:
    def __init__(self, win):
        self.win = win
        self.board = Board()
        self.turn = WHITE
        self.selected = None
        self.ai_agent = Agent(BLACK)

    def update(self):
        self.board.draw(self.win)
        if self.selected:
            s = self.selected
            x = s.col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = s.row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(self.win, HIGHLIGHT_COLOR, (x, y), SQUARE_SIZE // 2 - 4, 4)
        pygame.display.update()

    def select(self, row, col):
        piece = self.board.board[row][col]
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        elif piece != 0 and piece.color == self.turn:
            self.selected = piece
            return True
        return False

    def _move(self, row, col):
        piece = self.selected
        valid_moves = self.board.get_valid_moves(piece)
        if (row, col) in valid_moves:
            self.board.move(piece, row, col)
            skipped = valid_moves[(row, col)]
            if skipped:
                self.board.remove([skipped])
            self.change_turn()
            return True
        return False

    def change_turn(self):
        self.selected = None
        self.turn = BLACK if self.turn == WHITE else WHITE

    def check_winner(self):
        white_left = black_left = 0
        white_moves = black_moves = 0

        for row in self.board.board:
            for piece in row:
                if isinstance(piece, Piece):
                    if piece.color == WHITE:
                        white_left += 1
                        if self.board.get_valid_moves(piece):
                            white_moves += 1
                    elif piece.color == BLACK:
                        black_left += 1
                        if self.board.get_valid_moves(piece):
                            black_moves += 1

        if white_left == 0 or white_moves == 0:
            return "AI Wins!"
        elif black_left == 0 or black_moves == 0:
            return "Player Wins!"
        return None

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers: Elemental Duel')
    game = Game(win)

    run = True
    while run:
        game.update()

        winner = game.check_winner()
        if winner:
            draw_game_over(win, f"Game Over: {winner}")
            run = False
            continue

        if game.turn == BLACK:
            pygame.time.delay(500)
            _, new_board = game.ai_agent.minimax(game.board, 3, float('-inf'), float('inf'), False)
            game.board = new_board
            game.change_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and game.turn == WHITE:
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                game.select(row, col)

if __name__ == '__main__':
    main()
