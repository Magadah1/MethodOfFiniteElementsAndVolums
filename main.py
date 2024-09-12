import numpy as np
import pyamg
import matplotlib.pyplot as plt

import data_functions


def main():
    grid = data_functions.make_grid()

    for vertex in grid.vertices:
        print(f"x={vertex.x};y={vertex.y}")

    for i, element in enumerate(grid.elements):
        print(f"element#{i}")
        for vertex_id in element.vertices_ids:
            vertex = grid.vertices[vertex_id]
            print(f"x={vertex.x};y={vertex.y}", end=' _ ')
        print()


if __name__ == '__main__':
    main()
