from traceback import print_tb

import numpy as np
import pyamg
import matplotlib.pyplot as plt

import data_functions


def main():
    # криво решаем матрицу через pyamg
    A = pyamg.gallery.poisson((1,3), format='csr')
    for i in range(3):
        for j in range(3):
            A[i, j] = i == j
    m1 = pyamg.smoothed_aggregation_solver(A)
    b = np.random.rand(3)
    for i in range(3):
        b[i] = 1
    print(b)
    print(A)
    x = m1.solve(b)
    print(x)

    # то, что сверху - временная мера
    grid = data_functions.make_grid()

    for vertex in grid.vertices:
        print('x=%f;y=%f'%(vertex.x, vertex.y))

    for i, element in enumerate(grid.elements):
        print('element#%d'%(i))
        print(' _ ', end='')
        for vertex_id in element.vertices_ids:
            vertex = grid.vertices[vertex_id]
            print('x=%f;y%f'%(vertex.x, vertex.y), end=' _ ')
        print()




if __name__ == '__main__':
    main()
