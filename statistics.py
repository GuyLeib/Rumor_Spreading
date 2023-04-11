from rumor_spreading import matrix, choose_first, pass_rumor,get_stats,create_matrix, game_counter,gen_lim,threshold,s1, s2, s3 ,s4, rows, cols
import csv
def percentage(nums_list, total):
    avg=sum(nums_list)/len(nums_list)
    return (avg/total)*100

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
                counter += 1
    return counter


def get_total_pop():
    global matrix
    counter= 0
    for i in range(100):
        for j in range(100):
            if matrix[i][j].doubt!=0:
                counter += 1
    return counter




def run_simulatations(l_value=5, p=0.5, S1=0.25,S2=0.25,S3=0.25,S4=0.25):
    global gen_lim
    global threshold
    global s1
    global s2
    global s3
    global s4
    threshold = p
    gen_lim=l_value
    s1=S1
    s2=S2
    s3=S3
    s4=S4
    print(s1)
    pepole_per_generation = {}
    for i in range(30):
        pepole_per_generation[i] = []

    for simulation in range(100):
        global matrix
        matrix = create_matrix()
        total = get_total_pop()
        print("total pop: ", get_total_pop())
        choose_first()
        print(simulation)
        for generation in range(30):
            pass_rumor()
            knows = get_num_of_knowers()
            pepole_per_generation[generation].append(knows)
            print("genration:", generation, "knows: ",knows)
    avg_people_per_iteration=[]
    for gen, number_list in pepole_per_generation.items():
        avg_people_per_iteration.append([gen,average(number_list)])
    return avg_people_per_iteration
    # percent_per_generation = {}
    # avg_per_generation={}
    # for gen, number_list in pepole_per_generation.items():
    #     avg_per_generation[gen]=average(number_list)
    #     percent_per_generation[gen] = percentage(number_list,total)
    #     print(gen, percentage(number_list, total))
    # return percent_per_generation,avg_per_generation


def create_data():
    gen_limit_list=[0,5,10,15,20,25,30]
    threshold_list=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    s_tuples_list=[(0.25, 0.25,0.25,0.25), (0.7,0.1,0.1,0.1),(0.1,0.7,0.1,0.1),(0.1,0.1,0.7,0.1),(0.1,0.1,0.1,0.7)]
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # create tables for different gen limit:
        for gen_limit in gen_limit_list:
            people_per_generation = run_simulatations(l_value=gen_limit)
            title= ['gen limit:'+str(gen_limit), ' ']
            table_headers=['iteration', 'number_of_people']
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
            people_per_generation = run_simulatations(S1=s_tuple[0],S2=s_tuple[1],S3=s_tuple[2],S4=s_tuple[3])
            title = ['s proportion:' + str(s_tuple), ' ']
            table_headers = ['iteration', 'number_of_people']
            writer.writerow(title)
            writer.writerow(table_headers)
            for row in people_per_generation:
                writer.writerow(row)
            writer.writerow([])
        # create table for opposite s1 concetration and population denstiy.
        people_per_generation = run_simulatations(p=0.9,S1=0.1,S2=0.1,S3=0.1,S4=0.7)
        title = ['s proportion:' + str(0.1), ' threshold: ' +str(0.9),' ']
        table_headers = ['iteration', 'number_of_people']
        writer.writerow(title)
        writer.writerow(table_headers)
        for row in people_per_generation:
            writer.writerow(row)
        writer.writerow([])
        # create table for opposite s1 concetration and population denstiy.
        people_per_generation = run_simulatations(p=0.1,S1=0.7,S2=0.1,S3=0.1,S4=0.1)
        title = ['s proportion:' + str("S1=0.7,S2=0.1,S3=0.1,S4=0.1"), ' threshold: ' +str(0.1),' ']
        table_headers = ['iteration', 'number_of_people']
        writer.writerow(title)
        writer.writerow(table_headers)
        for row in people_per_generation:
            writer.writerow(row)
        writer.writerow([])



create_data()
