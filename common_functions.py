import math

import data


def get_triangle_area_made_by_vertices(vl : data.Vertex, vm : data.Vertex, vn : data.Vertex):
    """
    Реализация вычисления площади плоского треугольника, заданного 3-мя Вершинами.
    """
    return 0.5 * math.fabs(
        (vl.x - vn.x) * (vm.y - vn.y) - (vm.x - vn.x) * (vl.y - vn.y)
    )


def triangle_form(vl : data.Vertex, vm : data.Vertex, vn : data.Vertex, v : data.Vertex, f):
    """
    Вычисляет значение функции треугольной формы в треугольнике (vl, vm, vn) в точке v на функции f.
    """
    Fl = f(vl.x, vl.y)
    Fm = f(vm.x, vm.y)
    Fn = f(vn.x, vn.y)

    area = get_triangle_area_made_by_vertices(vl, vm, vn)

    Fl_area = get_triangle_area_made_by_vertices(v, vm, vn)
    Fm_area = get_triangle_area_made_by_vertices(vl, v, vn)
    Fn_area = get_triangle_area_made_by_vertices(vl, vm, v)

    return (Fl * Fl_area + Fm * Fm_area + Fn * Fn_area) / area

