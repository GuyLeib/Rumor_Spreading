from rumor_spreading import matrix, get_stats, game_counter, gen_lim, \
    threshold, s1, s2, s3, s4, rows, cols
import csv
import random
from collections import namedtuple
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

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
            new_num_neigh=cell.num_neighbors + 1
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

    game_counter += 1




def percentage(nums_list, total):
    avg = sum(nums_list) / len(nums_list)
    return (avg / total) * 100


def average(nums_list):
    avg = sum(nums_list) / len(nums_list)
    return avg


def get_num_of_knowers():
    global matrix
    # How many new believers for each iteration
    counter = 0
    for i in range(100):
        for j in range(100):
            if matrix[i][j].received_rumor:
                counter = counter + 1
            if matrix[i][j].received_gen > 0 and not matrix[i][j].received_rumor:
                print("k")
    return counter


def get_total_pop():
    global matrix
    counter = 0
    for i in range(100):
        for j in range(100):
            if matrix[i][j].doubt != 0:
                counter += 1
    return counter


def run_simulatations(l_value=5, p=0.8, S1=0.6, S2=0.2, S3=0.1, S4=0.1):
    global gen_lim
    global threshold
    global s1
    global s2
    global s3
    global s4
    global game_counter
    threshold = p
    gen_lim = l_value
    s1 = S1
    s2 = S2
    s3 = S3
    s4 = S4
    print(s1)
    pepole_per_generation = {}
    for i in range(75):
        pepole_per_generation[i] = []
    for simulation in range(10):
        global matrix
        matrix = create_matrix()
        print("total pop: ", get_total_pop())
        choose_first()
        print(simulation)
        total = get_total_pop()

        for generation in range(75):
            pass_rumor()
            knows = get_num_of_knowers()
            percent = (knows / total) * 100
            pepole_per_generation[generation].append(percent)
            print("genration:", generation, "percent: ", percent)

    avg_people_per_iteration = []
    for gen, number_list in pepole_per_generation.items():
        avg_people_per_iteration.append([gen, average(number_list)])
    return avg_people_per_iteration
    # percent_per_generation = {}
    # avg_per_generation={}
    # for gen, number_list in pepole_per_generation.items():
    #     avg_per_generation[gen]=average(number_list)
    #     percent_per_generation[gen] = percentage(number_list,total)
    #     print(gen, percentage(number_list, total))
    # return percent_per_generation,avg_per_generation


