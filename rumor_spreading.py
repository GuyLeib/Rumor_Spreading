import random
from collections import namedtuple
import tkinter as tk
import math
from tkinter import messagebox
from decimal import Decimal
from tkinter import simpledialog

# Global Variables: Number of rows, columns and game counter.
game_counter = 0
gen_lim = 5
threshold = 0.5
s1 = 0.25
s2 = 0.25
s3 = 0.25
s4 = 0.25
rows = 100
cols = 100
matrix = []
strategy = 'normal'


# This function create a matrix for the normal setting of the game
def create_matrix():
    global threshold, s1, s2, s3, s4
    global matrix
    matrix = []
    # Possible value for doubtness level.
    doubt_value = [1, 2, 3, 4]
    # define the namedtuple
    Cell = namedtuple('Cell', ['doubt', 'received_rumor', 'received_gen', 'passed_gen', 'num_neighbors', 'temp_doubt',
                               'counter'])

    # Creating a matrix filled with cells
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.uniform(0, 1) <= threshold:
                # If larger than threshold than the cell is filled human.
                # The doubtness level is assigned according to the specified percentages
                rand = random.uniform(0, 1)
                if rand <= s1:
                    row.append(Cell(1, False, 0, 0, 0, 0, 0))
                elif rand <= s1 + s2:
                    row.append(Cell(2, False, 0, 0, 0, 0, 0))
                elif rand <= s1 + s2 + s3:
                    row.append(Cell(3, False, 0, 0, 0, 0, 0))
                else:
                    row.append(Cell(4, False, 0, 0, 0, 0, 0))
            else:
                row.append(Cell(0, False, 0, 0, 0, 0, 0))
        matrix.append(row)

    return matrix


# This function will create a matrix fot the fast strategy of the game
def max_neighbors():
    global threshold, s1, s2, s3, s4, gen_lim
    fast_matrix = []
    neighbor_matrix = []
    # define the namedtuple
    Cell = namedtuple('Cell', ['doubt', 'received_rumor', 'received_gen', 'passed_gen', 'num_neighbors', 'temp_doubt',
                               'counter'])

    # Creating a matrix filled with cells
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.uniform(0, 1) <= threshold:
                row.append(Cell(-1, False, 0, 0, 0, 0, 0))
            else:
                row.append(Cell(0, False, 0, 0, 0, 0, 0))

        fast_matrix.append(row)
    s4_list = []
    for i in range(rows):
        neighbor_row = []
        for j in range(cols):
            if fast_matrix[i][j].doubt == -1:
                neighbors = get_neighbors(fast_matrix, i, j)
                neighbors_to_add = [(ni, nj) for ni, nj in neighbors if (fast_matrix[ni][nj].doubt != 0)]
                if not neighbors_to_add:
                    # assigning s4 to people without neighbors
                    s4_list.append((i, j))
                neighbor_row.append(neighbors_to_add)
            else:
                neighbor_row.append([])
        neighbor_matrix.append(neighbor_row)

    num_humans = sum(cell.doubt == -1 for row in fast_matrix for cell in row)
    num_of_missing_humans = sum(cell.doubt == 0 for row in fast_matrix for cell in row)

    num_s1 = math.ceil(s1 * num_humans)
    num_s2 = math.ceil(s2 * num_humans)
    num_s3 = math.ceil(s3 * num_humans)
    num_s4 = num_humans - num_s1 - num_s2 - num_s3

    # Flatten the neighbor matrix into a list of tuples
    neighbor_list = [(i, j, len(neighbor_matrix[i][j])) for i in range(rows) for j in range(cols)]
    # Sort the list based on the number of neighbors in descending order
    sorted_neighbors = sorted(neighbor_list, key=lambda x: x[2], reverse=True)
    # Extract only the cell indices from the sorted list
    highest_neighbors = [(i, j) for i, j, _ in sorted_neighbors]

    # First assign the s4 to the human without any neighbors.
    for i, j in s4_list:
        if num_s4 > 0:
            fast_matrix[i][j] = fast_matrix[i][j]._replace(doubt=4)
            num_s4 -= 1
            continue
        if num_s3 > 0:
            fast_matrix[i][j] = fast_matrix[i][j]._replace(doubt=3)
            num_s3 -= 1
            continue
        if num_s2 > 0:
            fast_matrix[i][j] = fast_matrix[i][j]._replace(doubt=2)
            num_s2 -= 1
            continue
        if num_s1 > 0:
            fast_matrix[i][j] = fast_matrix[i][j]._replace(doubt=1)
            num_s1 -= 1
            continue

    for i, j in highest_neighbors:
        if num_s1 > 0:
            fast_matrix[i][j] = fast_matrix[i][j]._replace(doubt=1)
            num_s1 -= 1
            continue
        if num_s2 > 0:
            fast_matrix[i][j] = fast_matrix[i][j]._replace(doubt=2)
            num_s2 -= 1
            continue
        if num_s3 > 0:
            fast_matrix[i][j] = fast_matrix[i][j]._replace(doubt=3)
            num_s3 -= 1
            continue
        if num_s4 > 0:
            fast_matrix[i][j] = fast_matrix[i][j]._replace(doubt=4)
            num_s4 -= 1
            continue
    return fast_matrix


