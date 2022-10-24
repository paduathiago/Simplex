import numpy as np

def print_matrix(matrix):
    for i in np.shape(matrix)[0]:  # rows
        for j in np.shape(matrix)[1]:
            print(f'{matrix[i][j]} ')
        print()


restrictions, variables = int(input()).split()

restrictions_matrix = np.array([])
current_line = np.array([])
for k in range(restrictions):
    for value in input().split():
        current_line.append(value)
    restrictions_matrix.append(current_line, axis = 0)
    current_line = np.array([])



