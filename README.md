# termtris

**Terminal Tetris (termtris)** — a CLI Tetris-like game with persistent highscores.

<img src="images/snapshot.png" width="400" alt="Gameplay snapshot">

---

## Installation

### Recommended (for most users): `pipx` — isolated global CLI install

- Install pipx (if you don't have it):  
  - macOS (Homebrew): `brew install pipx` and then `pipx ensurepath`  
- Install termtris from PyPI:  
  `pipx install termtris`

**Install from TestPyPI (for testing a pre-release on TestPyPI):**  
`pipx install --pip-args="--index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple" termtris`

---

### Alternative: Install into a Virtual Environment (recommended for developers)

**macOS / Linux**  
1. `python3 -m venv .venv`  
2. `source .venv/bin/activate`  
3. `python3 -m pip install --upgrade pip`  
4. `python3 -m pip install termtris`

**Windows**  
1. `python -m venv .venv`  
2. `.venv\Scripts\activate`  
3. `python -m pip install --upgrade pip`  
4. `python -m pip install termtris`

---

### Install directly from TestPyPI (for testing)

`python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple termtris`

---

## If you see `externally-managed-environment` (PEP 668)

Some system Python installations (e.g., Homebrew on macOS, certain Linux distros) prevent `pip` from installing packages into the system site-packages.  
If you hit an error like:

`error: externally-managed-environment`

Recommended fixes (in order):

1. Use **pipx** (best for CLI tools) — shown above.  
2. Use a **virtual environment** — shown above.  
3. Only if you understand the risk: use `--break-system-packages` (not recommended):  
   `python3 -m pip install termtris --break-system-packages`

---

## Quick start / Usage

After installing, run:

- Start the game: `termtris`  
- Or run via module: `python -m termtris play`

### CLI commands

- `termtris` → Start the game  
- `termtris scores` → Show top scores  
- `termtris reset` → Reset highscores  

---

## Controls

| Key        | Action            |
|------------|-------------------|
| A / D      | Move left/right   |
| Left/Right | Move left/right   |
| Down       | Soft drop         |
| Q / E      | Rotate left/right |
| Space      | Hard drop         |
| P          | Pause             |
| X          | Quit              |
| C          | Toggle Colors     |

**Ghost Piece**: The game shows a boundary-style preview (ghost piece) of where the current piece will land, helping you plan your moves. The ghost piece updates automatically when you move or rotate the current piece.

Arrow keys are supported in addition to A/D.  
Colors require a color-capable terminal (`xterm-256color`, Windows terminal with proper support, etc).

---

## Configuration & Data

High scores are stored in the user config directory:  

`~/.config/termtris/termtris.db`

---

## Uninstall

- If installed with pipx: `pipx uninstall termtris`  
- If installed in a virtualenv: deactivate and remove the `.venv` folder  
- If installed with pip globally (not recommended): `python3 -m pip uninstall termtris`

---

## Testing / Development

To install the package locally for development:

1. `git clone https://github.com/shay-ff/termtris.git`  
2. `cd termtris`  
3. `python3 -m venv .venv`  
4. `source .venv/bin/activate`  
5. `python -m pip install -e .`  
6. `python -m termtris play`

---

## Notes

- If you published a test release on TestPyPI, the project page is available at:  
  `https://test.pypi.org/project/termtris/`  
- For a frictionless install experience for end-users, **pipx** is the recommended distribution method for CLI apps.

---

**Have fun!**
