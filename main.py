import matplotlib.pyplot as plt

import data_functions
import solvers


def main():
    # криво решаем матрицу через pyamg
    A = solvers.pyamg.gallery.poisson((1,3), format='csr')
    for i in range(3):
        for j in range(3):
            A[i, j] = i == j
    m1 = solvers.pyamg.smoothed_aggregation_solver(A)
    b = solvers.np.random.rand(3)
    for i in range(3):
        b[i] = 1
    print(b)
    print(A)
    x = m1.solve(b)
    print(x)

    # то, что сверху - временная мера
    grid = data_functions.make_grid()

    for v_id, vertex in enumerate(grid.vertices):
        print('v#%d:x=%f;y=%f'%(v_id, vertex.x, vertex.y))

    for i, element in enumerate(grid.elements):
        print('element#%d'%i)
        print(' _ ', end='')
        for vertex_id in element.vertices_ids:
            vertex = grid.vertices[vertex_id]
            print('x=%f;y%f'%(vertex.x, vertex.y), end=' _ ')
        print()
        for edge_id in element.edges_ids:
            edge = grid.edges[edge_id]
            print(' _ ', end='')
            print('\tedge#%d;v1=%d;v2=%d;e_l=%d;e_r=%d'%(edge_id, edge.v1, edge.v2, edge.element_left, edge.element_right), end=' _ ')
            print('')

    for v_id in range(len(grid.vertices)):
        print("around v%d: %d-elements;%d-edges"%(v_id, len(grid.get_vertex_elements(v_id)), len(grid.get_vertex_edges(v_id))))

    # рисуем сетку
    fig, beforeNone = plt.subplots()
    fig1, beforeLin = plt.subplots()
    fig2, beforeQuad = plt.subplots()

    data_functions.draw_grid(grid, beforeNone)
    grid.set_grid_function(lambda x, y : x + y)
    data_functions.draw_function_on_grid(grid, beforeLin)
    grid.set_grid_function(lambda x, y : (x ** 2 + y ** 2) ** 0.5)
    data_functions.draw_function_on_grid(grid, beforeQuad)

    solvers.solve_grid_deformation(grid)

    fig3, afterNone = plt.subplots()
    fig4, afterLin = plt.subplots()
    fig5, afterQuad = plt.subplots()

    data_functions.draw_grid(grid, afterNone)
    grid.set_grid_function(lambda x, y : x + y)
    data_functions.draw_function_on_grid(grid, afterLin)
    grid.set_grid_function(lambda x, y : (x ** 2 + y ** 2) ** 0.5)
    data_functions.draw_function_on_grid(grid, afterQuad)

    plt.show()


if __name__ == '__main__':
    main()