# An helper function to get the neighbors of a cell in the matrix.
def get_neighbors(matrix, i, j):
    global rows, cols
    neighbors = []
    for di, dj in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            neighbors.append((ni, nj))
    return neighbors


# This function will create a matrix for the slow strategy
def slow_create_matrix():
    global threshold, s1, s2, s3, s4, gen_lim
    global matrix
    matrix = []
    # define the namedtuple
    Cell = namedtuple('Cell', ['doubt', 'received_rumor', 'received_gen', 'passed_gen', 'num_neighbors', 'temp_doubt',
                               'counter'])
    total_pop = 0
    # Creating a matrix filled with cells
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.uniform(0, 1) <= threshold:
                # If larger than threshold than the cell is filled human.
                # The doubtness level is assigned according to the specified percentages
                row.append(Cell(5, False, 0, 0, 0, 0, 0))
                total_pop += 1
            else:
                row.append(Cell(0, False, 0, 0, 0, 0, 0))
        matrix.append(row)

    s1_count = int(s1 * total_pop)
    s2_count = int(s2 * total_pop)
    s3_count = int(s3 * total_pop)
    s4_count = int(s4 * total_pop)
    s1_prop = int(s1 * 10)
    s2_prop = int(s2 * 10)
    s3_prop = int(s3 * 10)
    s4_prop = int(s4 * 10)

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j].doubt == 5:
                if i == 0 or i % 10 < s1_prop:
                    if s1_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=1)
                        s1_count -= 1
                        continue
                    elif s4_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=4)
                        s4_count -= 1
                        continue
                    elif s2_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=2)
                        s2_count -= 1
                        continue
                    elif s3_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=3)
                        s3_count -= 1
                        continue
                    else:
                        matrix[i][j] = matrix[i][j]._replace(doubt=0)
                        continue
                elif i % 10 < s4_prop + s1_prop:
                    if s4_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=4)
                        s4_count -= 1
                        continue
                    elif s3_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=3)
                        s3_count -= 1
                        continue
                    elif s2_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=2)
                        s2_count -= 1
                        continue
                    elif s1_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=1)
                        s1_count -= 1
                        continue
                    else:
                        matrix[i][j] = matrix[i][j]._replace(doubt=0)
                        continue
                elif i % 10 < s4_prop + s1_prop + s2_prop:
                    if s2_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=2)
                        s2_count -= 1
                        continue
                    elif s4_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=4)
                        s4_count -= 1
                        continue
                    elif s3_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=3)
                        s3_count -= 1
                        continue
                    elif s1_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=1)
                        s1_count -= 1
                        continue
                    else:
                        matrix[i][j] = matrix[i][j]._replace(doubt=0)
                        continue
                elif i % 10 < s4_prop + s1_prop + s2_prop + s3_prop:
                    if s3_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=3)
                        s3_count -= 1
                        continue
                    elif s4_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=4)
                        s4_count -= 1
                        continue
                    elif s2_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=2)
                        s2_count -= 1
                        continue

                    elif s1_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=1)
                        s1_count -= 1
                        continue
                    else:
                        matrix[i][j] = matrix[i][j]._replace(doubt=0)
                        continue
                else:
                    if s4_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=4)
                        s4_count -= 1
                        continue
                    elif s3_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=3)
                        s3_count -= 1
                        continue
                    elif s2_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=2)
                        s2_count -= 1
                        continue
                    elif s1_count > 0:
                        matrix[i][j] = matrix[i][j]._replace(doubt=1)
                        s1_count -= 1
                        continue
    sum = 0
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j].doubt == 5:
                sum += 1
    print("5 doubt: ", sum)
    return matrix


