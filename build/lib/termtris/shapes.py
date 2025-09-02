import sys
# Tetromino shapes and rotation helpers
# Matrix representation: list of lists with colored blocks (ANSI codes), top-left origin

# ANSI color codes for each tetromino
COLORS = {
    'I': '\033[36m',   # Cyan
    'O': '\033[33m',   # Yellow
    'T': '\033[35m',   # Magenta
    'S': '\033[32m',   # Green
    'Z': '\033[31m',   # Red
    'J': '\033[34m',   # Blue
    'L': '\033[38;5;208m', # Orange (extended)
}

RESET = '\033[0m'
BLOCK = '█'

def colored_block(shape):
    return COLORS[shape] + BLOCK + RESET

TETROMINOES = {
    'I': [[colored_block('I')]*4],
    'O': [[colored_block('O')]*2,
          [colored_block('O')]*2],
    'T': [[None, colored_block('T'), None],
          [colored_block('T')]*3],
    'S': [[None, colored_block('S'), colored_block('S')],
          [colored_block('S'), colored_block('S'), None]],
    'Z': [[colored_block('Z'), colored_block('Z'), None],
          [None, colored_block('Z'), colored_block('Z')]],
    'J': [[colored_block('J'), None, None],
          [colored_block('J')]*3],
    'L': [[None, None, colored_block('L')],
          [colored_block('L')]*3],
}

ORDER = ['I','O','T','S','Z','J','L']

def rotate_clockwise(mat):
      # Transpose + reverse rows
      return [list(row) for row in zip(*mat[::-1])]

def rotate_counterclockwise(mat):
      # Reverse rows + transpose
      return [list(row) for row in zip(*mat)][::-1]
