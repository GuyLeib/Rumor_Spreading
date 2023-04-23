from rumor_spreading import matrix, choose_first, pass_rumor, get_stats, create_matrix, game_counter, gen_lim, \
    threshold, s1, s2, s3, s4, rows, cols
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


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


def run_simulatations(l_value=5, p=0.5, S1=0.25, S2=0.25, S3=0.25, S4=0.25):
    global gen_lim
    global threshold
    global s1
    global s2
    global s3
    global s4
    threshold = p
    gen_lim = l_value
    s1 = S1
    s2 = S2
    s3 = S3
    s4 = S4
    print(s1)
    pepole_per_generation = {}
    for i in range(30):
        pepole_per_generation[i] = []
    for simulation in range(100):
        global matrix
        matrix = create_matrix()
        print("total pop: ", get_total_pop())
        choose_first()
        print(simulation)
        total = get_total_pop()

        for generation in range(30):
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
        people_per_generation = run_simulatations(p=0.9, S1=0.1, S2=0.1, S3=0.1, S4=0.7)
        title = ['s proportion:' + str(0.1), ' threshold: ' + str(0.9), ' ']
        table_headers = ['iteration', 'number_of_people']
        writer.writerow(title)
        writer.writerow(table_headers)
        for row in people_per_generation:
            writer.writerow(row)
        writer.writerow([])
        # create table for opposite s1 concetration and population denstiy.
        people_per_generation = run_simulatations(p=0.1, S1=0.7, S2=0.1, S3=0.1, S4=0.1)
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
        for t in range(0, 791, 33):
            title = (str(rows[t][0]), t + 2, t + 31)
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


def plot_data():
    dict_df = spilt_to_df()
    # generate a plot for generation limit:
    # Create a figure and axis object
    fig, ax = plt.subplots()
    ax.set_title('generation limit')
    for key, value in dict_df.items():
        if key.startswith('gen'):
            x = value['iteration']
            y = value['percent']
            # Plot the data as a continuous line
            ax.plot(x, y, label=key)

    # Set the labels and title
    ax.set_xlabel('iteration')
    ax.set_ylabel('percent of spread')
    # Add a legend
    plt.legend()
    #Saves and Show the plot
    plt.savefig("gen_lim.png")
    plt.show()

    plt.clf()
    # generate a plot for s proportion:
    fig, ax = plt.subplots()
    ax.set_title('s proportion')
    for key, value in dict_df.items():
        if key.startswith('s proportion:('):
            x = value['iteration']
            y = value['percent']
            # Plot the data as a continuous line
            ax.plot(x, y, label=key)
    # Set the labels and title
    ax.set_xlabel('iteration')
    ax.set_ylabel('percent of spread')
    # Add a legend
    plt.legend()
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
    ax.set_xlabel('iteration')
    ax.set_ylabel('percent of spread')
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
    ax.set_xlabel('iteration')
    ax.set_ylabel('percent of spread')
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
            ax.bar(x, y, width=0.8, align='center', edgecolor='black')
            ax.set_xticks(range(0, 30))
    # Set the labels and title
    ax.set_xlabel('Generation')
    ax.set_ylabel('Percent of new knowers')
    ax.set_title("Rumor Spread in each generation")
    # Add a legend
    plt.legend()
    # Show the plot
    plt.savefig("generation_spread.png")
    plt.show()


# create_data()
plot_data()
