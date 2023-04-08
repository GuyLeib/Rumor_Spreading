import random
from collections import namedtuple

game_counter=0

def create_matrix(threshold = 0.5):
    # Variables: Number of rows, columns.
    rows = 100
    cols = 100
    matrix = []
    doubt_value = [1,2,3,4]
    # define the namedtuple
    Cell = namedtuple('Cell', ['doubt', 'recieved_rumor','recieved_gen','passed_gen', 'num_neighbors','temp_doubt', 'counter'])

    # Creating a matrix filled with 0.
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.uniform(0, 1) >= threshold:
                # If larger than threshold than the cell is filled human.
                # The doubtness level is assigned.
                row.append(Cell(random.choice(doubt_value), False, 0, 0, 0, 0))
            else: 
                row.append(Cell(0, False, 0, 0, 0, 0)) 
        matrix.append(row)

    return matrix

def choose_fisrt(matrix):
    is_staffed = False
    while not is_staffed:
        row=random.randint(0,99)
        column = random.randint(0, 99)
        if matrix[row][column] is not None:
            is_staffed = True
            return row, column

def believe_rumor(doubt_level):
    if doubt_level==1:
        return True;
    elif doubt_level==2:
        if random.uniform(0, 1) >=(1/3):
            return True
        else:
            return False
    elif doubt_level==3:
        if random.uniform(0, 1) < (1 / 3):
            return True
        else:
            return False
    elif doubt_level==4:
        return False;
def define_temp_doubt(doubt):
    if doubt!=1:
        return doubt-1
    else:
        return 1;


def get_rumor(cell):
    # check if cell is not none:
    if cell is None:
        return None
    global game_counter
    # check if the neighbor already received the rumor in another generation:
    if cell.received_rumor is True:
        if cell.recieved_gen != game_counter:
            cell.num_neighbors = 1
        else:
            cell.num_neighbors += 1
    else:
        cell.received_rumor = True
        cell.num_neighbors += 1
        # check if there is a need to update temp_doubt:
    if cell.num_neighbors >= 2 and cell.recieved_gen == game_counter:
        # update temp_doubt:
        cell.temp_doubt = define_temp_doubt(cell.doubt)
    # update the received generation:
    cell.received_gen = game_counter
    return cell


def spread_to_neighbors(row, column, matrix):
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

    return matrix


def pass_rumor(matrix, is_first, gen_lim, row=None, column=None):
    if is_first:
        matrix = spread_to_neighbors(row, column, matrix, gen_lim)
        matrix[row][column].counter -= 1
        return matrix
    else:
        # Loop over all the board:
        for i in range(100):
            for j in range(100):
                if matrix[i][j] is not None:
                    # if the cell already spreaded the rumor + the generation is game_counter-1 + l_counter ==0:
                    if matrix[i][j].recieved_rumor and matrix[i][j].recieved_gen == game_counter-1 \
                            and matrix[i][j].counter == 0:
                        # check if the cell has a temp doubt:
                        if matrix[i][j].temp_doubt != 0:
                            believe = believe_rumor(matrix[i][j].temp_doubt)
                        else:
                            believe = believe_rumor(matrix[i][j].doubt)
                        # check if the cell believes the rumor, if so- spread to neighbors:
                        if believe:
                            # update L counter:
                            matrix[row][column].counter = gen_lim
                            # update the passing generation:
                            matrix[i][j].passed_gen = game_counter

                            matrix = spread_to_neighbors(matrix, i, j, gen_lim)
                    if matrix[i][j].counter != 0:
                        # decrement the L counter:
                        matrix[i][j].counter -= 1
                    # clear temp doubt if needed:
                    if matrix[i][j].temp_doubt != 0 and matrix[i][j].recieved_gen <= game_counter - 1:
                        matrix[row - 1][column - 1].temp_doubt = 0

    return matrix
def Game_flow():
    game_over= False
    # get from the user generation limit♥♥:
    gen_lim=5
    matrix = create_matrix()
    # print matrix♥♥:
    # choose the first player:
    row, column = choose_fisrt(matrix)
    # pass the first rumor:
    matrix=pass_rumor(matrix, True, gen_lim,  row, column)
    # print the matrix♥♥:
    # increment the game's counter:
    global game_counter
    game_counter += 1
    # loop until game is over:
    while not game_over:
        matrix = pass_rumor()
        game_counter += 1
        # print the matrix♥♥:

