from rumor_spreading import choose_first, pass_rumor,get_stats,create_matrix, knows_the_rumor, total_population, game_counter,gen_lim,threshold,s1, s2, s3 ,s4, rows, cols

def percentage(nums_list, total):
    avg=sum(nums_list)/len(nums_list)
    return (avg/total)*100

def create_plots():
    import seaborn as sns
    import matplotlib.pyplot as plt
    global total_population
    global knows_the_rumor
    global matrix
    # list of P with 0.1 jumps
    # differnt options for s1-s4
    # list of L with jump of 5

    # create a dictionary to hold the percentage of people for each iteration:
    pepole_per_generation = {}
    for i in range(30):
        pepole_per_generation[i] = []
        print(pepole_per_generation)
    for simulation in range(10):
        knows_the_rumor = 1
        total_population = 0
        matrix = create_matrix()
        choose_first()
        for generation in range(30):
            pass_rumor()
            pepole_per_generation[generation].append(knows_the_rumor)
            print("genration:" ,generation, "knows: ", knows_the_rumor )

    # create a dict of simulation results:
    percent_per_generation={}
    for gen, number_list in pepole_per_generation.items():
        percent_per_generation[gen]=percentage(number_list, total_population)
    # create lists for the x and y values
    x_vals = list(percent_per_generation.keys())
    y_vals = list(percent_per_generation.values())

    # create a density plot using seaborn
    sns.kdeplot(x=x_vals, y=y_vals)

    # add labels and title to the plot
    plt.xlabel('Generation')
    plt.ylabel('Percentage of People Who Know the Rumor')
    plt.title('Density Plot of Rumor Spread by Generation')

    # display the plot
    plt.show()


create_plots()