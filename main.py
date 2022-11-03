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
        simplex_result = self.run_simplex()
        self.print_result(simplex_result)

    def find_possible_solution(self):
        possible_solution = np.zeros(self.variables)
        for j in range(self.variables):
            if self.tableau[0, j] == 0:
                for i in range(1, self.restrictions + 1):  # REVISAR QUESTÃO DE ONDE i começa
                    if self.tableau[i, j] == 1:
                        possible_solution[i - 1] = self.tableau[i, -1]
        return possible_solution
    
    def print_result(self, LP_type):    
        if LP_type == 'optimal':
            print('otima')
            print(self.tableau[0, -1])
            print(self.find_possible_solution())
            # TODO: print certificate
        elif LP_type == 'unbounded':
            print('ilimitada')
        elif LP_type == "not feasible":
            print('inviavel')
            

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
        print(restrictions_matrix)  # REMOVER

        return vector_c, restrictions_matrix
    
    def is_feasible(self):
        is_feasible = False
        for i in range(1, self.restrictions + 1):
            is_feasible = False
            if self.tableau[i, -1] < 0:
                for j in range(len(self.tableau[i]) - 1):
                    if self.tableau[i, j] < 0:
                        is_feasible = True
                        break

                if not is_feasible:
                    return False
        
        return True

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
            if not self.is_feasible():
                return 'not feasible'

            coordinates = self.find_pivot(is_optimal)
            if not coordinates:
                return 'unbounded'

            self.pivot_column(coordinates)
            is_optimal = self.is_optimal()
        
        return 'optimal'
        
    def find_pivot(self, column_with_pivot):
        """
        Returns list containing coordinates for the current pivot's position
        First Element: row
        Second Element: column
        """
        pivot = -1
        pivot_division = 0
        coordinates = []
        for i in range(self.restrictions + 1):
            if self.tableau[i, column_with_pivot] > 0:
                if pivot < 0:
                    pivot = self.tableau[i, column_with_pivot]
                    pivot_division = self.tableau[i, -1] / self.tableau[i, column_with_pivot]
                    coordinates = [i, column_with_pivot]
                else:
                    current_division = self.tableau[i, -1] / self.tableau[i, column_with_pivot]
                    if current_division < pivot_division:
                        pivot = self.tableau[i, column_with_pivot]
                        coordinates = [i, column_with_pivot]
                        pivot_division = current_division
        
        if pivot == -1:  # unbounded LP problem
            return False  
        print(pivot)  # REMOVER
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
