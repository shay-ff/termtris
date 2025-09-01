# Tetromino shapes and rotation helpers
# Matrix representation: list of lists with 0/1, top-left origin
TETROMINOES = {
    'I': [[1,1,1,1]],
    'O': [[1,1],
          [1,1]],
    'T': [[0,1,0],
          [1,1,1]],
    'S': [[0,1,1],
          [1,1,0]],
    'Z': [[1,1,0],
          [0,1,1]],
    'J': [[1,0,0],
          [1,1,1]],
    'L': [[0,0,1],
          [1,1,1]],
}

ORDER = ['I','O','T','S','Z','J','L']

def rotate_clockwise(mat):
    # Transpose + reverse rows
    return [list(row) for row in zip(*mat[::-1])]

def rotate_counterclockwise(mat):
    # Reverse rows + transpose
    return [list(row) for row in zip(*mat)][::-1]
