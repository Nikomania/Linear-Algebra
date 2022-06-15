from tkinter import mainloop
from graphics import *
import time


TITLE = 'Linear algebra project'
WIDTH, LENGTH = 1000, 1000
BG_COLOUR = 'black'
OBJ_COLOUR = 'white'


class Vector:
    list_vector = list()
    list_len = 0

    # Vector with 2 coordinates (bidimensational)
    def __init__(self, x=0, y=0, insert=True):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError('X and Y coordinates must be real numbers')

        self.coord = {'x': x, 'y': y}
        # When an object is created, he's registered in this list
        if insert:
            Vector.list_len += 1
            Vector.list_vector.append(self)


    def __iter__(self):
        self.i = 0
        return self


    def __next__(self):
        c = 'x', 'y'
        self.i += 1
        if self.i == 3:
            raise StopIteration

        return self[c[self.i - 1]]


    def __repr__(self):
        return f"({self['x']}, {self['y']})"


    def __getitem__(self, key):
        return self.coord.get(key, False)


    def __setitem__(self, key, value):
        if self.coord.get(key, None) is None:
            print(f"There isn't a key called {key}")
            return

        self.coord[key] = value


    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self['x'] + other['x'], self['y'] + other['y'], insert=False)

        raise TypeError("Can't add a vector to other type of value")


    def __radd__(self, other):
        return self.__add__(other)


    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self['x'] - other['x'], self['y'] - other['y'], insert=False)

        raise TypeError("Can't subtract a vector to other type of value")


    def __rsub__(self, other):
        return self.__sub__(other)


    def __mul__(self, other):
        # Only scalar product (only 2 dimensions)
        if isinstance(other, (int, float)):
            return Vector(self['x'] * other, self['y'] * other, insert=False)
        
        if isinstance(other, Vector):
            return self['x'] * other['x'] + self['y'] * other['y']

        raise TypeError("A vector must be multiplied by a scalar or another vector")


    def __rmul__(self, other):
        return self.__mul__(other)


    def mod(self):
        return (self * self) ** 0.5


    def linear_transformation(self, matrix):
        if not isinstance(matrix, (list, tuple)):
            raise TypeError("Matrix must be a list or a tuple")

        if len(matrix) != 2 or len(matrix[0]) != 2 or len(matrix[1]) != 2:
            print('Error: Must be a squared matrix')
            return

        coordinates = matrix_mul(matrix, [[self['x']], [self['y']]])
        return Vector(coordinates[0][0], coordinates[1][0], insert=False)


    def show(self, win, wid, len, color=OBJ_COLOUR, add=True):
        global BG_COLOUR

        if add:
            action = 'add'
        else:
            action = 'remove'
            color = BG_COLOUR

        if not isinstance(win, GraphWin):
            print(f'To {action} a vector from a window, the argument must be a GraphWin')
            return
        
        point = Point(self['x'] + wid / 2, self['y'] + len / 2)
        point.setFill(color)

        point.draw(win)


    @classmethod
    def get_vectors(cls):
        return cls.list_vector


    @classmethod
    def linear_transformation_all(cls, matrix):
        if not isinstance(matrix, (list, tuple)):
            raise TypeError("Matrix must be a list or a tuple")

        if len(matrix) != 2 or len(matrix[0]) != 2 or len(matrix[1]) != 2:
            print('Error: Must be a squared matrix')
            return

        old_vectors = []
        for index, vector in enumerate(cls.list_vector):
            old_vectors.append(Vector(vector['x'], vector['y'], insert=False))
            coordinates = matrix_mul(matrix, [[vector['x']], [vector['y']]])
            cls.list_vector[index]['x'] = coordinates[0][0]
            cls.list_vector[index]['y'] = coordinates[1][0]

        return old_vectors


    @classmethod
    def update_vectors_win(cls, old, win, wid, len, color=OBJ_COLOUR, gradient=None):
        for vector in old:
            vector.show(win, wid, len, add=False)

        if gradient is None:
            for vector in cls.list_vector:
                vector.show(win, wid, len, color)
            return
        
        linear_gradient(cls.list_vector, win, wid, len, gradient[0], gradient[1])
        



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


def linear_gradient(vectors, win, wid, len, start, increment):
        index = 0
        colors = [start, start, start]
        for vector in vectors:
            colors[index] += increment
            if colors[index] > 255:
                colors[index] = 255
                index += 1
            vector.show(win, wid, len, color_rgb(*colors), add=True)


if __name__ == '__main__':
    window = GraphWin(TITLE, WIDTH, LENGTH)
    window.setBackground(BG_COLOUR)
    axises = [Line(Point(0, 500), Point(1000, 500)), Line(Point(500, 0), Point(500, 1000))]

    for axis in axises:
        axis.setFill(OBJ_COLOUR)
        axis.draw(window)

    
    index = 0
    colors = [50, 50, 50]
    for x in range(-100, 101, 10):
        for y in range(-100, 101, 10):
            colors[index] += 1
            if colors[index] > 255:
                colors[index] = 255
                index += 1
        
            Vector(x, y).show(window, WIDTH, LENGTH, color_rgb(*colors), True)

    
    matrix = [
        [1, -1],
        [0, 1]
    ]
    
    old_vectors = Vector.linear_transformation_all(matrix)

    time.sleep(2)
    Vector.update_vectors_win(old_vectors, window, WIDTH, LENGTH, color='red', gradient=[50, 1])


    mainloop()