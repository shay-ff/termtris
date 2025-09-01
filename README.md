# termtris

**Terminal Tetris (termtris)** — a CLI game with persistent highscores.

---

## Installation

### 1. Create a Virtual Environment

**macOS / Unix**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install termtris

```bash
pip install .
```

Or run directly (without installing):

```bash
python -m termtris play
```

---

## Usage

### Start the Game

```bash
termtris
```

### Other Commands

```bash
termtris scores   # Show top scores
termtris reset    # Reset highscores
```

---

## Controls

| Key        | Action           |
|------------|------------------|
| Left/Right | Move             |
| Down       | Soft drop        |
| Z / X      | Rotate left/right|
| Space      | Hard drop        |
| P          | Pause            |
| N          | New game         |
| Q          | Quit             |

---

**Scores are stored in your user's config directory:**  
`~/.config/termtris/termtris.db`

# cli-tetris
