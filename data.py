import math

from enum import Enum
from accessify import private


class Material:
    """
    Определяет свойства материала.
    TODO: добавить информацию о материале (какую?)
    """
    pass


class Vertex:
    """
    Определяет координаты Вершины на плоскости.
    Хранит номер одного из Рёбер, которому принадлежит.
    Хранит информацию о том, является ли граничной.
    """
    def __init__(self, x : float = 0, y : float = 0, is_at_boarder : bool = False):
        self.x = x
        self.y = y
        self.is_at_boarder = is_at_boarder
        self.edge_id = -1


class Edge:
    """
    Определяем Ребро, как две связанные Вершины. Хранит информацию об Элементе слева и справа.
    """
    def __init__(self, v1 : int = -1, v2 : int = -1):
        self.v1 = v1
        self.v2 = v2
        self.element_left = -1
        self.element_right = -1


    def length(self, vertices : list[Vertex]):
        """
        Возвращает длину Ребра.
        Из-за специфики хранения данных требует массив Вершин, из 2х из которых состоит Ребро.
        """
        v1 = vertices[self.v1]
        v2 = vertices[self.v2]
        return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2)


    def get_normal(self, vertices : list[Vertex]):
        """
        Возвращает случайную единичную нормаль к Ребру.
        Из-за специфики хранения данных требует массив Вершин, из 2х из которых состоит Ребро.
        """
        x = vertices[self.v2].x - vertices[self.v1].x
        y = vertices[self.v2].y - vertices[self.v1].y
        l = math.sqrt(x ** 2 + y ** 2)
        if l < 1e-9:
            return None
        x /= l
        y /= l
        return Vertex(-y, x) # возвращается "Вершина", которую нужно считать как вектор.


class Element:
    """
    Определяет структуру произвольного Элемента.
    Содержит массив индексов своих Вершин, расположенных в определённом порядке (обходе).
    !! Индексы действительны только в пределах Сетки, содержащей данные Элементы и все их Вершины. !!
    Содержит массив индексов своих Рёбер в произвольном порядке.
    """
    def __init__(self):
        self.vertices_ids = []
        self.edges_ids = []


    def get_center(self, vertices : list[Vertex]):
        """
        Возвращает центр Элемента.
        """
        center = Vertex()
        for v_id in self.vertices_ids:
            v = vertices[v_id]
            center.x += v.x
            center.y += v.y

        l = len(self.vertices_ids)
        if l == 0:
            return None

        center.x /= l
        center.y /= l

        return center


    def get_area(self, vertices : list[Vertex]):
        """
        Возвращает площадь Элемента.
        """
        if len(self.vertices_ids) == 3:
            return self.get_triangle_area(vertices)

        if len(self.vertices_ids) == 4:
            return self.get_rectangle_area(vertices)

        return -1


    @private
    def get_triangle_area_implementation(self, v1_id, v2_id, v3_id, vertices : list[Vertex]):
        """
        Реализация вычисления площади плоского треугольника.
        Из-за специфики хранения данных требует массив Вершин, из которых состоит Элемент.
        """
        vl = vertices[v1_id]
        vm = vertices[v2_id]
        vn = vertices[v3_id]

        return 0.5 * math.fabs(
            (vl.x - vn.x) * (vm.y - vn.y) - (vm.x - vn.x) * (vl.y - vn.y)
        )


    @private
    def get_triangle_area(self, vertices : list[Vertex]):
        """
        Возвращает площадь Элемента формы Треугольник.
        Из-за специфики хранения данных требует массив Вершин, из которых состоит Элемент.
        """
        return self.get_triangle_area_implementation(self.vertices_ids[0],
                                                     self.vertices_ids[1],
                                                     self.vertices_ids[2],
                                                     vertices)


    @private
    def get_rectangle_area(self, vertices : list[Vertex]):
        """
        Возвращает площадь Элемента формы Прямоугольник.
        Из-за специфики хранения данных требует массив Вершин, из которых состоит Элемент.
        """
        return (self.get_triangle_area_implementation(self.vertices_ids[0],
                                                     self.vertices_ids[1],
                                                     self.vertices_ids[2],
                                                     vertices)
                + self.get_triangle_area_implementation(self.vertices_ids[0],
                                                        self.vertices_ids[2],
                                                        self.vertices_ids[3],
                                                        vertices))


class ElementsType(Enum):
    """
    Определяет тип Элементов сетки.
    """
    TRIANGLE = 0
    RECTANGLE = 1


class GridType(Enum):
    """
    Определяет тип Сетки
    """
    RECTANGULAR = 0
    RADIAL = 1


class Grid:
    """
    Определяет структуру сетки.
    Содержит общий массив Вершин и тип их расположения. А также массив значений некоторой функции в них.
    Содержит массив Рёбер.
    Содержит массив Элементов, состоящих из хранящихся в сетке Вершин и их общий тип.
    """
    def __init__(self, grid_type : GridType = GridType.RECTANGULAR, elements_type : ElementsType = ElementsType.TRIANGLE):
        self.vertices = list[Vertex]()
        self.function_values = list[float]()
        self.function = None
        self.elements = list[Element]()
        self.edges = list[Edge]()
        self.grid_type = grid_type
        self.elements_type = elements_type


    def get_area(self):
        """
        Возвращает суммарную площадь всей Сетки.
        """
        return sum([el.get_area(self.vertices) for el in self.elements])


    def get_vertex_edges(self, v_id):
        """
        Возвращает список индексов всех Рёбер, которым принадлежит Вершина с заданным индексом.
        Их порядок произвольный относительно Вершины.
        """
        edges = []
        for edge_id, edge in enumerate(self.edges):
            if edge.v1 == v_id or edge.v2 == v_id:
                edges.append(edge_id)

        return edges


    def get_vertex_elements(self, v_id):
        """
        Возвращает список индексов всех Элементов, которым принадлежит Вершина с заданным индексом.
        Их порядок произвольный относительно Вершины.
        """
        elements = []
        for el_id, el in enumerate(self.elements):
            if v_id in el.vertices_ids:
                elements.append(el_id)

        return elements


    def set_grid_function(self, f):
        """
        Устанавливает функцию, действующую на Сетку.
        """
        self.function = f


    def calculate_function_on_grid(self):
        """
        Вычисляет значения заданной функции на Сетке.
        """
        self.function_values.clear()
        if self.function is None:
            return
        for vert in self.vertices:
            self.function_values.append(self.function(vert.x, vert.y))