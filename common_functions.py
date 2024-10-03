import math

import data


def get_triangle_area_made_by_vertices(vl : data.Vertex, vm : data.Vertex, vn : data.Vertex):
    """
    Реализация вычисления площади плоского треугольника, заданного 3-мя Вершинами.
    """
    return 0.5 * math.fabs(
        (vl.x - vn.x) * (vm.y - vn.y) - (vm.x - vn.x) * (vl.y - vn.y)
    )


def triangle_form(v1 : data.Vertex, v2 : data.Vertex, v3 : data.Vertex, v : data.Vertex, v_id : int):
    """
    Функция формы треугольника в Вершине v, относительно Вершины с номером v_id = 1, 2, 3.
    """
    if v_id > 3 or v_id < 1:
        return -1

    triangle_area = get_triangle_area_made_by_vertices(v1, v2, v3)

    if v_id == 1:
        return get_triangle_area_made_by_vertices(v, v2, v3) / triangle_area
    elif v_id == 2:
        return get_triangle_area_made_by_vertices(v1, v, v3) / triangle_area
    elif v_id == 3:
        return get_triangle_area_made_by_vertices(v1, v2, v) / triangle_area


def full_triangle_form_with_function_value(v1 : data.Vertex, v2 : data.Vertex, v3 : data.Vertex, v : data.Vertex, f):
    """
    Вычисляет значение функции треугольной формы в Вершине v на функции f.
    """
    F1 = f(v1.x, v1.y)
    F2 = f(v2.x, v2.y)
    F3 = f(v3.x, v3.y)

    F1_area = triangle_form(v1, v2, v3, v, 1)
    F2_area = triangle_form(v1, v2, v3, v, 2)
    F3_area = triangle_form(v1, v2, v3, v, 3)

    return F1 * F1_area + F2 * F2_area + F3 * F3_area


def dfi(v1 : data.Vertex, v2 : data.Vertex, v3 : data.Vertex, v_id : int, xy):
    """
    Получение значения производной у формы треугольника по x или y.
    """
    if v_id < 1 or v_id > 3:
        return None

    if xy not in ['x', 'y']:
        return None

    triangle_area = get_triangle_area_made_by_vertices(v1, v2, v3)

    if v_id == 1:
        if xy == 'x':
            return (v3.y - v2.y) / triangle_area
        elif xy == 'y':
            return (v3.x - v2.x) / triangle_area
        return None
    elif v_id == 2:
        if xy == 'x':
            return (v1.y - v3.y) / triangle_area
        elif xy == 'y':
            return (v1.x - v3.x) / triangle_area
        return None
    elif v_id == 3:
        if xy == 'x':
            return (v2.y - v1.y) / triangle_area
        elif xy == 'y':
            return (v2.x - v1.x) / triangle_area
        return None


def dfi_integral(v1 : data.Vertex, v2 : data.Vertex, v3 : data.Vertex, v_id : int, xy):
    """
    Получение интеграла от производной формы треугольника по x или y.
    """
    triangle_area = get_triangle_area_made_by_vertices(v1, v2, v3)

    return dfi(v1, v2, v3, v_id, xy) * triangle_area


def dfi2_integral(v1: data.Vertex, v2: data.Vertex, v3: data.Vertex, v_id1: int, v_id2, xy1, xy2):
    """
    Получение интеграла от производных форм треугольника по x и/или y.
    """
    triangle_area = get_triangle_area_made_by_vertices(v1, v2, v3)

    return dfi(v1, v2, v3, v_id1, xy1) * dfi(v1, v2, v3, v_id2, xy2) * triangle_area


def fi_integral(grid : data.Grid, el_id : int, v_id : int):
    """
    Считает интеграл формы треугольника по Элементу с индексом el_id.
    1 <= v_id <= 3 : относительно Вершин Элемента в его массиве element.vertices_ids.
    """
    element = grid.elements[el_id]

    if element.type != data.ElementType.TRIANGLE:
        return None

    if element.is_at_border(grid.edges):
        res = 0
        for edge_id in element.edges_ids:
            edge = grid.edges[edge_id]
            if edge.element_right == -1:
                edge_center = edge.get_center(grid.vertices)
                res += triangle_form(grid.vertices[element.vertices_ids[0]],
                                     grid.vertices[element.vertices_ids[1]],
                                     grid.vertices[element.vertices_ids[2]],
                                     edge_center,
                                     v_id)
        return res
    else:
        # q = 1, r = s = 0 in q!r!s!/(q+r+s+2)! * 2F
        # не зависит от номера формы
        return 1 / 6 * 2 * get_triangle_area_made_by_vertices(grid.vertices[element.vertices_ids[0]],
                                                              grid.vertices[element.vertices_ids[1]],
                                                              grid.vertices[element.vertices_ids[2]])


