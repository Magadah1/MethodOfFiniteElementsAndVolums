import math
import random

from matplotlib.patches import Polygon

import data


def get_angle_between_vectors_in_degrees(v1 : data.Vertex, v2 : data.Vertex):
    """
    Определяет угол (в градусах) между двумя векторами.
    """
    v1_l = math.sqrt(v1.x ** 2 + v1.y ** 2)
    v2_l = math.sqrt(v2.x ** 2 + v2.y ** 2)

    like_cos = min(1.0, max(-1.0, (v1.x * v2.x + v1.y * v2.y) / (v1_l * v2_l))) # из-за ошибок округления можем выйти за значения cos

    angle_in_radians = math.acos(like_cos)

    return angle_in_radians * 180 / math.pi


def is_vertex_at_boarder(i, j, m, n):
    """
    Определяет, находится ли Вершина с двумерным индексом (i, j) на границе Сетки размеров (m+1, n+1)
    """
    return i == 0 or j == 0 or i == m or j == n


def make_rectangular_grid_of_unconnected_vertices(Lx : float, Ly : float, Nx : int, Ny : int):
    """
    Создаёт прямоугольную Сетку из Вершин в нужном количестве и с нужными шагами.
    """
    vertices = list[data.Vertex]()

    hx = Lx / Nx
    hy = Ly / Ny

    # послойно заполняем матрицу послойно по y
    for iy in range(0, Ny + 1):
        for ix in range(0, Nx + 1):
            vertices.append(data.Vertex(x = 0 + hx * ix,
                                        y = 0 + hy * iy,
                                        is_at_boarder = is_vertex_at_boarder(ix, iy, Nx, Ny)))

    return vertices


def make_radial_grid_of_unconnected_vertices(Ir : float, Or : float, Nr : int, NFi : int):
    """
    Создаёт радиальную Сетку из Вершин в нужном количестве и с нужными шагами. Центр в (0, 0).
    """
    vertices = list[data.Vertex]()

    start_angle = math.pi

    hr = (Or - Ir) / Nr
    hfi = start_angle / NFi

    # послойное заполнение слева направо по возрастающему радиусу
    for ir in range(0, Nr + 1):
        for ifi in range(0, NFi + 1):
            vertices.append(data.Vertex(x = (Ir + hr * ir) * math.cos(start_angle - ifi * hfi),
                                        y = (Ir + hr * ir) * math.sin(start_angle - ifi * hfi),
                                        is_at_boarder = is_vertex_at_boarder(ir, ifi, Nr, NFi)))

    return vertices


def convert_2d_matrix_indices_to_1d_matrix_index(i : int, j : int, m : int):
    """
    Переводит двумерный индекс в одномерный (массив представляет собой матрицу m x n, последний размер не важен).
    """
    return i * (m + 1) + j


def make_vertices_indices_like_triangle_for_elements_of_grid(layer_size : int, column_size : int):
    """
    Создаёт в Элементах массив индексов на Вершины таким образом, что Элемент считается треугольником.
    """
    elements = list[data.Element]()
    # заполняем элементы сетки
    for iy in range(0, column_size):
        for ix in range(0, layer_size):
            element_right = data.Element(element_type = data.ElementType.TRIANGLE)
            element_right.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size))
            element_right.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix + 1, layer_size))
            element_right.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, layer_size))
            elements.append(element_right)
            element_left = data.Element(element_type = data.ElementType.TRIANGLE)
            element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size))
            element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, layer_size))
            element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix, layer_size))
            elements.append(element_left)

    return elements


def make_vertices_indices_like_rectangular_for_elements_of_grid(layer_size : int, column_size : int):
    """
    Создаёт прямоугольную Сетку.
    """
    elements = list[data.Element]()
    # заполняем элементы Сетки
    for iy in range(0, column_size):
        for ix in range(0, layer_size):
            element = data.Element(element_type = data.ElementType.RECTANGLE)
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size))
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix + 1, layer_size))
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, layer_size))
            element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix, layer_size))
            elements.append(element)

    return elements


def make_vertices_indices_like_rectangular_or_triangle_for_elements_of_grid(layer_size : int, column_size : int):
    """
    Создаёт Сетку, Элементы которой либо прямоугольные, либо треугольные
    """
    elements = list[data.Element]()
    # заполняем элементы Сетки
    for iy in range(0, column_size):
        for ix in range(0, layer_size):
            if random.random() >= 0.5: # пусть в таком случае будут прямоугольники
                element = data.Element(element_type = data.ElementType.RECTANGLE)
                element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size))
                element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix + 1, layer_size))
                element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, layer_size))
                element.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix, layer_size))
                elements.append(element)
            else: # а иначе треугольники
                element_right = data.Element(element_type=data.ElementType.TRIANGLE)
                element_right.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size))
                element_right.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix + 1, layer_size))
                element_right.vertices_ids.append( convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, layer_size))
                elements.append(element_right)
                element_left = data.Element(element_type=data.ElementType.TRIANGLE)
                element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy, ix, layer_size))
                element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix + 1, layer_size))
                element_left.vertices_ids.append(convert_2d_matrix_indices_to_1d_matrix_index(iy + 1, ix, layer_size))
                elements.append(element_left)

    return elements


