import random
from collections import namedtuple
import tkinter as tk

# Global Variables: Number of rows, columns and game counter.
game_counter = 0
rows = 100
cols = 100

# init the Graphics window
# Create a Tkinter window
root = tk.Tk()
# Create a Canvas widget to display the matrix
canvas = tk.Canvas(root, width=cols * 10, height=rows * 10)
canvas.pack()


def create_matrix(threshold=0.5):
    matrix = []
    # Possible value for dobutness level.
    doubt_value = [1, 2, 3, 4]
    # define the namedtuple
    Cell = namedtuple('Cell', ['doubt', 'received_rumor', 'received_gen', 'passed_gen', 'num_neighbors', 'temp_doubt',
                               'counter'])

    # Creating a matrix filled with 0.
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.uniform(0, 1) >= threshold:
                # If larger than threshold than the cell is filled human.
                # The doubtness level is assigned.
                row.append(Cell(random.choice(doubt_value), False, 0, 0, 0, 0, 100))
            else:
                row.append(Cell(0, False, 0, 0, 0, 0, 100))
        matrix.append(row)

    return matrix


def choose_first(matrix):
    is_staffed = False
    while not is_staffed:
        row = random.randint(0, 99)
        column = random.randint(0, 99)
        if matrix[row][column] is not None:
            is_staffed = True
            return row, column


def believe_rumor(doubt_level):
    if doubt_level == 1:
        return True
    elif doubt_level == 2:
        if random.uniform(0, 1) >= (1 / 3):
            return True
        else:
            return False
    elif doubt_level == 3:
        if random.uniform(0, 1) < (1 / 3):
            return True
        else:
            return False
    elif doubt_level == 4:
        return False


def define_temp_doubt(doubt):
    if doubt != 1:
        return doubt - 1
    else:
        return 1


def get_rumor(cell):
    # check if cell is not none:
    print("line 77")
    if cell.doubt == 0:
        return cell
    global game_counter
    # check if the neighbor a te the received generation:
    cell = cell._replace(received_gen=game_counter)
    return cell


def spread_to_neighbors(row, column, matrix):
    global game_counter
    print("line 101")
    # spread the rumor to all neighbors while making sure they exist:
    if row > 0:
        matrix[row - 1][column] = get_rumor(matrix[row - 1][column])
        if column > 0:
            matrix[row - 1][column - 1] = get_rumor(matrix[row - 1][column - 1])
            if column < 99:
                matrix[row - 1][column + 1] = get_rumor(matrix[row - 1][column + 1])
        if row < 99:
            matrix[row + 1][column] = get_rumor(matrix[row + 1][column])
            if column > 0:
                matrix[row + 1][column - 1] = get_rumor(matrix[row + 1][column - 1])
                if column < 99:
                    matrix[row + 1][column + 1] = get_rumor(matrix[row - 1][column + 1])
    if column > 0:
        matrix[row][column - 1] = get_rumor(matrix[row][column - 1])
        if column < 99:
            matrix[row][column + 1] = get_rumor(matrix[row][column + 1])

    return matrix


def pass_rumor(matrix, gen_lim):
    # Loop over all the board:
    for i in range(100):
        for j in range(100):
            if matrix[i][j] is not None:
                if matrix[i][j].received_rumor == True:
                    spread_to_neighbors(i, j, matrix)
                # if the cell already spread the rumor + the generation is game_counter-1 + l_counter ==0:
                if matrix[i][j].received_rumor and matrix[i][j].received_gen == game_counter - 1 and matrix[i][
                    j].counter == 0:
                    # check if the cell has a temp doubt:
                    if matrix[i][j].temp_doubt != 0:
                        believe = believe_rumor(matrix[i][j].temp_doubt)
                    else:
                        believe = believe_rumor(matrix[i][j].doubt)
                    # check if the cell believes the rumor, if so- spread to neighbors:
                    if believe:
                        # update L counter:
                        matrix[i][j] = matrix[i][j]._replace(counter=gen_lim)
                        # update the passing generation:
                        matrix[i][j].passed_gen = game_counter

                        matrix = spread_to_neighbors(i, j, matrix)
                if matrix[i][j].counter != 0:
                    # decrement the L counter:
                    matrix[i][j] = matrix[i][j]._replace(counter=matrix[i][j].counter - 1)
                # clear temp doubt if needed:
                if matrix[i][j].temp_doubt != 0 and matrix[i][j].received_gen <= game_counter - 1:
                    matrix[i - 1][j - 1] = matrix[i - 1][j - 1]._replace(temp_doubt=0)


# Define a function to draw a rectangle for each cell
def draw_cell(matrix, i, j, flag=False):
    cell = matrix[i][j]
    if cell.doubt == 1:
        color = '#D5F5FF'
    if cell.doubt == 2:
        color = '#ADD8E6'
    if cell.doubt == 3:
        color = "#87CEEB"
    if cell.doubt == 4:
        color = "#6495ED"
    if cell.received_rumor:
        color = '#006400'
    if cell.doubt == 0:
        color = 'white'
    x1 = j * 10
    y1 = i * 10
    x2 = x1 + 10
    y2 = y1 + 10
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")


def draw_all_cells(matrix, flag=False):
    # Draw all cells on the canvas
    for i in range(rows):
        for j in range(cols):
            draw_cell(matrix, i, j, flag)


# Global variables for the Game flow
gen_lim = 5
matrix = create_matrix()


# Wrapper function that is being called by the button.
def choose_first_wrapper():
    global matrix
    global game_counter
    canvas.delete('all')
    row, column = choose_first(matrix)
    matrix[row][column] = matrix[row][column]._replace(received_rumor=True)
    matrix[row][column] = matrix[row][column]._replace(received_gen=game_counter)
    print(row, column)
    print(matrix[row][column].received_rumor)
    root.update()
    draw_all_cells(matrix, True)
    root.update()


def pass_rumor_wrapper():
    global game_counter
    global matrix
    canvas.delete('all')
    pass_rumor(matrix, gen_lim)
    game_counter += 1
    root.update()
    print('line 198')
    draw_all_cells(matrix, True)
    root.update()


def Game_flow():
    global matrix
    global game_counter
    game_over = False
    # Print the initial matrix before the rumor.
    draw_all_cells(matrix)

    # choose the first player:
    start_button = tk.Button(root, text="Start", command=choose_first_wrapper)
    # start_button.pack()
    start_button.place(x=500, y=1000)

    # pass the rumor:
    next_gen_button = tk.Button(root, text="Next Generation", command=pass_rumor_wrapper)
    # next_gen_button.pack()
    next_gen_button.place(x=500, y=0)


Game_flow()

# Start the Tkinter event loop
root.mainloop()
