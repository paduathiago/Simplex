import numpy as np
from copy import deepcopy


class Tableau:

    def __init__(self):
        self.tableau = []
        self.restrictions = 0
        self.variables = 0

    def FPI(self, vector_c, matrix):
        # Inserts (number of restrictions x number of restrictions) identity matrix 
        A_rows = np.shape(matrix)[0]
        aux = np.identity(A_rows)
        for column in aux:
            matrix = np.insert(matrix, -1, column, axis = 1)

        for _ in range(np.shape(matrix)[1] - len(vector_c)):
            vector_c.append(0.0)

        vector_c = np.array(vector_c)
        return vector_c, matrix

    def build_tableau(self, matrix_A, vector_c, restrictions, variables):
        tableau = np.insert(vector_c, 0, -1 * matrix_A, axis=0)
        self.tableau = tableau
        self.restrictions = restrictions
        self.variables = variables
        return self

    def build_auxiliary_LP(Tableau):
        auxiliary_LP = deepcopy(Tableau)
        for i in range(1, auxiliary_LP.restrictions + 1):
            if auxiliary_LP.tableau[i, -1] < 0:
                auxiliary_LP.tableau[i] = np.negative(auxiliary_LP.tableau[i])
        
        auxiliary_LP.tableau[0] = np.zeros_like(auxiliary_LP.tableau[0])
        identity = np.identity(np.shape(auxiliary_LP.tableau)[0] - 1)
        negative_entries = np.full(np.shape(auxiliary_LP.tableau)[0] -1, 1)
        new_matrix = np.insert(identity, 0, negative_entries, axis=0)
        auxiliary_LP.tableau = np.insert(auxiliary_LP.tableau, [-1], new_matrix, axis=1)
        return auxiliary_LP

    def find_pivot(self, column_with_pivot):
        """
        Returns list containing coordinates for the current pivot's position; False if unbounded LP problem
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
            
        return coordinates
    
    def round_zeros(self, value):
        if(abs(value) < 1e-4):
            value = 0.0
        return value

    def pivot_column(self, coordinates):
        self.tableau[coordinates[0]] /=  self.tableau[coordinates[0], coordinates[1]]
        for i in range(self.restrictions + 1):
            if i != coordinates[0]:
                self.tableau[i] += np.multiply((-1 * self.tableau[i, coordinates[1]]), self.tableau[coordinates[0]])
        
        find_zeros = np.vectorize(self.round_zeros)
        self.tableau = find_zeros(self.tableau)

    def is_pivot_column(self, column):
        counter = 0
        pivot_line = None
        for i, entry in enumerate(column):
            if not (entry == 0.0 or entry == 1.0):
                return False, None
            elif entry == 1.0:
                counter += 1
                pivot_line = i
                if counter > 1:
                    return False, None
        return True, pivot_line
    
    def canonize(self):
        for j in range(len(self.tableau[0] -1)):
            is_pivot, pivot_line = self.is_pivot_column(self.tableau[1:, j])
            if is_pivot:
                self.tableau[0] += np.multiply((-1 * self.tableau[0, j]), self.tableau[pivot_line + 1])
        return self

    def canonize_auxiliary_LP(self):
        for row in range(1, np.shape(self.tableau)[0]):
            self.tableau[0] -= self.tableau[row]
        return self.tableau

    def is_b_negative(self):
        if np.all(self.tableau[:, -1] >= 0):
            return False
        return True

class Simplex:
    
    def __init__(self):
        self.tableau = Tableau()
        self.restrictions = 0
        self.variables = 0

    def solve_LP(self):
        c, A = self.process_input()
        FPI_A, FPI_c = self.tableau.FPI(c, A)
        self.tableau = self.tableau.build_tableau(FPI_A, FPI_c, self.restrictions, self.variables)
        if self.tableau.is_b_negative():
            simplex_result = self.run_two_phase_simplex()
            self.print_result(self.tableau.tableau, simplex_result)
        else:
            simplex_result = self.run_simplex(self.tableau)
            self.print_result(self.tableau.tableau, simplex_result)

    def find_possible_solution(self, tableau):
        possible_solution = np.zeros(self.variables)
        for j in range(self.variables):
            if tableau[0, j] == 0:
                for i in range(1, self.restrictions + 1):
                    if tableau[i, j] == 1:
                        possible_solution[j] = tableau[i, -1]
        return possible_solution
    
    def print_result(self, tableau, LP_type):    
        if LP_type == 'optimal':
            print('otima')
            print(f'{tableau[0, -1]:.7f}')
            for item in self.find_possible_solution(tableau):
                print(f'{item:.7f}', end=" ")
            print()
        elif LP_type == 'unbounded':
            print('ilimitada')
            for item in self.find_possible_solution(tableau):
                print(f'{item:.7f}', end=" ")
            print()
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

        return vector_c, restrictions_matrix
    
    def is_feasible(self, Tableau):
        is_feasible = False
        for i in range(1, Tableau.restrictions + 1):
            is_feasible = False
            if Tableau.tableau[i, -1] < 0:
                for j in range(len(Tableau.tableau[i]) - 1):
                    if Tableau.tableau[i, j] < 0:
                        is_feasible = True
                        break

                if not is_feasible:
                    return False
        return True
    
    def run_simplex(self, Tableau, is_auxiliary_LP=False):
        if not is_auxiliary_LP:
            is_PL_optimal = self.is_optimal(Tableau.tableau)
            while not is_PL_optimal == 'T':
                if not self.is_feasible(Tableau):
                    return 'not feasible'

                coordinates = Tableau.find_pivot(is_PL_optimal)
                if not coordinates:
                    return 'unbounded'

                Tableau.pivot_column(coordinates)
                is_PL_optimal = self.is_optimal(Tableau.tableau)
            return 'optimal'
        
        is_PL_optimal = self.is_optimal(Tableau.tableau)
        while not is_PL_optimal == 'T':
            coordinates = Tableau.find_pivot(is_PL_optimal)
            Tableau.pivot_column(coordinates)
            is_PL_optimal = self.is_optimal(Tableau.tableau)
        
        return Tableau.tableau[0, -1]

    def run_two_phase_simplex(self):
        """
        2-Phase Simplex method used when b vector has at least one negative entry

        Returns "not feasible" if the original LP is not feasible; runs simplex on auxiliary tableau otherwise
        """
        auxiliary_LP = self.tableau.build_auxiliary_LP()
        auxiliary_LP.tableau = auxiliary_LP.canonize_auxiliary_LP()
        
        optimal_value = self.run_simplex(auxiliary_LP, is_auxiliary_LP=True)
        if optimal_value < 0:
            return "not feasible"
    
        self.tableau = self.build_tableau_after_auxiliary(self.tableau, auxiliary_LP)
        return self.run_simplex(self.tableau)
    
    def build_tableau_after_auxiliary(self, tableau_original, tableau_auxiliar):
        tableau_auxiliar.tableau = np.delete(tableau_auxiliar.tableau, np.s_[len(tableau_original.tableau[0]) - 1 : -1], axis=1)
        tableau_auxiliar.tableau[0] = tableau_original.tableau[0]
        
        tableau_auxiliar = tableau_auxiliar.canonize()
        return tableau_auxiliar
        
    def is_optimal(self, tableau):
        """
        Returns wether the simplex has reached optimality (returns 'T') or not.
        In the second case, the value returned is the column index for the next pivot
        """
        for column_index, element in enumerate(tableau[0, :-1]):
            if element < 0:
                return column_index
        return 'T'

        
simplex = Simplex()
simplex.solve_LP()
