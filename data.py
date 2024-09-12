from enum import Enum


class Material:
    """
    Определяет свойства материала.
    TODO: добавить информацию о материале (какую?)
    """
    pass


class Vertex:
    """
    Определяет координаты вершины на плоскости.
    TODO: добавить информацию о принадлежности ГУ
    """
    def __init__(self, x : float = 0, y : float = 0):
        self.x = x
        self.y = y


class Element:
    """
    Определяет структуру произвольного Элемента.
    Содержит массив индексов своих вершин, расположенных в определённом порядке (обходе).
    !! Индексы действительны только в пределах сетки, содержащей данные элементы и все их вершины. !!
    Содержит свой тип.
    Содержит информацию о материале, из которого состоит.
    """
    def __init__(self, material : Material = None):
        self.vertices_ids = list[int]()
        self.material = material


    def __len__(self):
        return len(self.vertices_ids)


    def __setitem__(self, key : int, value : int):
        self.vertices_ids[key] = value


    def __getitem__(self, item : int):
        return self.vertices_ids[item]


class ElementsType(Enum):
    """
    Определяет тип Элементов сетки.
    """
    TRIANGLE = 0
    RECTANGLE = 1


class Grid:
    """
    Определяет структуру сетки.
    Содержит размеры сетки и шаги разбиения.
    Содержит общий массив вершин.
    Содержит массив элементов, состоящих из хранящихся в сетке вершин и их общий тип.
    """
    def __init__(self,
                 Lx : int,
                 Ly : int,
                 Nx : int,
                 Ny : int,
                 elements_type : ElementsType = ElementsType.TRIANGLE):
        self.Lx = Lx
        self.Ly = Ly
        self.Ny = Ny
        self.Nx = Nx
        self.vertices = list[Vertex]()
        self.elements = list[Element]()
        self.elements_type = elements_type

