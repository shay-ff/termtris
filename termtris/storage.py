import sqlite3, os, time, sys
from datetime import datetime
from platformdirs import user_config_dir

APP_NAME = "termtris"
APP_AUTHOR = "termtris"  # generic

def _db_path():
    cfg_dir = user_config_dir(APP_NAME, APP_AUTHOR)
    os.makedirs(cfg_dir, exist_ok=True)
    return os.path.join(cfg_dir, "termtris.db")

def init_db():
    conn = sqlite3.connect(_db_path())
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL,
            lines INTEGER NOT NULL,
            level INTEGER NOT NULL,
            duration REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_score(name: str, score: int, lines: int, level: int, duration: float):
    conn = sqlite3.connect(_db_path())
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO scores (name, score, lines, level, duration, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name[:20] or "PLAYER", int(score), int(lines), int(level), float(duration), datetime.utcnow().isoformat()+"Z"))
    conn.commit()
    conn.close()

def top_scores(limit=10):
    conn = sqlite3.connect(_db_path())
    cur = conn.cursor()
    cur.execute("SELECT name, score, lines, level, duration, created_at FROM scores ORDER BY score DESC, duration ASC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def show_scores(limit=10):
    rows = top_scores(limit)
    if not rows:
        print("No scores yet. Play a game first!")
        return
    print("\n=== Top Scores ===")
    print(f"{'Rank':<6}{'Name':<12}{'Score':>8}{'Lines':>8}{'Level':>8}{'Time(s)':>10}{'When(UTC)':>26}")
    for i, (name, score, lines, level, duration, created_at) in enumerate(rows, 1):
        print(f"{i:<6}{name[:12]:<12}{score:>8}{lines:>8}{level:>8}{duration:>10.1f}{created_at:>26}")
    print("")

def reset_scores():
    path = _db_path()
    if os.path.exists(path):
        os.remove(path)
        print("Highscores reset.")
    else:
        print("No highscores database found.")
    init_db()
