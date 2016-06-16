"""
Получение эталонных данных
Вход:
isFrom - состояние пазла до сделанного хода
isTo - состояние пазла после хода
sizeH, sizeV - размер пазла

Выход:
массив allgraphs, включающий в себя набор матриц с состояниями " из .. в " и признак того что ход был верных
- "1" или не верный "0"
"""

import numpy as np

# Получение данных
def check_values(isFrom, isTo, sizeH, sizeV):

    allgraphs = np.array([])
    if np.array_equal(isFrom, isTo):                    # Состояния равны
        train_y = 0
        graphs = np.concatenate((isFrom, isTo))
        allgraphs = np.append(allgraphs, [graphs, train_y])
    else:
        positionIsFrom = isFrom[sizeH*sizeV-1]
        positionIsTo = isTo[sizeH*sizeV-1]
        tmp = [positionIsFrom[0]-1,positionIsFrom[1]]
        if np.array_equal(tmp, positionIsTo):
            train_y = 1
        else:
            train_y = 0
        isToTmp = np.array(isTo)
        i = find_index(isToTmp, tmp)
        if i != -1:
            isToTmp[i] = isToTmp[sizeH*sizeV-1]
        isToTmp[sizeH*sizeV-1] = tmp
        graphs = np.concatenate((isFrom, isToTmp))
        allgraphs = np.append(allgraphs, [graphs, train_y])
        tmp = [positionIsFrom[0]+1, positionIsFrom[1]]
        if np.array_equal(tmp, positionIsTo):
            train_y = 1
        else:
            train_y = 0
        isToTmp = np.array(isTo)
        i = find_index(isToTmp, tmp)
        if i != -1:
            isToTmp[i] = isToTmp[sizeH*sizeV-1]
        isToTmp[sizeH*sizeV-1] = tmp
        graphs = np.concatenate((isFrom, isToTmp))
        allgraphs = np.append(allgraphs, [graphs, train_y])
        tmp = [positionIsFrom[0], positionIsFrom[1]-1]
        if np.array_equal(tmp, positionIsTo):
            train_y = 1
        else:
            train_y = 0
        isToTmp = np.array(isTo)
        i = find_index(isToTmp, tmp)
        if i != -1:
            isToTmp[i] = isToTmp[sizeH*sizeV-1]
        isToTmp[sizeH*sizeV-1] = tmp
        graphs = np.concatenate((isFrom, isToTmp))
        allgraphs = np.append(allgraphs, [graphs, train_y])
        tmp = [positionIsFrom[0], positionIsFrom[1]+1]
        if np.array_equal(tmp, positionIsTo):
           train_y = 1
        else:
            train_y = 0
        isToTmp = np.array(isTo)
        i = find_index(isToTmp, tmp)
        if i != -1:
            isToTmp[i] = isToTmp[sizeH*sizeV-1]
        isToTmp[sizeH*sizeV-1] = tmp
        graphs = np.concatenate((isFrom, isToTmp))
        allgraphs = np.append(allgraphs,[graphs,train_y])

    return allgraphs


# Поиск индекса элемента
# В случае отсутствия элемента возвращается -1
def find_index(arr, value):

    index = -1

    for i in range(len(arr)):
        if np.array_equal(arr[i],value):
            index = i
    return index


def turple_repl(new_el, pos, t):
    assert isinstance(t, tuple)
    pos = int(pos)
    return t[:pos] + (new_el,) + t[pos + 1:]