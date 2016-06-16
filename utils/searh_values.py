from turple_repl import turple_repl
import numpy as np

"""
Поиск индекса элемента в массиве
Вход:
arr - Массив с данными
value - элемент для поиска
Выход:
Индекс элемента, присутсвующего в массиве.  -1, если он не найден

"""

def find_index(arr, value):
    print ('In find_index')
    index = -1;
    print(arr, value)
    for i in range(len(arr)):
        #print(arr[i])
        if np.array_equal(arr[i],value):
            index = i
    return index
                   
"""
Поиск возможных ходов из текущего состояния пазла
В данной функции не учитываются ошибочный варианты ходов (т.е. в ответ попадают варианты с выходом за границы (-1 в индексе позиции))
Вход:
isFrom - текущее состояние пазла
sizeH, sizeV - - размер полей позла по гороизонтали и вертикали
Выход:
allgraphs - Масив с перечнем возможных выриантов перехода

"""
def searh_values(isFrom, sizeH, sizeV):

    graphs = np.array([])
    allgraphs = np.array([])
    
    if(len(isFrom)!=0):
        positionIsFrom = isFrom[sizeH*sizeV-1]
        tmp = [positionIsFrom[0]-1,positionIsFrom[1]]
        isToTmp = np.array(isFrom)

        i = find_index(isToTmp,tmp)
        if (i >=0):
            isToTmp[i] = isToTmp[sizeH*sizeV-1]
        isToTmp[sizeH*sizeV-1] = tmp
        graphs = np.concatenate((isFrom, isToTmp))
        allgraphs = np.append(allgraphs,[graphs])
      
        tmp = [positionIsFrom[0]+1,positionIsFrom[1]]
        isToTmp = np.array(isFrom)

        i = find_index(isToTmp,tmp)
        if (i >=0):
            isToTmp[i] = isToTmp[sizeH*sizeV-1]
        isToTmp[sizeH*sizeV-1] = tmp
        graphs = np.concatenate((isFrom, isToTmp))
        allgraphs = np.append(allgraphs,[graphs])

        tmp = [positionIsFrom[0],positionIsFrom[1]-1]
        isToTmp = np.array(isFrom)
        
        i = find_index(isToTmp,tmp)
        if (i >=0):
            isToTmp[i] = isToTmp[sizeH*sizeV-1]
        isToTmp[sizeH*sizeV-1] = tmp
        graphs = np.concatenate((isFrom, isToTmp))
        allgraphs = np.append(allgraphs,[graphs])
        
        tmp = [positionIsFrom[0],positionIsFrom[1]+1]
        isToTmp = np.array(isFrom)
        
        i = find_index(isToTmp,tmp)
        if (i >=0):
            isToTmp[i] = isToTmp[sizeH*sizeV-1]
        isToTmp[sizeH*sizeV-1] = tmp
        graphs = np.concatenate((isFrom, isToTmp))
        allgraphs = np.append(allgraphs,[graphs])

       
    return allgraphs
