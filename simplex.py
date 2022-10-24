import numpy as np

class Simplex:
    
    def receive_input(self):
        restrictions, variables = [int(x) for x in input().split()]

        vector_c = []
        vector_c.append([float(c) for c in input().split()])

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
    
    def FPI(self, matrix):
        # Adicionar uma matriz identidade cujas dimensões são iguais ao número de restrições(linhas) da matriz A
        vector_b = matrix[::, np.shape(matrix)[1]-1]
        rows = np.shape(matrix)[0]
        aux = np.identity(rows)
        for column in aux:
            matrix = np.insert(matrix, -1, column, axis = 1)

        print('===============================')
        print(aux)
        print('===============================')
        print(matrix)
        print('===============================')
        print (vector_b)

simplex = Simplex()
c, A = simplex.receive_input()
simplex.FPI(A)