def choose_first():
    global matrix
    while True:
        row = random.randint(0, 99)
        column = random.randint(0, 99)
        if matrix[row][column].doubt != 0:
            matrix[row][column] = matrix[row][column]._replace(received_rumor=True)
            matrix[row][column] = matrix[row][column]._replace(received_gen=game_counter)
            return


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
    global game_counter
    # check if cell is not none:
    if cell.doubt == 0:
        return cell
    if not cell.received_rumor:
        # Update the cell
        cell = cell._replace(received_gen=game_counter)
        cell = cell._replace(received_rumor=True)
        cell = cell._replace(num_neighbors=1)
    else:
        if cell.received_gen != game_counter:
            cell = cell._replace(num_neighbors=1)
        else:
            new_num_neigh = cell.num_neighbors + 1
            cell = cell._replace(num_neighbors=new_num_neigh)
        if cell.num_neighbors >= 2 and cell.received_gen == game_counter:
            # update temp_doubt:
            cell = cell._replace(temp_doubt=define_temp_doubt(cell.doubt))
    return cell


def spread_to_neighbors(row, column):
    global matrix
    global game_counter
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
                    matrix[row + 1][column + 1] = get_rumor(matrix[row + 1][column + 1])
    if column > 0:
        matrix[row][column - 1] = get_rumor(matrix[row][column - 1])
        if column < 99:
            matrix[row][column + 1] = get_rumor(matrix[row][column + 1])


def pass_rumor():
    global matrix
    global gen_lim
    global game_counter
    # Loop over all the board:
    for i in range(100):
        for j in range(100):
            if matrix[i][j].doubt != 0:
                if matrix[i][j].received_rumor:
                    # Condition for the first one to pass the rumor.
                    if matrix[i][j].received_gen == game_counter and game_counter == 0:
                        believe = True
                        if believe:
                            spread_to_neighbors(i, j)
                            # update L counter:
                            matrix[i][j] = matrix[i][j]._replace(counter=gen_lim)
                            return
                        # if the cell already spread the rumor + the generation is game_counter-1 + l_counter ==0:
                    if matrix[i][j].received_gen == game_counter - 1 and matrix[i][j].counter == 0:
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
                            matrix[i][j] = matrix[i][j]._replace(passed_gen=game_counter)
                            # Spread the rumor to neighbors
                            spread_to_neighbors(i, j)

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
        color = '#ce97bd'
    if cell.doubt == 2:
        color = '#add1f5'
    if cell.doubt == 3:
        color = "#bae6af"
    if cell.doubt == 4:
        color = "#f3d997"
    if cell.received_rumor:
        color = 'black'
    if cell.doubt == 0:
        color = 'white'
    x1 = j * 6
    y1 = i * 6
    x2 = x1 + 6
    y2 = y1 + 6
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")


def draw_all_cells(matrix, flag=False):
    # Draw all cells on the canvas
    for i in range(rows):
        for j in range(cols):
            draw_cell(matrix, i, j, flag)


# Wrapper function that is being called by the button.
def choose_first_wrapper():
    global matrix
    global game_counter
    canvas.delete('all')
    choose_first()
    root.update()
    draw_all_cells(matrix, True)
    root.update()


def pass_rumor_wrapper():
    global game_counter
    global matrix
    global stats_label
    canvas.delete('all')
    pass_rumor()
    game_counter += 1
    root.update()
    draw_all_cells(matrix, True)
    gen, counter, per = get_stats()
    per = "{:.1f}".format(per)
    stats_label.config(
        text="Generation {}: {} people knows the rumor - {} percent of the population".format(gen, counter, per),
        font=("Comic Sans MS", 8,'bold'), bg='black', fg='white', relief='ridge')
    root.update()


def pass_30_gens():
    global game_counter
    global matrix
    global stats_label
    canvas.delete('all')
    for i in range(0, 30):
        pass_rumor()
        game_counter += 1
    root.update()
    draw_all_cells(matrix, True)
    gen, counter, per = get_stats()
    per = "{:.1f}".format(per)
    stats_label.config(
        text="Generation {}: {} people knows the rumor - {} percent of the population".format(gen, counter, per),
        font=("Comic Sans MS", 8,'bold'), bg='black', fg='white', relief='ridge')
    root.update()


# Prints the number of people knows the rumor in each iteration
def get_stats():
    global game_counter
    global matrix
    num_humans = sum(cell.doubt != 0 for row in matrix for cell in row)
    # How many new believers for each iteration
    counter = 0
    for i in range(100):
        for j in range(100):
            if matrix[i][j].received_rumor:
                counter += 1
    # calc the percent of the population that know the rumor
    percent = (counter / num_humans) * 100
    return game_counter, counter, percent


def validate_float(input):
    try:
        value = float(input)
        if 0 <= value <= 1:
            return True
        else:
            return False
    except ValueError:
        return False


# Global variables for the Game flow
matrix = create_matrix()


