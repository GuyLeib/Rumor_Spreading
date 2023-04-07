import random

def create_matrix(threshold = 0.5):
    # Variables: Number of rows, columns.
    rows = 100
    cols = 100
    matrix = []

# Creating a matrix filled with 0.
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(0)
        matrix.append(row)

    for i in range(rows):
        for j in range(cols):
            # Filling the matrix according to the threshold.
            if random.uniform(0, 1) < threshold:
                matrix[i][j] = 0
            else:
                matrix[i][j] = 1

