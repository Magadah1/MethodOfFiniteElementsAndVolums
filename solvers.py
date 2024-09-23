import pyamg
import numpy as np

import data

class FEM_Solver:
    """
    Метод Конечных Элементов
    """
    pass


class FVM_Solver:
    """
    Метод Конечных Объёмов
    """
    pass


def solve_grid_deformation(grid : data.Grid):
    """
    Минимизируя функционал энергии, определяет новые положения Вершин Сетки.
    Не влияет на граничные Вершины!
    """
    XY = pyamg.gallery.poisson((1, len(grid.vertices)), format='csr') # я хз как нормально создать матрицу
    X = np.random.rand(len(grid.vertices))
    Y = np.random.rand(len(grid.vertices))

    # заполняем базовыми значениями
    for i in range(len(grid.vertices)):
        X[i] = 0
        Y[i] = 0
        for j in range(len(grid.vertices)):
            XY[i, j] = 0

    # пишем функционал для каждой Вершины
    for ver_id in range(len(grid.vertices)): # ver_id - номер текущей Вершины
        if grid.vertices[ver_id].is_at_boarder: # если Вершина на границе, то она не будет подвергнута смещению
            XY[ver_id, ver_id] = 1
            X[ver_id] = grid.vertices[ver_id].x
            Y[ver_id] = grid.vertices[ver_id].y
            continue

        edges_ids = grid.get_vertex_edges(ver_id) # берём индексы всех Рёбер, в которых одна из Вершин - текущая, не граничная
        XY[ver_id, ver_id] = len(edges_ids)
        for edge_id in edges_ids:
            edge = grid.edges[edge_id] # Ребро, одна из Вершин которого - текущая
            if edge.v1 == ver_id:
                v_id = edge.v2 # номер другой Вершины
                v = grid.vertices[v_id]
                if v.is_at_boarder: # если она на границе,
                    X[ver_id] += v.x # в X для нашей Вершины суммируется координата
                    Y[ver_id] += v.y # (аналогично в Y).
                else:
                    XY[ver_id, v_id] = -1
            elif edge.v2 == ver_id:
                v_id = edge.v1 # номер другой Вершины
                v = grid.vertices[v_id]
                if v.is_at_boarder: # если она на границе,
                    X[ver_id] += v.x # в X для нашей Вершины суммируется координата
                    Y[ver_id] += v.y # (аналогично в Y).
                else:
                    XY[ver_id, v_id] = -1

    # решаем получившуюся матрицу и обновляем значения координат Вершин Сетки
    solver = pyamg.smoothed_aggregation_solver(XY)
    newX = solver.solve(X)
    newY = solver.solve(Y)
    for i in range(len(newX)):
        grid.vertices[i].x = newX[i]
        grid.vertices[i].y = newY[i]