# This function will get the desired configuration from the user.
def get_user_input():
    global threshold, gen_lim, s1, s2, s3, s4, matrix, strategy

    # Create a new Toplevel window
    user_input_window = tk.Toplevel()
    user_input_window.geometry('400x600')  # Set window size

    # Create a label widget for the title
    title_label = tk.Label(user_input_window, text="Enter new configuration", font=("Comic Sans MS", 18))
    title_label.pack(pady=10)  # Add some padding

    # Create input fields for threshold, gen_lim, and var3
    threshold_label = tk.Label(user_input_window, text="Enter the desired population density: (0-1)",
                               font=("Comic Sans MS", 8))
    threshold_label.pack(pady=10)
    threshold_entry = tk.Entry(user_input_window)
    threshold_entry.pack(pady=5)

    gen_lim_label = tk.Label(user_input_window, text="Enter the generation limitation of spreading rumor: (integer)",
                             font=("Comic Sans MS", 8))
    gen_lim_label.pack(pady=10)
    gen_lim_entry = tk.Entry(user_input_window)
    gen_lim_entry.pack(pady=5)

    s1_label = tk.Label(user_input_window, text="Enter the percentage of s1 people: (0-1)", font=("Comic Sans MS", 8))
    s1_label.pack(pady=10)
    s1_entry = tk.Entry(user_input_window)
    s1_entry.pack(pady=5)

    s2_label = tk.Label(user_input_window, text="Enter the percentage of s2 people: (0-1)", font=("Comic Sans MS", 8))
    s2_label.pack(pady=10)
    s2_entry = tk.Entry(user_input_window)
    s2_entry.pack(pady=5)

    s3_label = tk.Label(user_input_window, text="Enter the percentage of s3 people: (0-1)", font=("Comic Sans MS", 8))
    s3_label.pack(pady=10)
    s3_entry = tk.Entry(user_input_window)
    s3_entry.pack(pady=5)

    s4_label = tk.Label(user_input_window, text="Enter the percentage of s4 people: (0-1)", font=("Comic Sans MS", 8))
    s4_label.pack(pady=10)
    s4_entry = tk.Entry(user_input_window)
    s4_entry.pack(pady=5)

    strategy_label = tk.Label(user_input_window, text="Enter the game strategy: normal, fast or slow",
                              font=("Comic Sans MS", 8))
    strategy_label.pack(pady=10)
    strategy_entry = tk.Entry(user_input_window)
    strategy_entry.pack(pady=5)

    # Create a button to submit the user input
    submit_button = tk.Button(user_input_window, text="Submit",
                              command=lambda: submit_user_input(user_input_window, threshold_entry, gen_lim_entry,
                                                                s1_entry, s2_entry, s3_entry, s4_entry, strategy_entry))
    submit_button.pack(pady=10, padx=10, side="bottom")


def submit_user_input(window, threshold_entry, gen_lim_entry, s1_entry, s2_entry, s3_entry, s4_entry, strategy_entry):
    global threshold, gen_lim, s1, s2, s3, s4, matrix, strategy
    global welcome, config_label, lim_label, pop_label, s1_label, s2_label, s3_label, s4_label, strategy_label

    # Get user input values
    try:
        threshold = float(threshold_entry.get())
    except ValueError:
        threshold = 0.5

    try:
        gen_lim = int(gen_lim_entry.get())
    except ValueError:
        gen_lim = 5

    try:
        s1 = float(s1_entry.get())
    except ValueError:
        s1 = 0.25

    try:
        s2 = float(s2_entry.get())
    except ValueError:
        s2 = 0.25

    try:
        s3 = float(s3_entry.get())
    except ValueError:
        s3 = 0.25

    try:
        s4 = float(s4_entry.get())
    except ValueError:
        s4 = 0.25

    strategy = strategy_entry.get()
    valid_strategy=['normal', 'fast', 'slow']
    if not strategy  in valid_strategy:
        strategy='normal'

    s_sum = Decimal(str(s1)) + Decimal(str(s2)) + Decimal(str(s3)) + Decimal(str(s4))
    if s_sum != 1:
        messagebox.showinfo("Wrong Values", "S1,S2,S3,S4 should be summed to 1")  # Creates the pop-up message box
        s1=0.25
        s2=0.25
        s3=0.25
        s4=0.25
    # Change the labels on the welcome screen
    pop_label.config(text="Population density: {}".format(threshold))

    lim_label.config(text="Generation limitation of spreading rumor: {}".format(gen_lim))

    s1_label.config(text="S1 proportion: {}".format(s1))

    s2_label.config(text="S2 proportion: {}".format(s2))

    s3_label.config(text="S3 proportion: {}".format(s3))

    s4_label.config(text="S4 proportion: {}".format(s4))

    strategy_label.config(text="Game strategy: {}".format(strategy))

    # Create the new matrix
    if strategy == 'normal':
        matrix = create_matrix()
    if strategy == 'fast':
        matrix = max_neighbors()
    if strategy == 'slow':
        matrix = slow_create_matrix()

    # Destroy the user input window
    window.destroy()