def create_data():
    gen_limit_list = [0, 5, 10, 15, 20, 25, 30]
    threshold_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    s_tuples_list = [(0.25, 0.25, 0.25, 0.25), (0.7, 0.1, 0.1, 0.1), (0.1, 0.7, 0.1, 0.1), (0.1, 0.1, 0.7, 0.1),
                     (0.1, 0.1, 0.1, 0.7)]
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        # # create table for opposite s1 concetration and population denstiy.
        # people_per_generation = run_simulatations(p=0.9, S1=0.9, S2=0.1, S3=0, S4=0)
        # title = ['s proportion:' + str("p=0.9, S1=0.9, S2=0.1, S3=0, S4=0"), ' threshold: ' + str(0.1), ' ']
        # table_headers = ['iteration', 'number_of_people']
        # writer.writerow(title)
        # writer.writerow(table_headers)
        # for row in people_per_generation:
        #     writer.writerow(row)
        # writer.writerow([])
        #
        # # create table for opposite s1 concetration and population denstiy.
        # people_per_generation = run_simulatations(p=0.9, S1=0.9, S2=0.1, S3=0, S4=0)
        # title = ['s proportion:' + str("p=0.9, S1=0.9, S2=0.1, S3=0, S4=0"), ' threshold: ' + str(0.1), ' ']
        # table_headers = ['iteration', 'number_of_people']
        # writer.writerow(title)
        # writer.writerow(table_headers)
        # for row in people_per_generation:
        #     writer.writerow(row)
        # writer.writerow([])
        #
        # # create table for opposite s1 concetration and population denstiy.
        # people_per_generation = run_simulatations(p=0.1, S1=0, S2=0, S3=0.9, S4=0.1)
        # title = ['s proportion:' + str("p=0.1, S1=0, S2=0, S3=0.9, S4=0.1"), ' threshold: ' + str(0.1), ' ']
        # table_headers = ['iteration', 'number_of_people']
        # writer.writerow(title)
        # writer.writerow(table_headers)
        # for row in people_per_generation:
        #     writer.writerow(row)
        # writer.writerow([])

        # create tables for different gen limit:
        for gen_limit in gen_limit_list:
            people_per_generation = run_simulatations(l_value=gen_limit)
            title = ['gen limit:' + str(gen_limit), ' ']
            table_headers = ['iteration', 'number_of_people']
            writer.writerow(title)
            writer.writerow(table_headers)
            for row in people_per_generation:
                writer.writerow(row)
            writer.writerow([])
        # create tables for different threshold:
        for t in threshold_list:
            global threshold
            people_per_generation = run_simulatations(p=t)
            print('threshold: ', threshold)
            title = ['threshold:' + str(t), ' ']
            table_headers = ['iteration', 'number_of_people']
            writer.writerow(title)
            writer.writerow(table_headers)
            for row in people_per_generation:
                writer.writerow(row)
            writer.writerow([])
        # create tables for different population proportion:
        for s_tuple in s_tuples_list:
            people_per_generation = run_simulatations(S1=s_tuple[0], S2=s_tuple[1], S3=s_tuple[2], S4=s_tuple[3])
            title = ['s proportion:' + str(s_tuple), ' ']
            table_headers = ['iteration', 'number_of_people']
            writer.writerow(title)
            writer.writerow(table_headers)
            for row in people_per_generation:
                writer.writerow(row)
            writer.writerow([])
        # create table for opposite s1 concetration and population denstiy.
        people_per_generation = run_simulatations(p=0.7, S1=0, S2=0, S3=0.2, S4=0.8)
        title = ['s proportion:' + str(0.1), ' threshold: ' + str(0.9), ' ']
        table_headers = ['iteration', 'number_of_people']
        writer.writerow(title)
        writer.writerow(table_headers)
        for row in people_per_generation:
            writer.writerow(row)
        writer.writerow([])
        # create table for opposite s1 concetration and population denstiy.
        people_per_generation = run_simulatations(p=0.3, S1=0.8, S2=0.2, S3=0, S4=0)
        title = ['s proportion:' + str("S1=0.7,S2=0.1,S3=0.1,S4=0.1"), ' threshold: ' + str(0.1), ' ']
        table_headers = ['iteration', 'number_of_people']
        writer.writerow(title)
        writer.writerow(table_headers)
        for row in people_per_generation:
            writer.writerow(row)
        writer.writerow([])


def spilt_to_df():
    titles = []
    dict_df = {}
    # read the csv file and save it as a list:
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        # create a list of tuples containing title,start index and end index:
        for t in range(0, 1872, 78):
            title = (str(rows[t][0]), t + 2, t + 76)
            titles.append(title)
    #
    for i in range(len(titles)):
        # create list containing only the relevant rows for the df:
        list_for_df = rows[titles[i][1]:titles[i][2] + 1][:]
        # create a df:
        df = pd.DataFrame(list_for_df, columns=['iteration', 'percent'])
        # convert values to numeric values:
        df['iteration'] = pd.to_numeric(df['iteration'])
        df['percent'] = pd.to_numeric(df['percent'])
        key = titles[i][0]
        # add the df to a dict if df's:
        dict_df[key] = df
    return dict_df


