import curses, time, math
from .board import Board, W, H
from .storage import add_score
from datetime import datetime

TICK_BASE = 0.6  # base seconds per tick at level 1

# Global color toggle state
colors_enabled = True

def _speed_for_level(level:int)->float:
    # Exponential-ish decay; faster at higher levels
    return max(0.05, TICK_BASE * (0.85 ** (level-1)))

def _init_colors():
    if not curses.has_colors():
        return
    curses.start_color()
    curses.use_default_colors()
    # Map tetromino kinds to color pairs
    # 1:I cyan, 2:O yellow, 3:T magenta, 4:S green, 5:Z red, 6:J blue, 7:L orange-ish
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_YELLOW, -1)
    curses.init_pair(3, curses.COLOR_MAGENTA, -1)
    curses.init_pair(4, curses.COLOR_GREEN, -1)
    curses.init_pair(5, curses.COLOR_RED, -1)
    curses.init_pair(6, curses.COLOR_BLUE, -1)
    # Orange may not exist; approximate with yellow or default
    curses.init_pair(7, curses.COLOR_YELLOW, -1)

def _should_use_colors():
    """Check if colors should be used based on global state and terminal capability"""
    return colors_enabled and curses.has_colors()

def _safe_addstr(stdscr, y, x, string, *args):
    """Safely add a string at position, checking bounds first"""
    try:
        h, w = stdscr.getmaxyx()
        if 0 <= y < h and 0 <= x < w and x + len(string) <= w:
            stdscr.addstr(y, x, string, *args)
    except (curses.error, ValueError):
        pass  # Silently ignore drawing errors

def _check_terminal_size(stdscr):
    """Check if terminal is large enough for the game"""
    h, w = stdscr.getmaxyx()
    # Minimum size: height for board + borders + sidebar, width for board + borders + sidebar
    min_h = H + 4  # board + borders + some space
    min_w = 2*W + 20  # board width + borders + sidebar
    return h >= min_h and w >= min_w

KIND_TO_COLOR = {
    'I': 1,
    'O': 2,
    'T': 3,
    'S': 4,
    'Z': 5,
    'J': 6,
    'L': 7,
}