def fi2_integral(grid: data.Grid, el_id: int, v_id1: int, v_id2 : int):
    """
    Считает интеграл двух форм треугольника по Элементу с индексом el_id.
    1 <= v_id1(2) <= 3 : относительно Вершин Элемента в его массиве element.vertices_ids.
    """
    element = grid.elements[el_id]

    if element.type != data.ElementType.TRIANGLE:
        return None

    if element.is_at_border(grid.edges):
        res = 0
        for edge_id in element.edges_ids:
            edge = grid.edges[edge_id]
            if edge.element_right == -1:
                edge_center = edge.get_center(grid.vertices)
                res += (triangle_form(grid.vertices[element.vertices_ids[0]],
                                     grid.vertices[element.vertices_ids[1]],
                                     grid.vertices[element.vertices_ids[2]],
                                     edge_center,
                                     v_id1) *
                        triangle_form(grid.vertices[element.vertices_ids[0]],
                                     grid.vertices[element.vertices_ids[1]],
                                     grid.vertices[element.vertices_ids[2]],
                                     edge_center,
                                     v_id2))
        return res
    else:
        # q = r = 1, s = 0 in q!r!s!/(q+r+s+2)! * 2F
        # не зависит от номера формы
        return 1 / 24 * 2 * get_triangle_area_made_by_vertices(grid.vertices[element.vertices_ids[0]],
                                                              grid.vertices[element.vertices_ids[1]],
                                                              grid.vertices[element.vertices_ids[2]])

# то, что ниже, вроде как не то, что надо
# def rectangle_form(v1 : data.Vertex, v2 : data.Vertex, v3 : data.Vertex, v4 : data.Vertex, v : data.Vertex, v_id : int):
#     """
#     Функция формы прямоугольника в Вершине v, относительно Вершины с номером v_id = 1, 2, 3, 4.
#     """
#     if v_id > 4 or v_id < 1:
#         return -1
#
#     rectangle_area = get_triangle_area_made_by_vertices(v1, v2, v3) + get_triangle_area_made_by_vertices(v1, v3, v4)
#
#     if v_id == 1:
#         return (get_triangle_area_made_by_vertices(v, v2, v3) + get_triangle_area_made_by_vertices(v, v3, v4)) / rectangle_area
#     elif v_id == 2:
#         return (get_triangle_area_made_by_vertices(v1, v, v3) + get_triangle_area_made_by_vertices(v1, v3, v4)) / rectangle_area
#     elif v_id == 3:
#         return (get_triangle_area_made_by_vertices(v1, v2, v) + get_triangle_area_made_by_vertices(v1, v, v4)) / rectangle_area
#     elif v_id == 4:
#         return (get_triangle_area_made_by_vertices(v1, v2, v3) + get_triangle_area_made_by_vertices(v1, v3, v)) / rectangle_area
#
#
# def full_rectangle_form_with_function_value(v1 : data.Vertex, v2 : data.Vertex, v3 : data.Vertex, v4 : data.Vertex, v : data.Vertex, f):
#     """
#     Вычисляет значение функции прямоугольной формы в Вершине v на функции f.
#     """
#     F1 = f(v1.x, v1.y)
#     F2 = f(v2.x, v2.y)
#     F3 = f(v3.x, v3.y)
#     F4 = f(v4.x, v4.y)
#
#     F1_area = rectangle_form(v1, v2, v3, v4, v, 1)
#     F2_area = rectangle_form(v1, v2, v3, v4, v, 2)
#     F3_area = rectangle_form(v1, v2, v3, v4, v, 3)
#     F4_area = rectangle_form(v1, v2, v3, v4, v, 4)
#
#     return F1 * F1_area + F2 * F2_area + F3 * F3_area + F4 * F4_area