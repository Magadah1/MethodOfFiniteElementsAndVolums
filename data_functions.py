import math
import random

import data

def make_rectangular_grid_of_unconnected_vertices(Lx : float, Ly : float, Nx : int, Ny : int):
    """
    Создаёт прямоугольную сетку из вершин в нужном количестве и с нужными шагами.
    """
    vertices = []

    hx = Lx / Nx
    hy = Ly / Ny

    # послойно заполняем матрицу послойно по y
    for iy in range(0, Ny + 1):
        for ix in range(0, Nx + 1):
            vertices.append(data.Vertex(x = 0 + hx * ix, y = 0 + hy * iy))

    return vertices


def make_radial_grid_of_unconnected_vertices(Ir : float, Or : float, Nr : int, NFi : int):
    """
    Создаёт радиальную сетку из вершин в нужном количестве и с нужными шагами. Центр в (0, 0)
    """
    vertices = []

    start_angle = math.pi

    hr = (Or - Ir) / Nr
    hfi = start_angle / NFi

    # послойное заполнение слева направо по возрастающему радиусу
    for ir in range(0, Nr + 1):
        for ifi in range(0, NFi + 1):
            vertices.append(data.Vertex(x = (Ir + hr * ir) * math.cos(start_angle - ifi * hfi),
                                        y = (Ir + hr * ir) * math.sin(start_angle - ifi * hfi)))

    return vertices


def convert_2d_matrix_indices_to_1d_matrix_index(i : int, j : int, m : int):
    """
    Переводит двумерный индекс в одномерный (массив представляет собой матрицу m x n, последний размер не важен).
    """
    return i * (m + 1) + j


def make_vertices_indices_like_triangle_for_elements_of_grid(vertices : list[data.Vertex], layer_size : int, column_size : int):
    """
    Создаёт в Элементах массив индексов на Вершины таким образом, что Элемент считается треугольником.
    """
    elements = []
    # заполняем элементы сетки
    for iy in range(0, column_size):
        for ix in range(0, layer_size):
            element_right = data.Element()
            element_right.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size))
            element_right.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix + 1, layer_size))
            element_right.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, layer_size))
            elements.append(element_right)
            element_left = data.Element()
            element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size))
            element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, layer_size))
            element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix, layer_size))
            elements.append(element_left)


    return elements


def make_vertices_indices_like_rectangular_for_elements_of_grid(vertices : list[data.Vertex], layer_size : int, column_size : int):
    """
    Создаёт прямоугольную сетку.
    """
    elements = []
    # заполняем элементы сетки
    for iy in range(0, column_size):
        for ix in range(0, layer_size):
            element = data.Element()
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size))
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix + 1, layer_size))
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, layer_size))
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix, layer_size))
            elements.append(element)


    return elements