def slow_create_matrix():
    global threshold, s1, s2, s3, s4
    threshold=0.7
    s1=0.6
    s2=0.2
    s3=0.1
    s4=0.1
    global matrix
    matrix = []
    # define the namedtuple
    Cell = namedtuple('Cell', ['doubt', 'received_rumor', 'received_gen', 'passed_gen', 'num_neighbors', 'temp_doubt',
                               'counter'])
    total_pop=0
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

    s1_count=int(s1*total_pop)
    s2_count=int(s2*total_pop)
    s3_count = int(s3 * total_pop)
    s4_count = int(s4 * total_pop)
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j].doubt == 5:
                if s1_count > 0:
                    matrix[i][j] = matrix[i][j]._replace(doubt=1)
                    s1_count -= 1
                    continue
                elif s4_count > 0:
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
                else:
                    matrix[i][j] = matrix[i][j]._replace(doubt=0)
    print (matrix)
    return matrix


def run_and_plot_slow_strategy():
    people_per_gen = run_simulatations(5, 0.7, 0.6, 0.2, 0.1, 0.1)
    x_values = [row[0] for row in people_per_gen]
    y_values = [row[1] for row in people_per_gen]

    # Plot the two lists using plt.plot()
    plt.plot(x_values, y_values)

    # set the x-axis label
    plt.xlabel('Generation')

    # set the y-axis label
    plt.ylabel('Percent Of Spread')

    # Add plot title
    plt.title('Slow Strategy')
    plt.ylim(0, 80)
    plt.xlim(0, 75)


    # Show the plot
    plt.show()
    plt.savefig("slow_stg")

