import numpy as np
import pyamg
import matplotlib.pyplot as plt
from pyamg import smoothed_aggregation_solver

import data_functions


def main():
    # криво решаем матрицу через pyamg
    A = pyamg.gallery.poisson((1,3), format='csr')
    for i in range(0, 3):
        for j in range(0, 3):
            A[i, j] = i == j
    m1 = smoothed_aggregation_solver(A)
    b = np.random.rand(3)
    for i in range(0, 3):
        b[i] = 1
    print(b)
    print(A)
    x = m1.solve(b)
    print(x)

    # то, что сверху - временная мера
    grid = data_functions.make_grid()

    for vertex in grid.vertices:
        print(f"x={vertex.x};y={vertex.y}")

    for i, element in enumerate(grid.elements):
        print(f"element#{i}")
        print(' _ ', end='')
        for vertex_id in element.vertices_ids:
            vertex = grid.vertices[vertex_id]
            print(f"x={vertex.x};y={vertex.y}", end=' _ ')
        print()




if __name__ == '__main__':
    main()
