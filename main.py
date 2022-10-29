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
        A_rows = np.shape(matrix)[0]
        aux = np.identity(A_rows)
        for column in aux:
            matrix = np.insert(matrix, -1, column, axis = 1)

        for _ in range(np.shape(matrix)[1] - len(vector_c)):
            vector_c.append(0.0)

        vector_c = np.array(vector_c)
        return vector_c, matrix

    def build_tableau(self, matrix_A, vector_c):
        tableau = np.insert(vector_c, 0, -1 * matrix_A, axis=0)
        print(tableau)  # REMOVER
        return tableau
    
    def run_simplex(self):
        is_optimal = self.is_optimal()
        while not is_optimal == 'T':
            coordinates = self.find_pivot(is_optimal)
            self.pivot_column(coordinates)
            is_optimal = self.is_optimal()
        # TODO: call print method
        
    def find_pivot(self, column_with_pivot):
        """
        Returns list containing coordinates for the current pivot's position
        First Element: row
        Second Element: column
        """
        pivot = -1
        division = 0
        coordinates = []
        for i in range(self.restrictions + 1):
            if self.tableau[i, column_with_pivot] > 0:
                if pivot < 0:
                    pivot = self.tableau[i, column_with_pivot]
                    division = self.tableau[i, self.variables + 1] / self.tableau[i, column_with_pivot]
                    coordinates = [i, column_with_pivot]
                else:
                    if self.tableau[i, self.variables + 1] / self.tableau[i, column_with_pivot] < division:
                        pivot = self.tableau[i, column_with_pivot]
                        coordinates = [i, column_with_pivot]
        
        if pivot == -1:
            print('PL ILIMITADA')  
        print(pivot)
        return coordinates

    def pivot_column(self, coordinates):
        self.tableau[coordinates[0]] /=  self.tableau[coordinates[0], coordinates[1]]
        for i in range(self.restrictions + 1):
            if i != coordinates[0]:
                self.tableau[i] += np.multiply((-1 * self.tableau[i, coordinates[1]]), self.tableau[coordinates[0]])
        print(self.tableau)

    def is_optimal(self):
        """
        Returns wether the simplex has reached optimality (result = 'T') or not.
        In the second case, the value returned is the column index for the next pivot
        """
        
        # print(self.tableau[0,:-1])  # REVISAR : esse range depende da utilização ou não do VERO na resolução do problema
        for column_index, element in enumerate(self.tableau[0,:-1]):
            if element < 0:
                return column_index
        return 'T'

        
simplex = Simplex()
simplex.solve_LP()
