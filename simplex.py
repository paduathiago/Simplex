import numpy as np


restrictions, variables = [int(x) for x in input().split()]

"""
restrictions_matrix = np.array([])
current_line = np.array([])
for k in range(restrictions):
    for value in [int(x) for x in input().split()]:
        current_line.append(value)
    restrictions_matrix.concat(current_line, axis = 0)
    current_line = np.array([])
"""

"""
restrictions_matrix = np.array([])
current_line = []
for k in range(restrictions):
    current_line.append([int(x) for x in input().split()])
        #current_line = np.append(current_line, value)
    restrictions_matrix = np.concatenate((restrictions_matrix, current_line))
    current_line = np.array([])
"""
restrictions_matrix = []
current_line = []
for k in range(restrictions):
    current_line.append([int(x) for x in input().split()])
        #current_line = np.append(current_line, value)
    restrictions_matrix.append(current_line)
    current_line = []

restrictions_matrix = np.array(restrictions_matrix).reshape(restrictions, variables + 1)



print(restrictions_matrix)