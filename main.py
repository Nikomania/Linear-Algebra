class Vector:
    list_vector = []

    # Vector with 2 coordinates (bidimensational)
    def __init__(self, x=0, y=0):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError('X and Y coordinates must be real numbers')

        self.coordinates = {'x': x, 'y': y}
        # When an object is created, he's registered in this list
        Vector.list_vector.append(self)


    def __repr__(self):
        return str(self.coordinates)


    def __getitem__(self, key):
        return self.coordinates[key]


    def __setitem__(self, key, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Can't assign a value that is not a real number")

        self.coordinates[key] = other


    def __len__(self):
        return len(self.coordinates)


    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self['x'] + other['x'], self['y'] + other['y'])

        raise TypeError("Can't add a vector to other type of value")


    def __radd__(self, other):
        return self.__add__(other)


    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self['x'] - other['x'], self['y'] - other['y'])

        raise TypeError("Can't subtract a vector to other type of value")


    def __rsub__(self, other):
        return self.__sub__(other)

    # Only scalar product (only 2 dimensions)
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self['x'] * other, self['y'] * other)
        
        if isinstance(other, Vector):
            return self['x'] * other['x'] + self['y'] * other['y']

        raise TypeError("A vector must be multiplied by a scalar or another vector")


    def __rmul__(self, other):
        return self.__mul__(other)


    def mod(self):
        return (self['x'] ** 2 + self['y'] ** 2) ** 0.5


    def linear_transformation(self, matrix):
        if not isinstance(matrix, (list, tuple)):
            raise TypeError("Matrix must be a list or a tuple")

        if len(matrix) != 2 or len(matrix[0]) != 2 or len(matrix[1]) != 2:
            print('Error: Must be a squared matrix')
            return

        coordinates = matrix_mul(matrix, [[self['x']], [self['y']]])
        self['x'] = coordinates[0][0]
        self['y'] = coordinates[1][0]


    @classmethod
    def get_vectors(cls):
        return cls.list_vector


    @classmethod
    def linear_transformation_list(cls, matrix):
        if not isinstance(matrix, (list, tuple)):
            raise TypeError("Matrix must be a list or a tuple")

        if len(matrix) != 2 or len(matrix[0]) != 2 or len(matrix[1]) != 2:
            print('Error: Must be a squared matrix')
            return

        for index, vector in enumerate(cls.list_vector):
            coordinates = matrix_mul(matrix, [[vector['x']], [vector['y']]])
            cls.list_vector[index]['x'] = coordinates[0][0]
            cls.list_vector[index]['y'] = coordinates[1][0]



def can_matrix_mul(m1, m2):
    if not isinstance(m1, (tuple, list)) or not isinstance(m2, (tuple, list)):
        print('Error: Matrix must be a list or a tuple')
        return False

    for m in (m1, m2):
        for line in m:
            if not isinstance(line, (list, tuple)):
                print("Error: Matrix's lines must be a list or a tuple")
                return False
            if m == m1:
                if len(line) != len(m2):
                    print("Error: First matrix must have same amount of columns as second's number of lines")
                    return False
            elif len(m[0]) != len(line):
                print("Error: Matrixes must have same number of columns in all of its lines")
                return False

            for element in line:
                if not isinstance(element, (int, float)):
                    print("Error: Matrix's values must be real numbers")
                    return False
    
    return True


def matrix_mul(m1, m2):
    if not can_matrix_mul(m1, m2):
        return

    matrix = []
    for line in range(len(m1)):
        matrix.append(list())
        for column in range(len(m2[0])):
            matrix[line].append(0)
            for index in range(len(m2)):
                matrix[line][column] += m1[line][index] * m2[index][column]

    return matrix



if __name__ == '__main__':
    vetor1 = Vector(2, 3)
    vetor2 = Vector(5, 7)
    matrix = [
        [3, 4],
        [0, -1]
    ]
    vetor1.linear_transformation(matrix)
    print(Vector.get_vectors())
