import math

from enum import Enum
from accessify import private

import data


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
    Если Ребро граничное, то "правый элемент" равен "-1".
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


    def get_center(self, vertices : list[Vertex]):
        """
        Возвращает центр Ребра.
        Из-за специфики хранения данных требует массив Вершин, из 2х из которых состоит Ребро.
        """
        v1 = vertices[self.v1]
        v2 = vertices[self.v2]

        return Vertex((v1.x + v2.x) / 2, (v1.y + v2.y) / 2)


class MedianEdge:
    """
    Определяет структуру Медианного Ребра, получаемого в результате (средне)медианного разбиения.
    Явно хранит индексы на свои Вершины и номер соседней Вершины исходной сетки.
    !! Индексы на свои Вершины валидны лишь в пределах Медианного Элемента. !!
    """
    def __init__(self, v1 : int, v2 : int, next_vertex : int):
        self.v1 = v1
        self.v2 = v2
        self.next_vertex = next_vertex


class ElementType(Enum):
    """
    Определяет тип Элемента сетки.
    """
    TRIANGLE = 0
    RECTANGLE = 1
    RANDOM = 2 # специальный тип, преобразуемый в один из вышеперечисленных



class Element:
    """
    Определяет структуру произвольного Элемента.
    Содержит массив индексов своих Вершин, расположенных в определённом порядке (обходе).
    !! Индексы действительны только в пределах Сетки, содержащей данные Элементы и все их Вершины. !!
    Содержит массив индексов своих Рёбер в произвольном порядке.
    Содержит сведения о типе Элемента.
    """
    def __init__(self, element_type : ElementType):
        self.vertices_ids = []
        self.edges_ids = []
        self.type = element_type


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


    def __and__(self, other):
        """
        Перегружает оператор "&". Возвращает индекс общего Ребра двух Элементов. Если нет общего Ребра - возвращает None.
        НЕИСПОЛЬЗУЕТСЯ
        """
        for edge_id in self.edges_ids:
            if edge_id in other.edges_ids:
                return edge_id

        return None


    def is_at_border(self, edges : list[data.Edge]):
        """
        Определяет, является ли элемент граничным.
        """
        for edge_id in self.edges_ids:
            edge = edges[edge_id]
            if edge.element_right == -1:
                return True

        return False


    def get_area(self, vertices : list[Vertex]):
        """
        Возвращает площадь Элемента.
        """
        if self.type == ElementType.TRIANGLE:
            return self.get_triangle_area(vertices)

        if self.type == ElementType.RECTANGLE:
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


class MedianElement:
    """
    Определяет структуру Медианного Элемента, получаемого в результате (средне)медианного разбиения.
    Хранит массивы Вершин и Рёбер, из которых состоит.
    !! Вершины расположены в определённом обходе, но (по крайней мере пока что) сам обход неоднозначен. !!
    """
    def __init__(self):
        self.vertices = list[Vertex]()
        self.edges = list[MedianEdge]()