def create_matrix_s1():
    global threshold, s1, s2, s3, s4
    global matrix
    fast_matrix = []
    neighbor_matrix = []
    # Possible value for dobutness level.
    doubt_value = [1, 2, 3, 4]
    # define the namedtuple
    Cell = namedtuple('Cell', ['doubt', 'received_rumor', 'received_gen', 'passed_gen', 'num_neighbors', 'temp_doubt',
                               'counter'])

    # Creating a matrix filled with cells
    threshold = 0.7
    for i in range(rows):
        row = []
        neighbor_row = []
        for j in range(cols):
            if random.uniform(0, 1) <= threshold:
                row.append(Cell(-1, False, 0, 0, 0, 0, 0))
            else:
                row.append(Cell(0, False, 0, 0, 0, 0, 0))
        fast_matrix.append(row)

    # Step 1: Count the number of humans in the matrix
    num_humans = sum(cell.doubt == -1 for row in fast_matrix for cell in row)
    num_of_missing_humans = sum(cell.doubt == 0 for row in fast_matrix for cell in row)
    print(num_of_missing_humans)

    # calculate the number of cells with doubt level 1, 2, 3, 4
    num_s1 = math.ceil(0.6 * num_humans)
    num_s2 = math.ceil(0.2 * num_humans)
    num_s3 = math.ceil(0.1 * num_humans)
    num_s4 = num_humans - num_s1 - num_s2 - num_s3

    # Step 3: Loop over the matrix and assign doubt level of 1 to a neighbor of each human, until the counter is 0
    while num_s1 > 0:
        for i in range(rows):
            for j in range(cols):
                if fast_matrix[i][j].doubt == -1:
                    # Check if the human has a neighbor with doubt level of 1
                    neighbors = get_neighbors(fast_matrix, i, j)
                    # Filter the neighbors
                    neighbors_choice = [(ni, nj) for ni, nj in neighbors if fast_matrix[ni][nj].doubt != 0]
                    if not neighbors_choice:
                        continue
                    rand_i, rand_j = random.choice(neighbors_choice)
                    fast_matrix[rand_i][rand_j] = fast_matrix[rand_i][rand_j]._replace(doubt=1)
                    num_s1 -= 1
                    num_humans -=1
                    if num_s1 == 0:
                        break
            if num_s1 == 0:
                break

    # Step 3: Loop over the matrix and assign doubt level of 1 to a neighbor of each human, until the counter is 0
    while num_s2 > 0:
        for i in range(rows):
            for j in range(cols):
                if fast_matrix[i][j].doubt !=0:
                    # Check if the human has a neighbor with doubt level of 1
                    neighbors = get_neighbors(fast_matrix, i, j)
                    neighbors_choice = [(ni, nj) for ni, nj in neighbors if (fast_matrix[ni][nj].doubt == -1)]
                    if not neighbors_choice:
                        continue
                    rand_i, rand_j = random.choice(neighbors_choice)
                    fast_matrix[rand_i][rand_j] = fast_matrix[rand_i][rand_j]._replace(doubt=2)
                    num_s2 -= 1
                    num_humans -=1
                    if num_s2 == 0:
                        break
            if num_s2 == 0:
                break

    # Step 3: Loop over the matrix and assign doubt level of 1 to a neighbor of each human, until the counter is 0
    while num_s3 > 0:
        for i in range(rows):
            for j in range(cols):
                if fast_matrix[i][j].doubt != 0:
                    # Check if the human has a neighbor with doubt level of 1
                    neighbors = get_neighbors(fast_matrix, i, j)
                    # If not, assign doubt level of 1 to a random neighbor with doubt level of 0
                    neighbors_choice = [(ni, nj) for ni, nj in neighbors if (fast_matrix[ni][nj].doubt == -1)]
                    if not neighbors_choice:
                        continue
                    rand_i, rand_j = random.choice(neighbors_choice)
                    fast_matrix[rand_i][rand_j] = fast_matrix[rand_i][rand_j]._replace(doubt=3)
                    num_s3 -= 1
                    num_humans -= 1
                    if num_s3 == 0:
                        break
            if num_s3 == 0:
                break

    # Step 3: Loop over the matrix and assign doubt level of 1 to a neighbor of each human, until the counter is 0
    while num_s4 > 0:
        for i in range(rows):
            for j in range(cols):
                if fast_matrix[i][j].doubt != 0:
                    # Check if the human has a neighbor with doubt level of 1
                    neighbors = get_neighbors(fast_matrix, i, j)
                    # Filter the neighbors
                    neighbors_choice = [(ni, nj) for ni, nj in neighbors if (fast_matrix[ni][nj].doubt == -1)]
                    if not neighbors_choice:
                        continue
                    rand_i, rand_j = random.choice(neighbors_choice)
                    fast_matrix[rand_i][rand_j] = fast_matrix[rand_i][rand_j]._replace(doubt=4)
                    num_s4 -= 1
                    num_humans -= 1
                    if num_s4 == 0:
                        break
            if num_s4 == 0:
                break

    num_of_missing_humans2 = sum(cell.doubt == 0 for row in fast_matrix for cell in row)
    print(num_of_missing_humans2)
    return fast_matrix


def get_neighbors(matrix, i, j):
    global rows,cols
    neighbors = []
    for di, dj in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            neighbors.append((ni, nj))
    return neighbors

