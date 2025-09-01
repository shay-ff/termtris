import argparse
from .ui import run_curses
from .storage import init_db, show_scores, reset_scores

def main():
    parser = argparse.ArgumentParser(prog="termtris", description="Terminal Tetris (curses) with persistent highscores.")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("play", help="start the game")
    sub.add_parser("scores", help="show top scores")
    sub.add_parser("reset", help="reset highscores")
    args = parser.parse_args()

    init_db()

    if args.cmd in (None, "play"):
        run_curses()
    elif args.cmd == "scores":
        show_scores()
    elif args.cmd == "reset":
        reset_scores()