class GridType(Enum):
    """
    Определяет тип Сетки.
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
    def __init__(self, grid_type : GridType = GridType.RECTANGULAR):
        self.vertices = list[Vertex]()
        self.function_values = list[float]()
        self.function = None
        self.elements = list[Element]()
        self.edges = list[Edge]()
        self.grid_type = grid_type


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


    def get_vertex_median_element(self, v_id):
        """
        Возвращает для заданной Вершины её Медианный Элемент.
        """
        if self.vertices[v_id].is_at_boarder:
            return self.get_vertex_median_element_at_boarder(v_id)
        else:
            return self.get_vertex_median_element_not_at_boarder(v_id)


    @private
    def get_vertex_median_element_not_at_boarder(self, v_id):
        """
        Возвращает для заданной неграничной Вершины её Медианный Элемент.
        """
        vertex_elements_ids = self.get_vertex_elements(v_id)

        # Принцип алгоритма такой:
        # 1. Берём произвольный Элемент у Вершины в качестве опорного.
        # 2. Для него ищем один из следующих соседних Элементов из массива vertex_elements_ids, который ещё не использовался.
        # 3. По ним получаем первое Медианное Ребро, для которого определим номер следующей (соседней) Вершины исходной сетки.
        # 4. В качестве опорного элемента выбираем номер Элемента из п.2. и повторяем п. 2 - 4 до тех пор, пока опять не возьмём Элемент из п. 1.
        # В итоге получим Медианный Элемент, Вершины которого расположены в определённом, но произвольном, обходе.

        median_element = MedianElement()
        median_element.vertices.append(self.elements[vertex_elements_ids[0]].get_center(self.vertices))
        pivot_el_id = vertex_elements_ids[0]
        prev_el_id = -1

        while True: # питонячий аналог Do While
            cur_el = self.elements[pivot_el_id] # 1
            next_el_id = -1
            next_vertex_id_in_median_edge = -1
            for cur_el_edge_id in cur_el.edges_ids:
                cur_el_edge = self.edges[cur_el_edge_id]
                possible_next_el_id = cur_el_edge.element_left if cur_el_edge.element_right == pivot_el_id else cur_el_edge.element_right
                if possible_next_el_id != prev_el_id and possible_next_el_id in vertex_elements_ids: # 2
                    next_el_id = possible_next_el_id
                    next_vertex_id_in_median_edge = cur_el_edge.v1 if cur_el_edge.v2 == v_id else cur_el_edge.v2
                    break

            if next_el_id == vertex_elements_ids[0]:
                median_element.edges.append(MedianEdge(
                    len(median_element.vertices) - 1,
                    0,
                    next_vertex_id_in_median_edge
                ))
                break
            else:
                median_element.vertices.append(self.elements[next_el_id].get_center(self.vertices))
                median_element.edges.append(MedianEdge( # 3
                    len(median_element.vertices) - 2,
                    len(median_element.vertices) - 1,
                    next_vertex_id_in_median_edge
                ))
                prev_el_id = pivot_el_id # 4
                pivot_el_id = next_el_id

        return median_element


    @private
    def get_vertex_median_element_at_boarder(self, v_id):
        """
        Возвращает для заданной граничной Вершины её Медианный Элемент.
        """
        vertex_elements_ids = self.get_vertex_elements(v_id)
        vertex_edges_ids = self.get_vertex_edges(v_id)

        # Принцип алгоритма такой:
        # 1. Находим одно из граничных Рёбер, которому принадлежит стартовая Вершина. К его середине пойдёт первое Медианное Ребро.
        # 2. Находим Элемент, которому принадлежит Ребро из п.1., и добавим второе Медианное Ребро.
        # 3. Применим адаптированный в данном случае алгоритм для неграничных Вершин.
        # 4. Найдём оставшееся граничное Ребро и добавим последние Медианные Рёбра, через его середину.
        # Медианные Рёбра из п.1. и п.4. (и те Медианные Рёбра, которые отходят от их центров к центрам их Элементов)
        # в качестве следующей (соседней) Вершины будут иметь оставшиеся Вершины, составляющие эти Рёбра.

        median_element = MedianElement()
        median_element.vertices.append(self.vertices[v_id])

        first_boarder_edge_id = -1
        for vertex_edges_id in vertex_edges_ids:
            edge = self.edges[vertex_edges_id]
            if (edge.v1 == v_id or edge.v2 == v_id) and edge.element_right == -1: # 1
                first_boarder_edge_id = vertex_edges_id
                break

        first_boarder_edge = self.edges[first_boarder_edge_id]
        median_element.vertices.append(self.edges[first_boarder_edge_id].get_center(self.vertices))
        median_element.edges.append(MedianEdge(
            0, 1,
            first_boarder_edge.v1 if first_boarder_edge.v2 == v_id else first_boarder_edge.v2
        )) # добавил Медианное Ребро, равное половине случайного граничного Ребра, которому принадлежит заданная Вершина

        pivot_el_id = -1
        for vertex_elements_id in vertex_elements_ids:
            element = self.elements[vertex_elements_id]
            if first_boarder_edge_id in element.edges_ids: # 2
                pivot_el_id = vertex_elements_id
                break

        median_element.vertices.append(self.elements[pivot_el_id].get_center(self.vertices))
        median_element.edges.append(MedianEdge(
            1, 2,
            first_boarder_edge.v1 if first_boarder_edge.v2 == v_id else first_boarder_edge.v2
        ))

        prev_el_id = -1

        while True: # 3
            cur_el = self.elements[pivot_el_id]
            next_el_id = -1
            next_vertex_id_in_median_edge = -1
            for cur_el_edge_id in cur_el.edges_ids:
                cur_el_edge = self.edges[cur_el_edge_id]
                possible_next_el_id = cur_el_edge.element_left if cur_el_edge.element_right == pivot_el_id else cur_el_edge.element_right
                if possible_next_el_id != prev_el_id and possible_next_el_id in vertex_elements_ids:
                    next_el_id = possible_next_el_id
                    next_vertex_id_in_median_edge = cur_el_edge.v1 if cur_el_edge.v2 == v_id else cur_el_edge.v2
                    break

            if next_el_id == -1: # 4
                last_boarder_edge_id = -1
                for vertex_edges_id in vertex_edges_ids:
                    edge = self.edges[vertex_edges_id]
                    if vertex_edges_id != first_boarder_edge_id and (edge.v1 == v_id or edge.v2 == v_id) and edge.element_right == -1:
                        last_boarder_edge_id = vertex_edges_id
                        break

                last_boarder_edge = self.edges[last_boarder_edge_id]
                median_element.vertices.append(self.edges[last_boarder_edge_id].get_center(self.vertices))
                median_element.edges.append(MedianEdge(
                    len(median_element.vertices) - 2,
                    len(median_element.vertices) - 1,
                    last_boarder_edge.v1 if last_boarder_edge.v2 == v_id else last_boarder_edge.v2
                ))
                median_element.edges.append(MedianEdge(
                    len(median_element.vertices) - 1,
                    0,
                    last_boarder_edge.v1 if last_boarder_edge.v2 == v_id else last_boarder_edge.v2
                ))
                break
            else:
                median_element.vertices.append(self.elements[next_el_id].get_center(self.vertices))
                median_element.edges.append(MedianEdge(
                    len(median_element.vertices) - 2,
                    len(median_element.vertices) - 1,
                    next_vertex_id_in_median_edge
                ))
                prev_el_id = pivot_el_id
                pivot_el_id = next_el_id

        return median_element


    def get_vertex_mean_median_element(self, v_id):
        """
        Возвращает для заданной Вершины её Средне Медианный Элемент.
        """
        if self.vertices[v_id].is_at_boarder:
            return self.get_vertex_mean_median_element_at_boarder(v_id)
        else:
            return self.get_vertex_mean_median_element_not_at_boarder(v_id)


    @private
    def get_vertex_mean_median_element_not_at_boarder(self, v_id):
        """
        Возвращает для заданной неграничной Вершины её Средне Медианный Элемент.
        """
        vertex_elements_ids = self.get_vertex_elements(v_id)

        # Принцип алгоритма такой:
        # 1. Берём произвольный Элемент у Вершины в качестве опорного.
        # 2. Для него ищем один из следующих соседних Элементов из массива vertex_elements_ids, который ещё не использовался.
        # 3. По ним получаем первые Средне Медианные Рёбра, для которых определим номер следующей (соседней) Вершины исходной сетки.
        # 4. В качестве опорного элемента выбираем номер Элемента из п.2. и повторяем п. 2 - 4 до тех пор, пока опять не возьмём Элемент из п. 1.
        # В итоге получим Средне Медианный Элемент, Вершины которого расположены в определённом, но произвольном, обходе.

        mean_median_element = MedianElement()
        mean_median_element.vertices.append(self.elements[vertex_elements_ids[0]].get_center(self.vertices))
        pivot_el_id = vertex_elements_ids[0]
        prev_el_id = -1

        while True:  # питонячий аналог Do While
            cur_el = self.elements[pivot_el_id]  # 1
            next_el_id = -1
            next_vertex_id_in_mean_median_edge = -1
            middle_vertex = None
            for cur_el_edge_id in cur_el.edges_ids:
                cur_el_edge = self.edges[cur_el_edge_id]
                possible_next_el_id = cur_el_edge.element_left if cur_el_edge.element_right == pivot_el_id else cur_el_edge.element_right
                if possible_next_el_id != prev_el_id and possible_next_el_id in vertex_elements_ids:  # 2
                    next_el_id = possible_next_el_id
                    next_vertex_id_in_mean_median_edge = cur_el_edge.v1 if cur_el_edge.v2 == v_id else cur_el_edge.v2
                    middle_vertex = cur_el_edge.get_center(self.vertices)
                    break

            if next_el_id == vertex_elements_ids[0]:
                mean_median_element.vertices.append(middle_vertex)
                mean_median_element.edges.append(MedianEdge(
                    len(mean_median_element.vertices) - 2,
                    len(mean_median_element.vertices) - 1,
                    next_vertex_id_in_mean_median_edge
                ))
                mean_median_element.edges.append(MedianEdge(
                    len(mean_median_element.vertices) - 1,
                    0,
                    next_vertex_id_in_mean_median_edge
                ))
                break
            else:
                mean_median_element.vertices.append(middle_vertex)
                mean_median_element.edges.append(MedianEdge(
                    len(mean_median_element.vertices) - 2,
                    len(mean_median_element.vertices) - 1,
                    next_vertex_id_in_mean_median_edge
                ))
                mean_median_element.vertices.append(self.elements[next_el_id].get_center(self.vertices))
                mean_median_element.edges.append(MedianEdge(
                    len(mean_median_element.vertices) - 2,
                    len(mean_median_element.vertices) - 1,
                    next_vertex_id_in_mean_median_edge
                ))
                prev_el_id = pivot_el_id  # 4
                pivot_el_id = next_el_id

        return mean_median_element


    @private
    def get_vertex_mean_median_element_at_boarder(self, v_id):
        """
        Возвращает для заданной граничной Вершины её Средне Медианный Элемент.
        """
        vertex_elements_ids = self.get_vertex_elements(v_id)
        vertex_edges_ids = self.get_vertex_edges(v_id)

        # Принцип алгоритма такой:
        # 1. Находим одно из граничных Рёбер, которому принадлежит стартовая Вершина. К его середине пойдёт первое Средне Медианное Ребро.
        # 2. Находим Элемент, которому принадлежит Ребро из п.1., и добавим второе Средне Медианное Ребро.
        # 3. Применим адаптированный в данном случае алгоритм для неграничных Вершин.
        # 4. Найдём оставшееся граничное Ребро и добавим последние Средне Медианные Рёбра, через его середину.
        # Средне Медианные Рёбра из п.1. и п.4. (и те Средне Медианные Рёбра, которые отходят от их центров к центрам их Элементов)
        # в качестве следующей (соседней) Вершины будут иметь оставшиеся Вершины, составляющие эти Рёбра.

        mean_median_element = MedianElement()
        mean_median_element.vertices.append(self.vertices[v_id])

        first_boarder_edge_id = -1
        for vertex_edges_id in vertex_edges_ids:
            edge = self.edges[vertex_edges_id]
            if (edge.v1 == v_id or edge.v2 == v_id) and edge.element_right == -1: # 1
                first_boarder_edge_id = vertex_edges_id
                break

        first_boarder_edge = self.edges[first_boarder_edge_id]
        mean_median_element.vertices.append(self.edges[first_boarder_edge_id].get_center(self.vertices))
        mean_median_element.edges.append(MedianEdge(
            0, 1,
            first_boarder_edge.v1 if first_boarder_edge.v2 == v_id else first_boarder_edge.v2
        ))  # добавил Медианное Ребро, равное половине случайного граничного Ребра, которому принадлежит заданная Вершина

        pivot_el_id = -1
        for vertex_elements_id in vertex_elements_ids:
            element = self.elements[vertex_elements_id]
            if first_boarder_edge_id in element.edges_ids:  # 2
                pivot_el_id = vertex_elements_id
                break

        mean_median_element.vertices.append(self.elements[pivot_el_id].get_center(self.vertices))
        mean_median_element.edges.append(MedianEdge(
            1, 2,
            first_boarder_edge.v1 if first_boarder_edge.v2 == v_id else first_boarder_edge.v2
        ))

        prev_el_id = -1

        while True:  # 3
            cur_el = self.elements[pivot_el_id]
            next_el_id = -1
            next_vertex_id_in_median_edge = -1
            middle_vertex = None
            for cur_el_edge_id in cur_el.edges_ids:
                cur_el_edge = self.edges[cur_el_edge_id]
                possible_next_el_id = cur_el_edge.element_left if cur_el_edge.element_right == pivot_el_id else cur_el_edge.element_right
                if possible_next_el_id != prev_el_id and possible_next_el_id in vertex_elements_ids:
                    next_el_id = possible_next_el_id
                    next_vertex_id_in_median_edge = cur_el_edge.v1 if cur_el_edge.v2 == v_id else cur_el_edge.v2
                    middle_vertex = cur_el_edge.get_center(self.vertices)
                    break

            if next_el_id == -1:  # 4
                last_boarder_edge_id = -1
                for vertex_edges_id in vertex_edges_ids:
                    edge = self.edges[vertex_edges_id]
                    if vertex_edges_id != first_boarder_edge_id and (edge.v1 == v_id or edge.v2 == v_id) and edge.element_right == -1:
                        last_boarder_edge_id = vertex_edges_id
                        break

                last_boarder_edge = self.edges[last_boarder_edge_id]
                mean_median_element.vertices.append(self.edges[last_boarder_edge_id].get_center(self.vertices))
                mean_median_element.edges.append(MedianEdge(
                    len(mean_median_element.vertices) - 2,
                    len(mean_median_element.vertices) - 1,
                    last_boarder_edge.v1 if last_boarder_edge.v2 == v_id else last_boarder_edge.v2
                ))
                mean_median_element.edges.append(MedianEdge(
                    len(mean_median_element.vertices) - 1,
                    0,
                    last_boarder_edge.v1 if last_boarder_edge.v2 == v_id else last_boarder_edge.v2
                ))
                break
            else:
                mean_median_element.vertices.append(middle_vertex)
                mean_median_element.edges.append(MedianEdge(
                    len(mean_median_element.vertices) - 2,
                    len(mean_median_element.vertices) - 1,
                    next_vertex_id_in_median_edge
                ))
                mean_median_element.vertices.append(self.elements[next_el_id].get_center(self.vertices))
                mean_median_element.edges.append(MedianEdge(
                    len(mean_median_element.vertices) - 2,
                    len(mean_median_element.vertices) - 1,
                    next_vertex_id_in_median_edge
                ))
                prev_el_id = pivot_el_id
                pivot_el_id = next_el_id

        return mean_median_element

    def get_min_max_x_y(self):
        min_x = 1e9
        max_x = -1e9
        min_y = 1e9
        max_y = -1e9
        for vertex in self.vertices:
            min_x = min(min_x, vertex.x)
            min_y = min(min_y, vertex.y)
            max_x = max(max_x, vertex.x)
            max_y = max(max_y, vertex.y)

        return min_x, max_x, min_y, max_y