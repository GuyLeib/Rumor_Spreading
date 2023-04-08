import random
from collections import namedtuple

def create_matrix(threshold = 0.5):
    # Variables: Number of rows, columns.
    rows = 100
    cols = 100
    matrix = []

    dobut_value = [1,2,3,4]
    # define the namedtuple
    Cell = namedtuple('Cell', ['doubt', 'recieved_rumor','recieved_gen','passed_gen', 'num_neighbors', 'counter'])

    # Creating a matrix filled with 0.
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.uniform(0, 1) >= threshold:
                # If larger than threshold than the cell is filled human.
                # The doubtness level is assigned.
                row.append(Cell(random.choice(dobut_value), False, 0, 0, 0, 0))
            else: 
                row.append(Cell(0, False, 0, 0, 0, 0)) 
        matrix.append(row)

    return matrix

create_matrix()

def Game_flow():
    create_matrix()
    # choose the first player
    # Graphics 
    # pass the rumor 
    # variable of iterations. 