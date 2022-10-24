import numpy as np

restrictions, variables = [int(x) for x in input().split()]

vector_c = []
vector_c.append([int(c) for c in input().split()])

restrictions_matrix = []
current_line = []
for k in range(restrictions):
    current_line.append([int(x) for x in input().split()])
    restrictions_matrix.append(current_line)
    current_line = []

restrictions_matrix = np.array(restrictions_matrix).reshape(restrictions, variables + 1)

print(restrictions_matrix)