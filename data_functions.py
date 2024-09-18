import math
import random

import data


def get_angle_between_vectors_in_degrees(v1 : data.Vertex, v2 : data.Vertex):
    """
    Определяет угол (в градусах) между двумя векторами.
    :param v1:
    :param v2:
    :return:
    """
    v1_l = math.sqrt(v1.x ** 2 + v1.y ** 2)
    v2_l = math.sqrt(v2.x ** 2 + v2.y ** 2)

    like_cos = min(1.0, max(0.0, (v1.x * v2.x + v1.y * v2.y) / (v1_l * v2_l))) # из-за ошибок округления можем выйти за значения cos

    angle_in_radians = math.acos(like_cos)

    return angle_in_radians * 180 / math.pi


def make_rectangular_grid_of_unconnected_vertices(Lx : float, Ly : float, Nx : int, Ny : int):
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


def make_radial_grid_of_unconnected_vertices(Ir : float, Or : float, Nr : int, NFi : int):
    """
    Создаёт радиальную сетку из вершин в нужном количестве и с нужными шагами. Центр в (0, 0).
    """
    vertices = list[data.Vertex]()

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
    elements = list[data.Element]()
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
    elements = list[data.Element]()
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


def fill_vertices_in_edges_in_grid_of_triangle(layer_size : int, column_size : int):
    """
    Заполняет узлы, из которых состоит ребро. Элементы представляют собой Треугольники.
    Отдельно обрабатывает "верхний" и "правый" слои.
    """
    edges = list[data.Edge]()

    for iy in range(0, column_size):
        for ix in range(0, layer_size):
            edges.append(data.Edge(
                v1 = convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size),
                v2 = convert_2d_matrix_indices_to_1d_matrix_index(iy, ix + 1, layer_size)
            ))
            edges.append(data.Edge(
                v1 = convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size),
                v2 = convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix, layer_size)
            ))
            edges.append(data.Edge(
                v1 = convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size),
                v2 = convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, layer_size)
            ))

    for ix in range(0, layer_size):
        edges.append(data.Edge(
            v1 = convert_2d_matrix_indices_to_1d_matrix_index(column_size, ix, layer_size),
            v2 = convert_2d_matrix_indices_to_1d_matrix_index(column_size, ix + 1, layer_size)
        ))

    for iy in range(0, column_size):
        edges.append(data.Edge(
            v1 = convert_2d_matrix_indices_to_1d_matrix_index(iy, layer_size, layer_size),
            v2 = convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, layer_size, layer_size)
        ))

    return edges


def fill_vertices_in_edges_in_grid_of_rectangle(layer_size : int, column_size : int):
    """
    Заполняет узлы, из которых состоит ребро. Элементы представляют собой Прямоугольники.
    Отдельно обрабатывает "верхний" слой.
    """
    edges = list[data.Edge]()

    for iy in range(0, column_size):
        for ix in range(0, layer_size):
            edges.append(data.Edge(
                v1 = convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size),
                v2 = convert_2d_matrix_indices_to_1d_matrix_index(iy, ix + 1, layer_size)
            ))
            edges.append(data.Edge(
                v1 = convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size),
                v2 = convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix, layer_size)
            ))

    for ix in range(0, layer_size):
        edges.append(data.Edge(
            v1 = convert_2d_matrix_indices_to_1d_matrix_index(column_size, ix, layer_size),
            v2 = convert_2d_matrix_indices_to_1d_matrix_index(column_size, ix + 1, layer_size)
        ))

    for iy in range(0, column_size):
        edges.append(data.Edge(
            v1 = convert_2d_matrix_indices_to_1d_matrix_index(iy, layer_size, layer_size),
            v2 = convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, layer_size, layer_size)
        ))

    return edges


def fill_edges_in_element(element : data.Element, grid : data.Grid):
    """
    Заполняет из каких Рёбер состоит конкретный Элемент сетки.
    """
    edges = set()
    for vert_id in element.vertices_ids: # пройдёмся по индексам узлов, из которых состоит элемент
        for edge_id, edge in enumerate(grid.edges): # для каждого из них проверим, в каком ребре он есть
            if edge.v1 == vert_id and edge.v2 in element.vertices_ids: # если найден, то пробуем найти второй узел ребра в текущем элементе
                edges.add(edge_id) # если нашли, то добавляем узел в сет, т.к. могут быть повторы для каждого узла ребра
            elif edge.v2 == vert_id and edge.v1 in element.vertices_ids:
                edges.add(edge_id)

    element.edges_ids = list(edges)


def fill_edges_in_elements(grid : data.Grid):
    """
    Заполняет из каких Рёбер состоят Элементы сетки.
    """
    for element in grid.elements:
        fill_edges_in_element(element, grid)