def plot_data():
    dict_df = spilt_to_df()
    ###test
    fig, ax = plt.subplots()
    ax.set_title('generation limit')
    for key, value in dict_df.items():
        if key.startswith('s proportion:'):
            x = value['iteration']
            y = value['percent']
            # Plot the data as a continuous line

            ax.plot(x, y, label=key)

    # Set the labels and title
    ax.set_xlabel('iteration')
    ax.set_ylabel('percent of spread')
    x_min = min(x)
    x_max = max(x)

    # Set the x-limits to fit the values
    ax.set_xlim(x_min, x_max)
    # Add a legend
    plt.legend()
    # Saves and Show the plot
    plt.savefig("gen_lim.png")
    plt.show()

    # generate a plot for generation limit:
    # Create a figure and axis object
    fig, ax = plt.subplots()
    ax.set_title('Rumor spreading rate -Generation Limit')
    for key, value in dict_df.items():
        if key.startswith('gen'):
            x = value['iteration']
            y = value['percent']
            # Plot the data as a continuous line
            ax.plot(x, y, label=key)

    # Set the labels and title
    ax.set_xlabel('Generation')
    ax.set_ylabel('Percent Of Spread')
    x_min = min(x)
    x_max = max(x)

    # Set the x-limits to fit the values
    ax.set_xlim(x_min, x_max)
    # Add a legend
    plt.legend(["0", "5", "10", "15", "20", "25", "30"])
    # Saves and Show the plot
    plt.savefig("gen_lim.png")
    plt.show()

    plt.clf()
    # generate a plot for s proportion:
    fig, ax = plt.subplots()
    ax.set_title('Rumor spreading rate -S Proportion')
    for key, value in dict_df.items():
        if key.startswith('s proportion:('):
            x = value['iteration']
            y = value['percent']
            # Plot the data as a continuous line
            ax.plot(x, y, label=key)
    # Set the labels and title
    ax.set_xlabel('Generation')
    ax.set_ylabel('Percent Of Spread')
    # Add a legend
    plt.legend(["s1=0.25, s2=0.25, s3=0.25, s4=0.25", "s1=0.7, s2=0.1, s3=0.1, s4=0.1", "s1=0.1, s2=0.7, s3=0.1, s4=0.1",  "s1=0.1, s2=0.1, s3=0.7, s4=0.1","s1=0.1, s2=0.1, s3=0.1, s4=0.7"])
    # Show the plot
    plt.savefig("s proportion.png")
    plt.show()

    plt.clf()
    # generate a plot for population density (threshold):
    fig, ax = plt.subplots()
    ax.set_title('s proportion')
    for key, value in dict_df.items():
        if key.startswith('threshold'):
            x = value['iteration']
            y = value['percent']
            # Plot the data as a continuous line
            ax.plot(x, y, label=key)
    # Set the labels and title
    ax.set_xlabel('Generation')
    ax.set_ylabel('Percent Of Spread')
    ax.set_title("Rumor spreading rate - Population Density ")

    # Add a legend
    plt.legend(["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"])
    # Show the plot
    plt.savefig("threshold.png")
    plt.show()

    plt.clf()
    # generate a plot for Population Density vs Doubt level:
    fig, ax = plt.subplots()
    ax.set_title('s proportion')
    for key, value in dict_df.items():
        if key.startswith('s proportion:0.1') or key.startswith("s proportion:S1=0.7"):
            x = value['iteration']
            y = value['percent']
            # Plot the data as a continuous line
            ax.plot(x, y, label=key)

    # Set the labels and title
    ax.set_xlabel('Generation')
    ax.set_ylabel('Percent Of Spread')
    ax.set_title("Rumor spreading rate - Population Density vs Doubt Level ")
    # Add a legend
    plt.legend(["Low Density High Doubt", "High Density Low Doubt"])
    # Show the plot
    plt.savefig("density_vs_doubt.png")
    plt.show()

    plt.clf()
    # Plot that demonstrate in which generation the rumor spread the most
    fig, ax = plt.subplots(figsize=(10, 6))  # adjust the figure size
    for key, value in dict_df.items():
        if key.startswith('threshold'):
            prev_per = 0
            x = value['iteration']
            changed_y = value['percent']
            for index, value in changed_y.iteritems():
                temp = value - prev_per
                prev_per = value
                changed_y[index] = temp
            y = changed_y

            # Plot the data as a continuous line
            ax.bar(x, y, width=0.8, align='center', color='black', linewidth=0)
            # Get the minimum and maximum x-values
            x_min = min(x)
            x_max = max(x)

            # Set the x-limits to fit the values
            ax.set_xlim(x_min , x_max)

    # Set the labels and title
    ax.set_xlabel('Generation')
    ax.set_ylabel('Percent of new knowers')
    ax.set_title("Rumor Spread in each generation")
    # Add a legend
    plt.legend()
    # Show the plot
    plt.savefig("generation_spread.png")
    plt.show()
    plt.clf()


run_and_plot_slow_strategy()