def draw(stdscr, board: Board, start_time, paused):
    stdscr.erase()
    h, w = stdscr.getmaxyx()

    # Check terminal size first
    if not _check_terminal_size(stdscr):
        _safe_addstr(stdscr, h//2, 0, "Terminal too small! Need at least {}x{}".format(2*W + 20, H + 4))
        stdscr.refresh()
        return

    # Borders and labels
    left = 2
    top = 1
    # draw playfield border
    for y in range(H+2):
        _safe_addstr(stdscr, top + y, left, "|")
        _safe_addstr(stdscr, top + y, left + 2*W + 1, "|")
    for x in range(2*W + 2):
        _safe_addstr(stdscr, top, left + x, "-")
        _safe_addstr(stdscr, top + H + 1, left + x, "-")
    _safe_addstr(stdscr, top-1, left, " TERMTRIS ")

    # draw grid blocks (locked cells)
    for r in range(H):
        for c in range(W):
            cell = board.grid[r][c]
            if cell:
                ch_y = top + 1 + r
                ch_x = left + 1 + 2*c
                if isinstance(cell, str) and _should_use_colors():
                    color_pair = curses.color_pair(KIND_TO_COLOR.get(cell, 0))
                    _safe_addstr(stdscr, ch_y, ch_x, "[]", color_pair)
                else:
                    _safe_addstr(stdscr, ch_y, ch_x, "[]")

    # draw current piece
    for r, row in enumerate(board.current.cells):
        for c, v in enumerate(row):
            if v:
                y = board.current.y + r
                x = board.current.x + c
                if 0 <= y < H and 0 <= x < W:
                    ch_y = top + 1 + y
                    ch_x = left + 1 + 2*x
                    if _should_use_colors():
                        color_pair = curses.color_pair(KIND_TO_COLOR.get(board.current.kind, 0))
                        _safe_addstr(stdscr, ch_y, ch_x, "[]", color_pair)
                    else:
                        _safe_addstr(stdscr, ch_y, ch_x, "[]")

    # sidebar
    sx = left + 2*W + 6
    _safe_addstr(stdscr, top, sx, "Score: {}".format(board.score))
    _safe_addstr(stdscr, top+1, sx, "Lines: {}".format(board.lines))
    _safe_addstr(stdscr, top+2, sx, "Level: {}".format(board.level))
    elapsed = int(time.time() - start_time)
    _safe_addstr(stdscr, top+3, sx, "Time: {}s".format(elapsed))

    _safe_addstr(stdscr, top+5, sx, "Next:")
    # draw next piece miniature
    np = board.next_piece
    for r, row in enumerate(np.cells):
        for c, v in enumerate(row):
            if v:
                if _should_use_colors():
                    color_pair = curses.color_pair(KIND_TO_COLOR.get(np.kind, 0))
                    _safe_addstr(stdscr, top+6+r, sx + 2*c, "[]", color_pair)
                else:
                    _safe_addstr(stdscr, top+6+r, sx + 2*c, "[]")

    _safe_addstr(stdscr, top+11, sx, "Controls:")
    _safe_addstr(stdscr, top+12, sx, "A/D move")
    _safe_addstr(stdscr, top+13, sx, "↓ soft drop")
    _safe_addstr(stdscr, top+14, sx, "Q/E rotate")
    _safe_addstr(stdscr, top+15, sx, "Space hard drop")
    _safe_addstr(stdscr, top+16, sx, "P pause | X quit")
    _safe_addstr(stdscr, top+17, sx, "C toggle colors")
    _safe_addstr(stdscr, top+18, sx, "Created by: github/shay-ff")

    # Show current color state
    color_status = "Colors: ON" if _should_use_colors() else "Colors: OFF"
    _safe_addstr(stdscr, top+19, sx, color_status)

    if paused:
        _safe_addstr(stdscr, top + H//2, left + 6, "[PAUSED]")

    if board.game_over:
        _safe_addstr(stdscr, top + H//2 - 1, left + 4, "== GAME OVER ==")
        _safe_addstr(stdscr, top + H//2, left + 2, "Enter name and press Enter")

    stdscr.refresh()

def run_curses():
    curses.wrapper(_main)

def _main(stdscr):
    global colors_enabled
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    _init_colors()

    board = Board()
    start_time = time.time()
    paused = False
    last_tick = time.time()
    delay = _speed_for_level(board.level)
    name_input = ""
    entering_name = False

    while True:
        now = time.time()
        # adjust speed if level changed
        delay = _speed_for_level(board.level)

        # Input
        try:
            ch = stdscr.getch()
        except curses.error:
            ch = -1

        if ch != -1:
            if entering_name:
                if ch in (10, 13):  # Enter
                    duration = time.time() - start_time
                    add_score(name_input.strip() or "PLAYER", board.score, board.lines, board.level, duration)
                    break
                elif ch in (27,):  # ESC to cancel
                    break
                elif ch in (curses.KEY_BACKSPACE, 127, 8):
                    name_input = name_input[:-1]
                elif 32 <= ch <= 126 and len(name_input) < 20:
                    name_input += chr(ch)
            else:
                if ch in (ord('x'), ord('X')):
                    break
                elif ch in (ord('p'), ord('P')):
                    paused = not paused
                elif ch in (ord('c'), ord('C')):
                    colors_enabled = not colors_enabled
                elif not paused:
                    if ch == curses.KEY_LEFT or ch in (ord('a'), ord('A')):
                        board.move(-1, 0)
                    elif ch == curses.KEY_RIGHT or ch in (ord('d'), ord('D')):
                        board.move(1, 0)
                    elif ch == curses.KEY_DOWN:
                        board.move(0, 1)
                        board.score += 1  # soft drop bonus
                    elif ch in (ord('q'), ord('Q')):
                        board.rotate_left()
                    elif ch in (ord('e'), ord('E')):
                        board.rotate_right()
                    elif ch == ord(' '):
                        board.hard_drop()

        if not paused and not board.game_over and (now - last_tick) >= delay:
            board.tick()
            last_tick = now

        if board.game_over and not entering_name:
            entering_name = True
            curses.echo()
            stdscr.nodelay(False)
            stdscr.addstr(0,0,"")  # focus

        draw(stdscr, board, start_time, paused)

        if entering_name:
            stdscr.addstr(2, 2, "Name: " + name_input)
            stdscr.refresh()

        time.sleep(0.01)