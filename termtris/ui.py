import curses, time, math
from .board import Board, W, H
from .storage import add_score
from datetime import datetime

TICK_BASE = 0.6  # base seconds per tick at level 1

def _speed_for_level(level:int)->float:
    # Exponential-ish decay; faster at higher levels
    return max(0.05, TICK_BASE * (0.85 ** (level-1)))

def draw(stdscr, board: Board, start_time, paused):
    stdscr.erase()
    h, w = stdscr.getmaxyx()

    # Borders and labels
    left = 2
    top = 1
    # draw playfield border
    for y in range(H+2):
        stdscr.addstr(top + y, left, "|")
        stdscr.addstr(top + y, left + 2*W + 1, "|")
    for x in range(2*W + 2):
        stdscr.addstr(top, left + x, "-")
        stdscr.addstr(top + H + 1, left + x, "-")
    stdscr.addstr(top-1, left, " TERMTRIS ")

    # draw grid blocks
    for r in range(H):
        for c in range(W):
            if board.grid[r][c]:
                stdscr.addstr(top + 1 + r, left + 1 + 2*c, "[]")

    # draw current piece
    for r, row in enumerate(board.current.cells):
        for c, v in enumerate(row):
            if v:
                y = board.current.y + r
                x = board.current.x + c
                if 0 <= y < H and 0 <= x < W:
                    stdscr.addstr(top + 1 + y, left + 1 + 2*x, "[]")

    # sidebar
    sx = left + 2*W + 6
    stdscr.addstr(top, sx, "Score: {}".format(board.score))
    stdscr.addstr(top+1, sx, "Lines: {}".format(board.lines))
    stdscr.addstr(top+2, sx, "Level: {}".format(board.level))
    elapsed = int(time.time() - start_time)
    stdscr.addstr(top+3, sx, "Time: {}s".format(elapsed))

    stdscr.addstr(top+5, sx, "Next:")
    # draw next piece miniature
    np = board.next_piece
    for r, row in enumerate(np.cells):
        for c, v in enumerate(row):
            if v:
                stdscr.addstr(top+6+r, sx + 2*c, "[]")

    stdscr.addstr(top+11, sx, "Controls:")
    stdscr.addstr(top+12, sx, "←/→ move")
    stdscr.addstr(top+13, sx, "↓ soft drop")
    stdscr.addstr(top+14, sx, "Z/X rotate")
    stdscr.addstr(top+15, sx, "Space hard drop")
    stdscr.addstr(top+16, sx, "P pause | Q quit")

    if paused:
        stdscr.addstr(top + H//2, left + 6, "[PAUSED]")

    if board.game_over:
        stdscr.addstr(top + H//2 - 1, left + 4, "== GAME OVER ==")
        stdscr.addstr(top + H//2, left + 2, "Enter name and press Enter")

    stdscr.refresh()

def run_curses():
    curses.wrapper(_main)

def _main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

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
                if ch in (ord('q'), ord('Q')):
                    break
                elif ch in (ord('p'), ord('P')):
                    paused = not paused
                elif not paused:
                    if ch == curses.KEY_LEFT:
                        board.move(-1, 0)
                    elif ch == curses.KEY_RIGHT:
                        board.move(1, 0)
                    elif ch == curses.KEY_DOWN:
                        board.move(0, 1)
                        board.score += 1  # soft drop bonus
                    elif ch in (ord('z'), ord('Z')):
                        board.rotate_left()
                    elif ch in (ord('x'), ord('X')):
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
