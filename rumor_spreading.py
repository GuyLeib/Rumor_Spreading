import random
from collections import namedtuple
import tkinter as tk
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
matrix=[]

def create_matrix():
    global threshold, s1, s2, s3, s4
    global matrix
    matrix=[]
    # Possible value for dobutness level.
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


def choose_first():
    global matrix
    is_staffed = False
    while not is_staffed:
        row = random.randint(0, 99)
        column = random.randint(0, 99)
        if matrix[row][column] is not None:
            is_staffed = True
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
        cell = cell._replace(num_neighbors=cell.num_neighbors + 1)
    else:
        if cell.received_gen != game_counter:
            cell = cell._replace(num_neighbors=1)
        else:
            cell = cell._replace(num_neighbors=cell.num_neighbors + 1)
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
                    matrix[row + 1][column + 1] = get_rumor(matrix[row - 1][column + 1])
    if column > 0:
        matrix[row][column - 1] = get_rumor(matrix[row][column - 1])
        if column < 99:
            matrix[row][column + 1] = get_rumor(matrix[row][column + 1])


def pass_rumor():
    global matrix
    global gen_lim
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
    canvas.delete('all')
    pass_rumor()
    game_counter += 1
    root.update()
    draw_all_cells(matrix, True)
    get_stats()
    root.update()


# Prints the number of people knows the rumor in each iteration
def get_stats():
    global game_counter
    global matrix
    # How many new believers for each iteration
    counter = 0
    for i in range(100):
        for j in range(100):
            if matrix[i][j].received_rumor:
                counter += 1
    print("Iteration {} : the rumor spread to {} people".format(game_counter, counter))


def validate_float(input):
    try:
        value = float(input)
        if 0 <= value <= 1:
            return True
        else:
            return False
    except ValueError:
        return False


# def validate_sum():
#     try:
#         value1 = float(number_entry1.get())
#         value2 = float(number_entry2.get())
#         value3 = float(number_entry3.get())
#         value4 = float(number_entry4.get())
#         if abs(value1 + value2 + value3 + value4 - 1) < 0.0001:
#             return True
#         else:
#             return False
#     except ValueError:
#         return False

# This function will get the desired configuration from the user.
def get_user_input():
    global threshold, gen_lim, s1, s2, s3, s4, matrix

    # Create a new Toplevel window
    user_input_window = tk.Toplevel()
    user_input_window.geometry('400x300')  # Set window size

    # Create a label widget for the title
    title_label = tk.Label(user_input_window, text="Enter new configuration", font=("Arial", 18))
    title_label.pack(pady=10)  # Add some padding

    # Create input fields for threshold, gen_lim, and var3
    threshold_label = tk.Label(user_input_window, text="Enter the desired population density:")
    threshold_label.pack(pady=10)
    threshold_entry = tk.Entry(user_input_window)
    threshold_entry.pack(pady=5)

    gen_lim_label = tk.Label(user_input_window, text="Enter the generation limitation of spreading rumor:")
    gen_lim_label.pack(pady=10)
    gen_lim_entry = tk.Entry(user_input_window)
    gen_lim_entry.pack(pady=5)

    s1_label = tk.Label(user_input_window, text="Enter the percentage of s1 people: (0-1)")
    s1_label.pack(pady=10)
    s1_entry = tk.Entry(user_input_window)
    s1_entry.pack(pady=5)

    s2_label = tk.Label(user_input_window, text="Enter the percentage of s2 people: (0-1)")
    s2_label.pack(pady=10)
    s2_entry = tk.Entry(user_input_window)
    s2_entry.pack(pady=5)

    s3_label = tk.Label(user_input_window, text="Enter the percentage of s3 people: (0-1)")
    s3_label.pack(pady=10)
    s3_entry = tk.Entry(user_input_window)
    s3_entry.pack(pady=5)

    s4_label = tk.Label(user_input_window, text="Enter the percentage of s4 people: (0-1)")
    s4_label.pack(pady=10)
    s4_entry = tk.Entry(user_input_window)
    s4_entry.pack(pady=5)

    # Create a button to submit the user input
    submit_button = tk.Button(user_input_window, text="Submit",
                              command=lambda: submit_user_input(user_input_window, threshold_entry, gen_lim_entry,
                                                                s1_entry, s2_entry, s3_entry, s4_entry))
    submit_button.pack(pady=10, padx=10, side="bottom")


def submit_user_input(window, threshold_entry, gen_lim_entry, s1_entry, s2_entry, s3_entry, s4_entry):
    global threshold, gen_lim, s1, s2, s3, s4, matrix

    # Get user input values
    threshold = float(threshold_entry.get())
    gen_lim = int(gen_lim_entry.get())
    s1 = float(s1_entry.get())
    s2 = float(s2_entry.get())
    s3 = float(s3_entry.get())
    s4 = float(s4_entry.get())

    # Create the matrix using the user input
    matrix = create_matrix()

    # Destroy the user input window
    window.destroy()


# This function will draw the buttons on the screen.
def draw_buttons():
    # choose the first player:
    start_button = tk.Button(root, text="Start", command=choose_first_wrapper)
    # start_button.pack()
    start_button.place(x=500, y=1000)
    # pass the rumor:
    next_gen_button = tk.Button(root, text="Next Generation", command=pass_rumor_wrapper)
    # next_gen_button.pack()
    next_gen_button.place(x=500, y=0)


# Global variables for the Game flow
matrix = create_matrix()


def welcome_screen():
    # Create a Tkinter window
    welcome = tk.Toplevel(root)
    welcome.geometry('800x600')  # Set window size

    # Create a label widget for the title
    title_label = tk.Label(welcome, text="Welcome to the Game of Life : Spreading Rumor edition", font=("Arial", 20))
    title_label.pack(pady=20)  # Add some padding

    # Create a label widget for the configurations
    config_label = tk.Label(welcome, text="The configurations are:", font=("Arial", 14))
    config_label.pack(pady=10)

    config_label = tk.Label(welcome, text="Population density: {}".format(threshold), font=("Arial", 14))
    config_label.pack(pady=10)

    config_label = tk.Label(welcome, text="Generation limitation of spreading rumor: {}".format(gen_lim),
                            font=("Arial", 14))
    config_label.pack(pady=10)

    # Add a button widget to start the game
    start_button = tk.Button(welcome, text="Start Game", command=lambda: start_game(welcome))
    start_button.pack(pady=20)

    input_button = tk.Button(welcome, text="Change configuration", command=get_user_input)
    input_button.pack(pady=20)

    welcome.wait_window()  # Wait for the welcome window to be destroyed


def start_game(welcome):
    global matrix
    global game_counter
    global canvas
    # hide the welcome window
    welcome.destroy()
    canvas = tk.Canvas(root, width=cols * 10, height=rows * 10)
    canvas.pack()
    # Draw the buttons on the screen
    draw_buttons()
    # Print the initial matrix before the rumor.
    draw_all_cells(matrix)


# init the Graphics window
# Create a Tkinter window
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
