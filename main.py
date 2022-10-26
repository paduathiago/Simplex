import numpy as np

class Simplex:
    
    def __init__(self):
        self.tableau = []
        self.restrictions = 0
        self.variables = 0

    def solve_LP(self):
        c, A = simplex.process_input()
        FPI_A, FPI_c = simplex.FPI(c, A)
        self.tableau = simplex.build_tableau(FPI_A, FPI_c)
        self.run_simplex()

    def process_input(self):
        self.restrictions, self.variables = [int(x) for x in input().split()]

        vector_c = []
        for c in input().split():
            vector_c.append(float(c))

        restrictions_matrix = []
        current_line = []
        for _ in range(self.restrictions):
            current_line.append([float(x) for x in input().split()])
            restrictions_matrix.append(current_line)
            current_line = []

        restrictions_matrix = np.array(restrictions_matrix).reshape(self.restrictions, self.variables + 1)
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
        vector_c = np.array(vector_c)

        return vector_c, matrix

    def build_tableau(self, matrix_A, vector_c):
        tableau = np.insert(vector_c, 0, -1 * matrix_A, axis=0)
        print(tableau)  # REMOVER
        return tableau
    
    def run_simplex(self):
        while not self.is_simplex_finished():
            self.find_pivot()
        # TODO: call print method
        
    def find_pivot(self):
        elements_in_column_lte0 = 0
        pivot = -1
        for column_index, element in enumerate(self.tableau[0,:-1]):
            if element < 0:
                for i in range(self.restrictions):
                    if self.tableau[i, column_index] <= 0:
                        elements_in_column_lte0 += 1
                    else:
                        if pivot < 0:
                            pivot = self.tableau[i, column_index]
                        else:
                            if self.tableau[i, self.variables + 1] / self.tableau[i, column_index] < pivot:
                                pivot = self.tableau[i, column_index]
        #if elements_in_column_lte0 == self.restrictions:
            # PL ilimitada     


    def is_simplex_finished(self):
        # print(self.tableau[0,:-1])  # REVISAR : esse range depende da utilização ou não do VERO na resolução do problema
        for element in self.tableau[0,:-1]:
            if element < 0:
                return False
        return True

        
simplex = Simplex()
simplex.solve_LP()
