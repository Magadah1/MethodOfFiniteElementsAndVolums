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
        print('element#%d'%i)
        print(' _ ', end='')
        for vertex_id in element.vertices_ids:
            vertex = grid.vertices[vertex_id]
            print('x=%f;y%f'%(vertex.x, vertex.y), end=' _ ')
        print()

    # рисуем сетку
    fig, beforeNone = plt.subplots()
    fig1, beforeLin = plt.subplots()
    fig2, beforeQuad = plt.subplots()

    data_functions.draw_grid(grid, beforeNone)
    data_functions.draw_function_on_grid(grid, lambda x, y : x + y, beforeLin)
    data_functions.draw_function_on_grid(grid, lambda x, y : (x ** 2 + y ** 2) ** 0.5, beforeQuad)

    data_functions.random_grid_translation(grid)

    fig3, afterNone = plt.subplots()
    fig4, afterLin = plt.subplots()
    fig5, afterQuad = plt.subplots()

    data_functions.draw_grid(grid, afterNone)
    data_functions.draw_function_on_grid(grid, lambda x, y : x + y, afterLin)
    data_functions.draw_function_on_grid(grid, lambda x, y : (x ** 2 + y ** 2) ** 0.5, afterQuad)

    plt.show()


if __name__ == '__main__':
    main()
