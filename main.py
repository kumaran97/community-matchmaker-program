import random
import pandas as pd

STUDENTS = ['Abed', 'Annie', 'Britta', 'Jeff', 'Pierce', 'Shirley', 'Todd', 'Troy']

# Create dictionary with list of preferred partners for each student. For each student, a random list
# is created from their most preferred partner to least preferred.

def create_matrix():
    preferred_partners = {}

    for stud in STUDENTS:
        students = list(STUDENTS)
        students.remove(stud)
        preferred_partners[stud] = random.sample(students, 7)

    # Create 2D matrix of preferred partners

    partner_matrix_func = []

    for key in preferred_partners:
        new_row = []
        for j in range(len(preferred_partners[key])):
            new_row.append(preferred_partners[key][j])
        partner_matrix_func.append(new_row)

    partners_df = pd.DataFrame(partner_matrix_func, index=STUDENTS)

    return partners_df

# Based on the preferred partners matrix, create a 2D matrix assigning score to each person

def score_matrix(people):

    score_df = pd.DataFrame(0, index=STUDENTS, columns=STUDENTS)

    for name in STUDENTS:
        rank = 7
        for i in range(len(people[0]) - 1):
            choice = people[i][name]
            score_df[choice][name] = rank
            rank -= 1

    return score_df

# Create an upper matrix getting sum of each pairing

def sum_matrix(score_df):

    sum_df = pd.DataFrame(0, index=STUDENTS, columns=STUDENTS)

    for name in STUDENTS:
        for choice in STUDENTS:
            if sum_df[name][choice] == 0:
                sum_df[choice][name] = score_df[choice][name] + score_df[name][choice]

    return sum_df

# Find the top 4 scores and that'll be the pairings

def find_pairings(sum_df_fp):

    name_1 = []
    name_2 = []
    sum_pairing = []

    for name in STUDENTS:
        for choice in STUDENTS:
            name_1.append(name)
            name_2.append(choice)
            sum_pairing.append(sum_df_fp[choice][name])

    sum_table = pd.DataFrame({'Student 1': name_1,
                              'Student 2': name_2,
                              'Sum': sum_pairing})
    sum_table.sort_values(by='Sum', inplace=True, ascending=False)
    sum_table.reset_index(inplace=True)

    final_pairings = []
    for i in range(0, 30):
        if sum_table['Student 1'][i] not in final_pairings and sum_table['Student 2'][i] not in final_pairings:
            final_pairings.append(sum_table['Student 1'][i])
            final_pairings.append(sum_table['Student 2'][i])

    return final_pairings


##### MAIN #####

partners = create_matrix()
scores = score_matrix(partners)
sums = sum_matrix(scores)
final_list = find_pairings(sums)

# Output: announce pairings

for i in range(0, int(len(final_list)), 2):
    print(f'Pairing {int(i/2 + 1)} is {final_list[i]} and {final_list[i+1]}.')