def make_grid():
    """
    Считывает из консоли данные в следующем формате: Grid_Type(0 - RECTANGULAR, 1 - RADIAL)
    Lx, Ly, Nx, Ny, Element_Type(0 - TRIANGLE, 1 - RECTANGLE). - Если Grid_Type == GridType.RECTANGULAR
    Ir, Or, Nr, Nfi, Element_Type(0 - TRIANGLE, 1 - RECTANGLE). - Если Grid_Type == GridType.RADIAL
    Где:
    Grid_Type - тип сетки.
    Lx, Ly - размеры прямоугольной сетки. (Ir, Or - внутренний и внешний радиусы)
    Nx, Ny - количество разбиений по каждой оси у прямоугольной сетки. (Nr, NFi - количество разбиений по радиусу и углу)
    Element_Type - тип ячеек сетки.

    Далее вызывают соответствующую типу сетки функцию её создания.
    При некорректном считывании данных возвращает None.

    TODO: добавить считывание ГУ.
    """
    print("Введите тип сетки, т.е. способ расположения узлов: Grid_Type(0 - RECTANGULAR, 1 - RADIAL)")
    Grid_Type = int(input())

    if Grid_Type == data.GridType.RECTANGULAR.value:
        print("Введите данные сетки в следующем формате: Lx, Ly, Nx, Ny, Element_Type(0 - TRIANGLE, 1 - RECTANGLE).")
        try:
            Lx, Ly, Nx, Ny, Element_Type = [float(s) for s in input().split()]

            Lx = max(Lx, 0)
            Ly = max(Ly, 0)
            Nx = int(max(Nx, 1))
            Ny = int(max(Ny, 1))

            grid = data.Grid()
            grid.grid_type = Grid_Type

            grid.vertices = make_rectangular_grid_of_unconnected_vertices(Lx, Ly, Nx, Ny)

            if Element_Type == data.ElementsType.TRIANGLE.value:
                print("Генерируется прямоугольная сетка с элементами типа Треугольник")
                grid.elements_type = Element_Type
                grid.elements = make_vertices_indices_like_triangle_for_elements_of_grid(grid.vertices, Nx, Ny)
                return grid

            if Element_Type == data.ElementsType.RECTANGLE.value:
                print("Генерируется прямоугольная сетка с элементами типа Прямоугольник")
                grid.elements_type = Element_Type
                grid.elements = make_vertices_indices_like_rectangular_for_elements_of_grid(grid.vertices, Nx, Ny)
                return grid

            print("Неизвестный тип Элементов сетки!")
            return None

        except ValueError :
            print("Ошибка при считывании данных сетки!")
            return None

    elif Grid_Type == data.GridType.RADIAL.value:
        print("Введите данные сетки в следующем формате: Ir, Or, Nr, NFi, Element_Type(0 - TRIANGLE, 1 - RECTANGLE).")
        try:
            Ir, Or, Nr, NFi, Element_Type = [float(s) for s in input().split()]

            Ir = max(Ir, 0)
            Or = max(Or, 0)
            Nr = int(max(Nr, 1))
            NFi = int(max(NFi, 1))

            grid = data.Grid()
            grid.grid_type = Grid_Type

            grid.vertices = make_radial_grid_of_unconnected_vertices(Ir, Or, Nr, NFi)

            if Element_Type == data.ElementsType.TRIANGLE.value:
                print("Генерируется радиальная сетка с элементами типа Треугольник")
                grid.elements_type = Element_Type
                grid.elements = make_vertices_indices_like_triangle_for_elements_of_grid(grid.vertices, NFi, Nr)
                return grid

            if Element_Type == data.ElementsType.RECTANGLE.value:
                print("Генерируется радиальная сетка с элементами типа Прямоугольник")
                grid.elements_type = Element_Type
                grid.elements = make_vertices_indices_like_rectangular_for_elements_of_grid(grid.vertices, NFi, Nr)
                return grid

            print("Неизвестный тип Элементов сетки!")
            return None

        except ValueError:
            print("Ошибка при считывании данных сетки!")
            return None

    print("Выбран недопустимый тип сетки!")
    return None


def make_triangles_from_grid(grid : data.Grid):
    triangles = []

    if grid.elements_type == data.ElementsType.TRIANGLE.value:
        for element in grid.elements:
            triangles.append(element.vertices_ids)
    elif grid.elements_type == data.ElementsType.RECTANGLE.value:
        for element in grid.elements:
            triangles.append([element.vertices_ids[0], element.vertices_ids[1], element.vertices_ids[2]])
            triangles.append([element.vertices_ids[0], element.vertices_ids[2], element.vertices_ids[3]])

    return triangles


def draw_grid(grid : data.Grid, ax):
    """
    Подготавливает сетку к отрисовке и рисует.
    """
    x = []
    y = []
    for vert in grid.vertices:
        x.append(vert.x)
        y.append(vert.y)

    triangles = make_triangles_from_grid(grid)

    ax.triplot(x, y, triangles)


def draw_function_on_grid(grid : data.Grid, f, ax):
    """
    Подготавливает сетку к отрисовке и рисует на ней функцию.
    """
    x = []
    y = []
    z = []
    for vert in grid.vertices:
        x.append(vert.x)
        y.append(vert.y)
        z.append(f(vert.x, vert.y))

    triangles = make_triangles_from_grid(grid)

    ax.tripcolor(x, y, z, triangles=triangles)


def random_grid_translation(grid : data.Grid):
    for vert in grid.vertices:
        vert.x += -0.5 + random.random()
        vert.y += -0.5 + random.random()