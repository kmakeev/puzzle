from coast import coast
from searh_graph import searh_graph
from chekInOpenSet import chekInOpenSet
from heapq import heappush, heappop


def searchSolution(start, sizeH, sizeV):
    # print('In Search Solution')
    goal = tuple([[i, j] for i in range(sizeV) for j in range(sizeH)])
    closed = []  # список обработанных состояний
    path_map = []  # очищаем карту
    g = 0  # оценка стоимости пути от начального узла до узла n
    h = coast(start, goal, sizeH, sizeV)
    f = h + g
    openset_heap = []

    heappush(openset_heap, [h, g, f, start, start])  # множество состояний, которые предстоит обработать
    while len(openset_heap) != 0:
        x = heappop(openset_heap)

        # print ('X - ', x[3], 'F- ', x[0], ' H -',x[1])

        # if (len(closed) % 1000) == 0:
            # print ('X full - ', x)
            # print('X - ', x[3], 'F- ', x[2], ' H -', x[0], ' G - ', x[1])
            # print('In open - ', len(openset_heap))
            # print('In closed - ', len(closed))
        if x[3] == goal:
            # print(' Start - ', start)
            # print(' Finish X - ', x[3], 'F- ', x[2], ' H -', x[0], ' G - ', x[1])
            current_node = x
            path_map.append(goal)
            while current_node[3] != start:
                path_map.append(current_node[3])
                current_node = current_node[4]
            return path_map

        closed.append(x[3])
        b = x[3]
        c = b[sizeH * sizeV - 1]
        tentative_g_score = x[1] + 1
        new_ = searh_graph(c, b, sizeH, sizeV)  # раскрытие/постановка в очередь смежных состояний
        if len(new_) != 0:
            for i in new_:
                # print (i)
                if i in closed:
                    # print ('Next in closed')
                    # print (i)
                    continue
                iInOpenSet = chekInOpenSet(i, openset_heap,
                                           tentative_g_score)  # Будем получать сразу два признака, наличия в списке
                                                               # открытых узлов и стоимость от начала до него
                if not iInOpenSet[0]:
                    # print ('IS better sets' , 'G - ', tentative_g_score)
                    tentative_is_better = True
                else:
                    if tentative_g_score < iInOpenSet[1]:
                        # print ('Better sets in open', tentative_g_score, iInOpenSet)
                        tentative_is_better = True
                    else:
                        # print ('tentative_g_score > iInOpenSet', tentative_g_score, iInOpenSet[1])
                        tentative_is_better = False
                if tentative_is_better:
                    g = tentative_g_score
                    h = coast(i, goal, sizeH, sizeV)
                    f = h + g
                    # x = iInOpenSet[2]
                    heappush(openset_heap, [h, g, f, i, x])
                    # print ('Add set in openset - ', [f,h,g,i,x])
                    # print ('In open - ', len(openset_heap))
                    # print ('In closed - ', len(closed))
        else:
            print('Not search :(')
            return path_map
