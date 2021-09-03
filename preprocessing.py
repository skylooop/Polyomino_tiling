import numpy as np


def rotate():
    rotate90_matrix = np.ndarray([[0, -1], [1, 0]])
    rotate180_matrix = np.ndarray([[-1, 0], [0, -1]])
    rotate270_matrix = np.ndarray([[0, 1], [-1, 0]])

def preprocess(M1, M2, R_poly, L_poly):
    """
    Для прямоугольных фигурок все просто, а для L-полиомино нужно просмотреть все возможные ориентации.
    """
    all_figures = []
    for r_poly in R_poly:
        all_figures.append(np.ones(r_poly[0]))
        if r_poly[0][0] == r_poly[0][1]:  # проверка на квадрат
            continue
        else:
            all_figures.append(np.ones(r_poly[0]).T)  # добавили еще транспонированный прямоугольник

    for l_poly in L_poly:
        # []
        # []
        # [][] Полиомино такого вида
        first = np.zeros(l_poly[0])
        first[:, :1] = np.ones((l_poly[0][0], 1))
        first[-1::] = np.ones(l_poly[0][1])
        all_figures.append(first)

        #     []
        # [][][]
        second = np.zeros(l_poly[0][::-1])
        second[:, -1:] = np.ones((l_poly[0][1], 1))
        second[-1] = np.ones(l_poly[0][0])
        all_figures.append(second)

        # [][][]
        # []
        third = np.zeros(l_poly[0][::-1])
        third[:, :1] = np.ones((l_poly[0][1], 1))
        third[0] = np.ones(l_poly[0][0])
        all_figures.append(third)

        # [][]
        #   []
        #   []
        fourth = np.zeros(l_poly[0])
        fourth[:, -1:] = np.ones((l_poly[0][0], 1))
        fourth[0] = np.ones(l_poly[0][1])
        all_figures.append(fourth)

    return all_figures


def adj_matrix(M1, M2, R_poly, L_poly):
    conf, num = {}, 0
    for i in R_poly:
        next = len(conf)
        adj_ma = {x + next: num for x in range((M1 - i[0][0] + 1) * (M2 - i[0][1] + 1))}
        conf.update(adj_ma)
        if i[0][0] == i[0][1]:
            num += 1
            continue
        else:
            next = len(conf)
            adj_ma = {x + next: num for x in range((M1 - i[0][1] + 1) * (M2 - i[0][0] + 1))}
            conf.update(adj_ma)
            num += 1
    for j in L_poly:
        next = len(conf)
        adj_ma = {x + next: num for x in range((M1 - j[0][0] + 1) * (M2 - j[0][1] + 1) * 2)}
        conf.update(adj_ma)
        next = len(conf)
        adj_ma = {x + next: num for x in range((M1 - j[0][1] + 1) * (M2 - j[0][0] + 1) * 2)}
        conf.update(adj_ma)
        num += 1
    return conf


def solution(x, y, cardinal, config, power_of_poly, result=None):
    """
    Algorithm X + Dancing Links/recursive
    Идем по графу, уменьшая при этом постепенно число доминошек
    """
    if result is None:
        result = []
    if cardinal == len(result):
        yield list(result)
    else:
        mini = 9999999999
        mini_col = None
        for i in x.keys():
            if len(x[i]) > 0:
                if mini > len(x[i]):
                    mini = len(x[i])
                    mini_col = i
            else:
                mini_col = list(x.keys())[-1]

        for vertex in list(x[mini_col]):
            power_of_poly[config[vertex]] -= 1
            result.append(vertex)
            columns = []
            for y_col in y[vertex]:
                for i_col in x[y_col]:
                    for i in y[i_col]:
                        if i != y_col:
                            x[i].remove(i_col)
                columns.append(x.pop(y_col))
            good = set()
            for i in x.values():
                good.update(i)  # union
            rows = []
            if power_of_poly[config[vertex]] == 0:
                for cell in config:
                    if config[cell] == config[vertex] and cell in good:
                        cur_row = cell  # Удалили ненужные строки
                        for i in y[cell]:
                            x[i].remove(cell)
                        rows.append(cur_row)
                        good.remove(cell)
            for s in solution(x, y, cardinal, config, power_of_poly, result):
                yield s
            power_of_poly[config[vertex]] += 1
            result.pop()
            for cell in rows:
                for i in y[cell]:
                    x[i].add(cell)

            for j in y[vertex][::-1]:
                x[j] = columns.pop()
                for i in x[j]:
                    for k in y[i]:
                        if k != j:
                            x[k].add(i)


