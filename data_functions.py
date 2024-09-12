import data
from data import Element


def make_grid_of_unconnected_vertices(Lx : int, Ly : int, Nx : int, Ny : int):
    """
    Создаёт прямоугольную сетку из вершин в нужном количестве и с нужными шагами.
    """
    vertices = list[data.Vertex]()

    hx = Lx / Nx
    hy = Ly / Ny

    # послойно заполняем матрицу послойно по y
    for iy in range(0, Ny + 1):
        for ix in range(0, Nx + 1):
            vertices.append(data.Vertex(x = 0 + hx * ix, y = 0 + hy * iy))

    return vertices


def convert_2d_matrix_indices_to_1d_matrix_index(i : int, j : int, m : int):
    """
    Переводит двумерный индекс в одномерный (массив представляет собой матрицу m x n, последний размер не важен).
    """
    return i * (m + 1) + j


def make_triangle_grid(Lx : int, Ly : int, Nx : int, Ny : int):
    """
    Создаёт треугольную сетку.
    """
    grid = data.Grid(Lx = Lx, Ly = Ly, Nx = Nx, Ny = Ny, elements_type = data.ElementsType.TRIANGLE)

    grid.vertices = make_grid_of_unconnected_vertices(Lx=Lx, Ly=Ly, Nx=Nx, Ny=Ny)

    # заполняем элементы сетки
    for iy in range(0, Ny):
        for ix in range(0, Nx):
            element_right = Element()
            element_right.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, Nx))
            element_right.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix + 1, Nx))
            element_right.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, Nx))
            grid.elements.append(element_right)
            element_left = Element()
            element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, Nx))
            element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, Nx))
            element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix, Nx))
            grid.elements.append(element_left)


    return grid


def make_rectangle_grid(Lx : int, Ly : int, Nx : int, Ny : int):
    """
    Создаёт прямоугольную сетку.
    """
    grid = data.Grid(Lx = Lx, Ly = Ly, Nx = Nx, Ny = Ny, elements_type = data.ElementsType.RECTANGLE)

    grid.vertices = make_grid_of_unconnected_vertices(Lx = Lx, Ly = Ly, Nx = Nx, Ny = Ny)

    # заполняем элементы сетки
    for iy in range(0, Ny):
        for ix in range(0, Nx):
            element = Element()
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, Nx))
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix + 1, Nx))
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, Nx))
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix, Nx))
            grid.elements.append(element)


    return grid


def make_grid():
    """
    Считывает из консоли данные в следующем формате: Lx, Ly, Nx, Ny, Type(0 - TRIANGLE, 1 - RECTANGLE).
    Где:
    Lx, Ly - размеры сетки.
    Nx, Ny - количество разбиений по каждой оси.
    Type - тип ячеек сетки.

    Далее вызывают соответствующую типу сетки функцию её создания.
    При некорректном считывании данных возвращает None.

    TODO: добавить считывание материала элементов и ГУ.
    """
    print("Введите данные сетки в следующем формате: Lx, Ly, Nx, Ny, Type(0 - TRIANGLE, 1 - RECTANGLE).")
    try:
        Lx, Ly, Nx, Ny, Type = [int(s) for s in input().split()]

        Lx = max(Lx, 0)
        Ly = max(Ly, 0)
        Nx = max(Nx, 1)
        Ny = max(Ny, 1)

        if Type == data.ElementsType.TRIANGLE.value:
            print("Генерируется сетка с элементами типа Треугольник")
            return make_triangle_grid(Lx, Ly, Nx, Ny)

        if Type == data.ElementsType.RECTANGLE.value:
            print("Генерируется сетка с элементами типа Прямоугольник")
            return make_rectangle_grid(Lx, Ly, Nx, Ny)

    except ValueError :
        print("Ошибка при считывании данных сетки!")
        return None

    return None
