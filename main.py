import numpy as np
from preprocessing import *
import matplotlib.pyplot as plt


def area_compute(R_poly, L_poly):
    """
    Суммарная площадь не больше площади сетки
    :param R_poly:
    :param L_poly:
    :return: area
    """
    area = 0
    for cur in R_poly:
        area += cur[0][0] * cur[0][1] * cur[1]  # площадь прямоугольника
    for cur in L_poly:
        area += (-1 + cur[0][0] + cur[0][1]) * cur[1]  # площадь L-полиомино
    return area


def create_figure(figure):
    set_figure = set()
    for cell in figure:
        set_figure.add((cell[0, 0], cell[0, 1]))
    return set_figure


def inscribe_poly_check(M1, M2, R_poly, L_poly):
    """
    функция для проверки невместимости хотя бы одного в плоскость, порожденную прямоугольником
    """
    concatenated = R_poly + L_poly
    m = max(max(concatenated, key=lambda x: max(x[0]))[0])
    if m > max(M1, M2):
        return False
    else:
        return True


def main(M1, M2, R_poly, L_poly):
    """

    :param M1, M2: 1-tuple - (M1, M2) размер доски M1>M2
    :param R_poly: 2-list из тьюплов - [((размер прямоугольного полимино_1, размер прямоугольного полимино_1), мощность_1),..
    ,((размер прямоугольного полимино_N, размер прямоугольного полимино_N), мощность_N)]
    :param L_poly: 3-list из тьюплов - [((размер L-shaped полимино_1, размер L-shaped полимино_1), мощность_1),..
    ,((размер L-shaped полимино_N, размер L-shaped полимино_N), мощность_N)]
    """

    if not inscribe_poly_check(M1, M2, R_poly, L_poly):
        return False

    if area_compute(R_poly, L_poly) > M1 * M2:
        return False

    fig = preprocess(M1, M2, R_poly, L_poly)
    position, cardinal = {}, 0  # position - {номер: конфигурация}
    struct, graph_inv = {}, {}  # bipartite graph
    power_of_poly = {}
    concatenated = R_poly + L_poly
    for idx, poly in enumerate(concatenated):
        power_of_poly[idx] = poly[1]

    for figure in fig:
        for i in range(M1):
            for j in range(M2):
                if (i + figure.shape[0]) <= M1:
                    if j + figure.shape[1] <= M2:
                        cur_pos = np.zeros((M1, M2))
                        cur_pos[i:i + figure.shape[0], j:j + figure.shape[1]] = figure
                        position[cardinal] = cur_pos
                        cardinal += 1
    for i in range(M1):  # строим граф
        for j in range(M2):
            for pos in position.keys():
                if position[pos][i][j] == 1:
                    if pos not in graph_inv:
                        graph_inv[pos] = []
                    if (i, j) not in struct:
                        struct[(i, j)] = set()
                    struct[(i, j)].add(pos)  # {(i, j): set(pos)}
                    graph_inv[pos].append((i, j))
    configurations = adj_matrix(M1, M2, R_poly, L_poly)

    result = list(solution(struct, graph_inv, sum(power_of_poly.values()), configurations, power_of_poly))

    if result:
        grid = np.zeros((M1, M2))
        for i in result[0]:
            grid += position[i] * (i + 1)
        print(grid)
        return True
    else:
        return False


if __name__ == '__main__':
    '''
    1-tuple - (M1, M2) размер доски M1>M2
    2-list из тьюплов - [((размер прямоугольного полимино_1, размер прямоугольного полимино_1), мощность_1),..
    ,((размер прямоугольного полимино_N, размер прямоугольного полимино_N), мощность_N)]
    3-list из тьюплов - [((размер L-shaped полимино_1, размер L-shaped полимино_1), мощность_1),..
    ,((размер L-shaped полимино_N, размер L-shaped полимино_N), мощность_N)]
    '''

    input = [(3, 5), [((2, 2), 1)], [((2, 2), 2), ((2, 3), 1)]]
    if main(input[0][0], input[0][1], input[1], input[2]):
        print("Правда")
    else:
        print("Ложь")
