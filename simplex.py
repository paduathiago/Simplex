from ast import For
import numpy as np

class Simplex:
    
    def receive_input(self):
        restrictions, variables = [int(x) for x in input().split()]

        vector_c = []
        for c in input().split():
            vector_c.append(float(c))

        restrictions_matrix = []
        current_line = []
        for _ in range(restrictions):
            current_line.append([float(x) for x in input().split()])
            restrictions_matrix.append(current_line)
            current_line = []

        restrictions_matrix = np.array(restrictions_matrix).reshape(restrictions, variables + 1)
        print(restrictions_matrix)

        # Colar vector c na matriz A e adicionar campo correspondente ao cáculo do ótimo
        return vector_c, restrictions_matrix
    
    def FPI(self, vector_c, matrix):
        # Adicionar uma matriz identidade cujas dimensões são iguais ao número de restrições(linhas) da matriz A
        vector_b = matrix[::, np.shape(matrix)[1]-1]
        A_rows = np.shape(matrix)[0]
        aux = np.identity(A_rows)
        for column in aux:
            matrix = np.insert(matrix, -1, column, axis = 1)

        print('===============================')
        print(aux)
        print('===============================')
        print(matrix)
        print('===============================')
        print (vector_b)

        
        print(vector_c)
        for _ in range(np.shape(matrix)[1] - len(vector_c)):
            vector_c.append(0.0)
        print('********************************')
        print(vector_c)

        
simplex = Simplex()
c, A = simplex.receive_input()
simplex.FPI(c, A)