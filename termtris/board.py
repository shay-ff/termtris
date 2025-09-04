import random
from .shapes import TETROMINOES, ORDER, rotate_clockwise, rotate_counterclockwise

W, H = 10, 20  # standard playfield

class Piece:
    def __init__(self, kind):
        self.kind = kind
        self.cells = [row[:] for row in TETROMINOES[kind]]
        self.x = W//2 - len(self.cells[0])//2
        self.y = 0

    def rotate_left(self):
        self.cells = rotate_counterclockwise(self.cells)

    def rotate_right(self):
        self.cells = rotate_clockwise(self.cells)

class Bag:
    # 7-bag randomizer
    def __init__(self):
        self.bag = []

    def next(self):
        if not self.bag:
            self.bag = ORDER[:]
            random.shuffle(self.bag)
        kind = self.bag.pop()
        return Piece(kind)

class Board:
    def __init__(self):
        self.grid = [[0]*W for _ in range(H)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.bag = Bag()
        self.current = self.bag.next()
        self.hold_used = False
        self.game_over = False
        self.next_piece = self.bag.next()

    def clone_grid(self):
        return [row[:] for row in self.grid]

    def can_place(self, piece, ox=None, oy=None):
        if ox is None: ox = piece.x
        if oy is None: oy = piece.y
        for r, row in enumerate(piece.cells):
            for c, v in enumerate(row):
                if not v: continue
                x, y = ox + c, oy + r
                if x < 0 or x >= W or y < 0 or y >= H: 
                    return False
                if self.grid[y][x]: 
                    return False
        return True

    def lock_piece(self):
        # Merge into grid
        for r, row in enumerate(self.current.cells):
            for c, v in enumerate(row):
                if v:
                    x, y = self.current.x + c, self.current.y + r
                    if 0 <= y < H and 0 <= x < W:
                        # Store the piece kind so UI can color locked cells
                        self.grid[y][x] = self.current.kind
        # Clear lines
        cleared = 0
        new_grid = [row for row in self.grid if any(v == 0 for v in row)]
        cleared = H - len(new_grid)
        for _ in range(cleared):
            new_grid.insert(0, [0]*W)
        self.grid = new_grid
        # Scoring (simple Tetris guideline-ish)
        scores = {0:0, 1:100, 2:300, 3:500, 4:800}
        self.score += scores.get(cleared, 0) * self.level
        self.lines += cleared
        self.level = 1 + self.lines // 10
        # Next piece
        self.current = self.next_piece
        self.next_piece = self.bag.next()
        # If cannot place new current -> game over
        if not self.can_place(self.current):
            self.game_over = True

    def move(self, dx, dy):
        nx, ny = self.current.x + dx, self.current.y + dy
        if self.can_place(self.current, nx, ny):
            self.current.x, self.current.y = nx, ny
            return True
        return False

    def rotate_left(self):
        old = [row[:] for row in self.current.cells]
        self.current.rotate_left()
        if not self.can_place(self.current):
            # wall kick attempts (simple)
            for kick in (-1, 1, -2, 2):
                if self.can_place(self.current, self.current.x + kick, self.current.y):
                    self.current.x += kick
                    return True
            self.current.cells = old
            return False
        return True

    def rotate_right(self):
        old = [row[:] for row in self.current.cells]
        self.current.rotate_right()
        if not self.can_place(self.current):
            for kick in (-1, 1, -2, 2):
                if self.can_place(self.current, self.current.x + kick, self.current.y):
                    self.current.x += kick
                    return True
            self.current.cells = old
            return False
        return True

    def hard_drop(self):
        dist = 0
        while self.move(0,1):
            dist += 1
        # Soft drop bonus for each row fallen on hard drop
        self.score += 2 * dist
        self.lock_piece()

    def get_ghost_position(self):
        """Calculate where the current piece will land (ghost piece position)"""
        ghost_y = self.current.y
        # Drop the piece down until it can't move further
        while self.can_place(self.current, self.current.x, ghost_y + 1):
            ghost_y += 1
        return self.current.x, ghost_y

    def tick(self):
        if not self.move(0,1):
            self.lock_piece()