# This function will draw the buttons on the screen.
def draw_buttons():
    # choose the first player:
    start_button = tk.Button(root, text="Start", command=choose_first_wrapper, font=("Comic Sans MS", 8),
                             relief="groove")
    start_button.pack(side='left')
    # start_button.place(x=500, y=1000)
    # pass the rumor:
    next_gen_button = tk.Button(root, text="Next Generation", command=pass_rumor_wrapper, font=("Comic Sans MS", 8),
                                relief="groove")
    next_gen_button.pack(side='right')
    # next_gen_button.place(x=500, y=0)

    next_30_gens_button = tk.Button(root, text="30 Generations forward", command=pass_30_gens,
                                    font=("Comic Sans MS", 8), relief="groove")
    next_30_gens_button.pack(side='bottom')


# create a reference to the welcome screen labels.
welcome = None
config_label = None
pop_label = None
lim_label = None
s1_label = None
s2_label = None
s3_label = None
s4_label = None
strategy_label = None


def welcome_screen():
    global welcome, config_label, lim_label, pop_label, s1_label, s2_label, s3_label, s4_label, strategy_label
    # Create a Tkinter window
    welcome = tk.Toplevel(root)
    welcome.geometry('800x600')  # Set window size

    # Create a label widget for the title
    title_label = tk.Label(welcome, text="Welcome to the Game of Life : Spreading Rumor edition",
                           font=("Comic Sans MS", 18, 'bold'))
    title_label.pack(pady=20)  # Add some padding

    # Create a label widget for the configurations
    config_label = tk.Label(welcome, text="The configurations are:", font=("Comic Sans MS", 14))
    config_label.pack(pady=7)

    pop_label = tk.Label(welcome, text="Population density: {}".format(threshold), font=("Comic Sans MS", 14))
    pop_label.pack(pady=5)

    lim_label = tk.Label(welcome, text="Generation limitation of spreading rumor: {}".format(gen_lim),
                         font=("Comic Sans MS", 14))
    lim_label.pack(pady=5)

    s1_label = tk.Label(welcome, text="S1 proportion: {}".format(s1), font=("Comic Sans MS", 14))
    s1_label.pack(pady=5)

    s2_label = tk.Label(welcome, text="S2 proportion: {}".format(s2), font=("Comic Sans MS", 14))
    s2_label.pack(pady=5)

    s3_label = tk.Label(welcome, text="S3 proportion: {}".format(s3), font=("Comic Sans MS", 14))
    s3_label.pack(pady=5)

    s4_label = tk.Label(welcome, text="S4 proportion: {}".format(s4), font=("Comic Sans MS", 14))
    s4_label.pack(pady=5)

    strategy_label = tk.Label(welcome, text="Game strategy: {}".format(strategy), font=("Comic Sans MS", 14))
    strategy_label.pack(pady=5)

    # Add a button widget to start the game
    start_button = tk.Button(welcome, text="Start Game", command=lambda: start_game(welcome), font=("Comic Sans MS", 8),
                             relief="groove")
    start_button.pack(pady=10)

    input_button = tk.Button(welcome, text="Change configuration", command=get_user_input, font=("Comic Sans MS", 8),
                             relief="groove")
    input_button.pack(pady=10)

    welcome.wait_window()  # Wait for the welcome window to be destroyed


stats_label = None


# This function will close the welcome screen and show the grid.
def start_game(welcome):
    global matrix
    global game_counter
    global canvas
    global stats_label
    # hide the welcome window
    welcome.destroy()
    canvas = tk.Canvas(root, width=cols * 6, height=rows * 6)
    canvas.pack()
    # init a stats label
    stats_label = tk.Label(root, text="")
    stats_label.pack()
    # Draw the buttons on the screen
    draw_buttons()
    # Print the initial matrix before the rumor.
    draw_all_cells(matrix)


# init the Graphics window
# Create a Tkinter window
root = tk.Tk()
root.state('normal')
root.iconify()  # Hide the root window
canvas = None
welcome_screen()

# Make the canvas window pop up
root.update()
root.deiconify()
root.lift()

# Start the Tkinter event loop
root.mainloop()