def fill_left_and_right_elements_in_edge(edge : data.Edge, elements : list[data.Element], grid : data.Grid):
    """
    Заполняет "левый" и "правый" Элементы у конкретного Ребра сетки.
    Размер elements считается равным 2.
    """
    edge_normal : data.Vertex = edge.get_normal(grid.vertices) # считаем вектором
    el1_center : data.Vertex = grid.elements[elements[0]].get_center(grid.vertices)
    el2_center : data.Vertex = grid.elements[elements[1]].get_center(grid.vertices)

    v_from_1_to_2_elements = data.Vertex(
        x = el2_center.x - el1_center.x,
        y = el2_center.y - el1_center.y
    )

    if get_angle_between_vectors_in_degrees(edge_normal, v_from_1_to_2_elements) <= 90: # если угол острый, то el1 - левая
        edge.element_left = elements[0]
        edge.element_right = elements[1]
    else: # угол тупой, значит не сонаправлен нормали
        edge.element_left = elements[1]
        edge.element_right = elements[0]


def fill_elements_in_edges(grid : data.Grid):
    """
    Заполняет "левый" и "правый" Элементы у Рёбер сетки.
    """
    edge_to_cells = {}
    for edge_id, edge in enumerate(grid.edges): # для каждого ребра переберём все элементы
        if edge_id not in edge_to_cells: # будем для ребра записывать номера элементов, которым оно принадлежит
            edge_to_cells[edge_id] = []
        for element_id, element in enumerate(grid.elements):
            if edge_id in element.edges_ids: # если ребро принадлежит элементу, то запишем его индекс
                edge_to_cells[edge_id].append(element_id)
    # теперь определим левые и правые элементы. Если у ребра только один содержащий его элемент, то он - левый
    for edge_id, edge_cells in edge_to_cells.items():
        if len(edge_cells) == 1:
            grid.edges[edge_id].element_left = edge_cells[0]
        elif len(edge_cells) == 2: # ребро по определению не может принадлежать более 2м элементам
            fill_left_and_right_elements_in_edge(grid.edges[edge_id], edge_cells, grid)



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
    TODO: добавить определение левой и правой ячеек.
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
                grid.edges = fill_vertices_in_edges_in_grid_of_triangle(Nx, Ny)
                fill_edges_in_elements(grid)
                fill_elements_in_edges(grid)
                return grid

            if Element_Type == data.ElementsType.RECTANGLE.value:
                print("Генерируется прямоугольная сетка с элементами типа Прямоугольник")
                grid.elements_type = Element_Type
                grid.elements = make_vertices_indices_like_rectangular_for_elements_of_grid(grid.vertices, Nx, Ny)
                grid.edges = fill_vertices_in_edges_in_grid_of_rectangle(Nx, Ny)
                fill_edges_in_elements(grid)
                fill_elements_in_edges(grid)
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
            if Ir == Or:
                print("Нельзя использовать одинаковые внутренний и внешний радиусы! Увеличиваю внешний на 1!")
                Ir += 1
            Nr = int(max(Nr, 1))
            NFi = int(max(NFi, 1))

            grid = data.Grid()
            grid.grid_type = Grid_Type

            grid.vertices = make_radial_grid_of_unconnected_vertices(Ir, Or, Nr, NFi)

            if Element_Type == data.ElementsType.TRIANGLE.value:
                print("Генерируется радиальная сетка с элементами типа Треугольник")
                grid.elements_type = Element_Type
                grid.elements = make_vertices_indices_like_triangle_for_elements_of_grid(grid.vertices, NFi, Nr)
                grid.edges = fill_vertices_in_edges_in_grid_of_triangle(NFi, Nr)
                fill_edges_in_elements(grid)
                fill_elements_in_edges(grid)
                return grid

            if Element_Type == data.ElementsType.RECTANGLE.value:
                print("Генерируется радиальная сетка с элементами типа Прямоугольник")
                grid.elements_type = Element_Type
                grid.elements = make_vertices_indices_like_rectangular_for_elements_of_grid(grid.vertices, NFi, Nr)
                grid.edges = fill_vertices_in_edges_in_grid_of_rectangle(NFi, Nr)
                fill_edges_in_elements(grid)
                fill_elements_in_edges(grid)
                return grid

            print("Неизвестный тип Элементов сетки!")
            return None

        except ValueError:
            print("Ошибка при считывании данных сетки!")
            return None

    print("Выбран недопустимый тип сетки!")
    return None


def make_triangles_from_grid(grid : data.Grid):
    """
    Создаёт массив из массивов индексов на узлы сетке, образующие треугольники в правильном обходе (против часовой стрелки).
    """
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


def draw_function_on_grid(grid : data.Grid, ax):
    """
    Подготавливает сетку к отрисовке и рисует на ней функцию.
    """
    x = []
    y = []
    for vert in grid.vertices:
        x.append(vert.x)
        y.append(vert.y)

    triangles = make_triangles_from_grid(grid)
    grid.calculate_function_on_grid()

    ax.tripcolor(x, y, grid.function_values, triangles=triangles)


def random_grid_translation(grid : data.Grid):
    """
    Случайно смещает узлы сетки.
    """
    for vert in grid.vertices:
        vert.x += -0.5 + random.random()
        vert.y += -0.5 + random.random()