def fill_vertices_in_edges_in_grid_of_triangle(layer_size : int, column_size : int):
    """
    Заполняет Вершины, из которых состоит Ребро. Элементы представляют собой Треугольники.
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
    Заполняет Вершины, из которых состоит Ребро. Элементы представляют собой Прямоугольники.
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
    Заполняет из каких Рёбер состоит конкретный Элемент Сетки.
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
    Заполняет из каких Рёбер состоят Элементы Сетки.
    """
    for element in grid.elements:
        fill_edges_in_element(element, grid)


def fill_left_and_right_elements_in_edge(edge : data.Edge, elements : list[data.Element], grid : data.Grid):
    """
    Заполняет "левый" и "правый" Элементы у конкретного Ребра Сетки.
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
    else: # угол тупой, значит не "сонаправлен" нормали
        edge.element_left = elements[1]
        edge.element_right = elements[0]


def fill_elements_in_edges(grid : data.Grid):
    """
    Заполняет "левый" и "правый" Элементы у Рёбер Сетки.
    """
    edge_to_cells = {}
    for edge_id, edge in enumerate(grid.edges): # для каждого Ребра переберём все Элементы
        if edge_id not in edge_to_cells: # будем для Ребра записывать номера Элементов, которым оно принадлежит
            edge_to_cells[edge_id] = []
        for element_id, element in enumerate(grid.elements):
            if edge_id in element.edges_ids: # если Ребро принадлежит Элементу, то запишем его индекс
                edge_to_cells[edge_id].append(element_id)
    # теперь определим левые и правые Элементы. Если у Ребра только один содержащий его Элемент, то он - левый
    for edge_id, edge_cells in edge_to_cells.items():
        if len(edge_cells) == 1:
            grid.edges[edge_id].element_left = edge_cells[0]
        elif len(edge_cells) == 2: # Ребро по определению не может принадлежать более 2м Элементам
            fill_left_and_right_elements_in_edge(grid.edges[edge_id], edge_cells, grid)



def make_grid():
    """
    Считывает из консоли данные в следующем формате: Grid_Type(0 - RECTANGULAR, 1 - RADIAL)
    Lx, Ly, Nx, Ny, Element_Type(0 - TRIANGLE, 1 - RECTANGLE, 2 - RANDOM). - Если Grid_Type == GridType.RECTANGULAR
    Ir, Or, Nr, Nfi, Element_Type(0 - TRIANGLE, 1 - RECTANGLE, 2 - RANDOM). - Если Grid_Type == GridType.RADIAL
    Где:
    Grid_Type - тип Сетки.
    Lx, Ly - размеры прямоугольной Сетки. (Ir, Or - внутренний и внешний радиусы)
    Nx, Ny - количество разбиений по каждой оси у прямоугольной Сетки. (Nr, NFi - количество разбиений по радиусу и углу)
    Element_Type - тип Элементов Сетки.

    Далее вызывают соответствующую типу Сетки функцию её создания.
    При некорректном считывании данных возвращает None.

    TODO: добавить считывание ГУ.
    TODO: добавить определение левой и правой ячеек.
    """
    print("Введите тип Сетки, т.е. способ расположения Вершин: Grid_Type(0 - RECTANGULAR, 1 - RADIAL)")
    Grid_Type = int(input())

    if Grid_Type == data.GridType.RECTANGULAR.value:
        print("Введите данные Сетки в следующем формате: Lx, Ly, Nx, Ny, Element_Type(0 - TRIANGLE, 1 - RECTANGLE, 2 - RANDOM).")
        try:
            Lx, Ly, Nx, Ny, Element_Type = [float(s) for s in input().split()]

            Lx = max(Lx, 0)
            Ly = max(Ly, 0)
            Nx = int(max(Nx, 1))
            Ny = int(max(Ny, 1))

            grid = data.Grid()
            grid.grid_type = Grid_Type

            grid.vertices = make_rectangular_grid_of_unconnected_vertices(Lx, Ly, Nx, Ny)

            if Element_Type == data.ElementType.TRIANGLE.value:
                print("Генерируется прямоугольная Сетка с Элементами типа Треугольник")
                grid.elements = make_vertices_indices_like_triangle_for_elements_of_grid(Nx, Ny)
                grid.edges = fill_vertices_in_edges_in_grid_of_triangle(Nx, Ny)
                fill_edges_in_elements(grid)
                fill_elements_in_edges(grid)
                return grid

            if Element_Type == data.ElementType.RECTANGLE.value:
                print("Генерируется прямоугольная Сетка с Элементами типа Прямоугольник")
                grid.elements = make_vertices_indices_like_rectangular_for_elements_of_grid(Nx, Ny)
                grid.edges = fill_vertices_in_edges_in_grid_of_rectangle(Nx, Ny)
                fill_edges_in_elements(grid)
                fill_elements_in_edges(grid)
                return grid

            if Element_Type == data.ElementType.RANDOM.value:
                print("Генерируется прямоугольная Сетка с Элементами произвольных типов")
                grid.elements = make_vertices_indices_like_rectangular_or_triangle_for_elements_of_grid(Nx, Ny)
                grid.edges = fill_vertices_in_edges_in_grid_of_rectangle(Nx, Ny)
                fill_edges_in_elements(grid)
                fill_elements_in_edges(grid)
                return grid

            print("Неизвестный тип Элементов Сетки!")
            return None

        except ValueError :
            print("Ошибка при считывании данных Сетки!")
            return None

    elif Grid_Type == data.GridType.RADIAL.value:
        print("Введите данные Сетки в следующем формате: Ir, Or, Nr, NFi, Element_Type(0 - TRIANGLE, 1 - RECTANGLE).")
        try:
            Ir, Or, Nr, NFi, Element_Type = [float(s) for s in input().split()]

            Ir = max(Ir, 0)
            Or = max(Or, 0)
            if Ir == Or:
                print("Нельзя использовать одинаковые внутренний и внешний радиусы! Увеличиваю внешний на 1!")
                Or += 1
            Nr = int(max(Nr, 1))
            NFi = int(max(NFi, 1))

            grid = data.Grid()
            grid.grid_type = Grid_Type

            grid.vertices = make_radial_grid_of_unconnected_vertices(Ir, Or, Nr, NFi)

            if Element_Type == data.ElementType.TRIANGLE.value:
                print("Генерируется радиальная Сетка с Элементами типа Треугольник")
                grid.elements = make_vertices_indices_like_triangle_for_elements_of_grid(NFi, Nr)
                grid.edges = fill_vertices_in_edges_in_grid_of_triangle(NFi, Nr)
                fill_edges_in_elements(grid)
                fill_elements_in_edges(grid)
                return grid

            if Element_Type == data.ElementType.RECTANGLE.value:
                print("Генерируется радиальная Сетка с Элементами типа Прямоугольник")
                grid.elements = make_vertices_indices_like_rectangular_for_elements_of_grid(NFi, Nr)
                grid.edges = fill_vertices_in_edges_in_grid_of_rectangle(NFi, Nr)
                fill_edges_in_elements(grid)
                fill_elements_in_edges(grid)
                return grid

            if Element_Type == data.ElementType.RANDOM.value:
                print("Генерируется радиальная Сетка с Элементами произвольных типов")
                grid.elements = make_vertices_indices_like_rectangular_or_triangle_for_elements_of_grid(NFi, Nr)
                grid.edges = fill_vertices_in_edges_in_grid_of_rectangle(NFi, Nr)
                fill_edges_in_elements(grid)
                fill_elements_in_edges(grid)
                return grid

            print("Неизвестный тип Элементов Сетки!")
            return None

        except ValueError:
            print("Ошибка при считывании данных Сетки!")
            return None

    print("Выбран недопустимый тип Сетки!")
    return None


def make_triangles_from_grid(grid : data.Grid):
    """
    Создаёт массив из массивов индексов на Вершины Сетки, образующие треугольники в правильном обходе (против часовой стрелки).
    """
    triangles = []

    for element in grid.elements:
        if element.type == data.ElementType.TRIANGLE:
            triangles.append(element.vertices_ids)
        elif element.type == data.ElementType.RECTANGLE:
            triangles.append([element.vertices_ids[0], element.vertices_ids[1], element.vertices_ids[2]])
            triangles.append([element.vertices_ids[0], element.vertices_ids[2], element.vertices_ids[3]])

    return triangles


def draw_grid(grid : data.Grid, ax):
    """
    Подготавливает Сетку к отрисовке и рисует.
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
    Подготавливает Сетку к отрисовке и рисует на ней функцию.
    """
    x = []
    y = []
    for vert in grid.vertices:
        x.append(vert.x)
        y.append(vert.y)

    triangles = make_triangles_from_grid(grid)
    grid.calculate_function_on_grid()

    ax.tripcolor(x, y, grid.function_values, triangles=triangles)


def draw_grid_path(grid : data.Grid, ax, plt):
    """
    Отрисовывает Сетку контурно.
    """
    polygons = list[Polygon]()

    min_x, max_x, min_y, max_y = grid.get_min_max_x_y()

    for element in grid.elements:
        element_vertices = []
        for el_ver_id in element.vertices_ids:
            vert = grid.vertices[el_ver_id]
            element_vertices.append((vert.x, vert.y))
        polygons.append(Polygon(element_vertices, fill = False))

    for polygon in polygons:
        ax.add_patch(polygon)

    plt.xlim(min_x * 1.1, max_x * 1.1)
    plt.ylim(min_y * 1.1, max_y * 1.1)


def random_grid_translation(grid : data.Grid):
    """
    Случайно смещает Вершины Сетки.
    """
    for vert in grid.vertices:
        vert.x += -0.5 + random.random()
        vert.y += -0.5 + random.random()