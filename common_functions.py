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


def rectangle_form(v1 : data.Vertex, v2 : data.Vertex, v3 : data.Vertex, v4 : data.Vertex, v : data.Vertex, v_id : int):
    """
    Функция формы прямоугольника в Вершине v, относительно Вершины с номером v_id = 1, 2, 3, 4.
    """
    if v_id > 4 or v_id < 1:
        return -1

    rectangle_area = get_triangle_area_made_by_vertices(v1, v2, v3) + get_triangle_area_made_by_vertices(v1, v3, v4)

    if v_id == 1:
        return (get_triangle_area_made_by_vertices(v, v2, v3) + get_triangle_area_made_by_vertices(v, v3, v4)) / rectangle_area
    elif v_id == 2:
        return (get_triangle_area_made_by_vertices(v1, v, v3) + get_triangle_area_made_by_vertices(v1, v3, v4)) / rectangle_area
    elif v_id == 3:
        return (get_triangle_area_made_by_vertices(v1, v2, v) + get_triangle_area_made_by_vertices(v1, v, v4)) / rectangle_area
    elif v_id == 4:
        return (get_triangle_area_made_by_vertices(v1, v2, v3) + get_triangle_area_made_by_vertices(v1, v3, v)) / rectangle_area


def full_rectangle_form_with_function_value(v1 : data.Vertex, v2 : data.Vertex, v3 : data.Vertex, v4 : data.Vertex, v : data.Vertex, f):
    """
    Вычисляет значение функции прямоугольной формы в Вершине v на функции f.
    """
    F1 = f(v1.x, v1.y)
    F2 = f(v2.x, v2.y)
    F3 = f(v3.x, v3.y)
    F4 = f(v4.x, v4.y)

    F1_area = rectangle_form(v1, v2, v3, v4, v, 1)
    F2_area = rectangle_form(v1, v2, v3, v4, v, 2)
    F3_area = rectangle_form(v1, v2, v3, v4, v, 3)
    F4_area = rectangle_form(v1, v2, v3, v4, v, 4)

    return F1 * F1_area + F2 * F2_area + F3 * F3_area + F4 * F4_area