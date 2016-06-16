"""
Расчет стоимости (дистанции/количества шагов) пути от позиции node до node_result
Вход:
sizeH, sizeV - sizeH, sizeV - размер полей по гороизонтали и вертикали
node стартовая позиция
node_result - конечная позиция
Выход:
distance - расчитанная дистанция
"""


def coast(node, node_result, sizeH, sizeV):
    assert len(node) == len(node_result)
    distance = 0
    for i in range(len(node)):                         # Расчет манхетонновского расстояния в нодах
        distance = distance + abs(node[i][0]-node_result[i][0]) + abs(node[i][1]-node_result[i][1])
    if (distance != 0) and (sizeV > 2) and (sizeH > 2):
        for i in range(sizeV):                         # Добавление в случаях наличия линейных конфликтов
            a = sizeH*i
            if i != sizeV-1:                           # Не для последней строчки
                distance += checkLinearConflict(i, node[int(a):int(a+sizeH)])
            else:
                # В последней строчке, не учитываем последнее значение
                distance += checkLinearConflict(i, node[int(a):int(a+sizeH-2)])
        for i in range(sizeH):                          # Добавление в случаях наличия конфликтов в столбцах
            column = []
            if i != sizeH-1:
                for j in range(sizeV):
                    column.append(node[i+j*sizeH])
            elif sizeV > 3:
                for j in range(sizeV-1):
                    column.append(node[i+j*sizeH])
            distance += checkColumnConflict(i, column)
        # print(node[(sizeH-1)*sizeV-1], [sizeV-2, sizeH-1], node[sizeH*sizeV-2], [sizeH-1, sizeV-1])
        # Добавление в случае конфликта последнего хода
        if (node[(sizeH-1)*sizeV-1] != [sizeV-2, sizeH-1]) or (node[sizeH*sizeV-2] != [sizeH-1, sizeV-1]):
            distance += 2
# Проверка угловых конфликтов
    if node[1] == [0, 1] and node[sizeH] == [1, 0] and node[0] != [0, 0]:
        # Проверка на конфликт в левом верхнем угле
        # print('Destrust Angle conflict left/top')
        # print(node[1], node[sizeH], node[0])
        # l = [node[sizeV], node[2 * sizeV]]
        # print(node[1:3], l)
        if checkLinearConflict(0, node[1:3]) != 2:
            if checkColumnConflict(0, [node[sizeV], node[2 * sizeV]]) != 2:
                distance += 2
        # isConflict = isConflict + int(self.checkLinearConflict(1, node[7:9]))
                    #print ('Is Conflict - ', isConflict)
                    #print ('Node - 4,8', [node[4],node[8]])
                    #print ('Node - 2,5', [node[1],node[5]])
#                    isConflict = isConflict + int(self.checkColumnConflict(0, [node[4],node[8]]))
#                    isConflict = isConflict + int(self.checkColumnConflict(1, [node[1],node[5]]))
#                    if (isConflict==0):
                        #print ('Angle conflict', node)
#                        distance = distance + 2
                        #print (distance)
#                if (node[2]==[0, 2])&(node[7]==[1, 3])&(node[3]!=[0, 3]):
                    #print ('Destrust Angle conflict')
                    #print ('Node -' , node )
                    #print ('Node 2-3 two - ', node[1:3])
                    #print ('Node 6-7- ', node[6:8])
#                    isConflict = 0
#                    isConflict = isConflict + int(self.checkLinearConflict(0, node[1:3]))
#                    isConflict = isConflict + int(self.checkLinearConflict(1, node[6:8]))
                    #print ('Is Conflict - ', isConflict)
                    #print ('Node - 3,7', [node[2],node[6]])
                    #print ('Node - 8,12', [node[7],node[11]])
#                    isConflict = isConflict + int(self.checkColumnConflict(2, [node[2],node[6]]))
#                    isConflict = isConflict + int(self.checkColumnConflict(3, [node[7],node[11]]))
#                    if (isConflict==0):
                        #print ('Angle conflict', node)
#                        distance = distance + 2
                        #print (distance)
#                if (node[8]==[3, 0])&(node[13]==[3, 1])&(node[12]!=[3, 0]):
                    #print ('Destrust Angle conflict')
                    #print ('Node -' , node )
                    #print ('Node 9-10 - ', node[8:9])
                    #print ('Node 14-15- ', node[13:15])
#                    isConflict = 0
#                    isConflict = isConflict + int(self.checkLinearConflict(2, node[8:9]))
#                    isConflict = isConflict + int(self.checkLinearConflict(3, node[13:15]))
                    #print ('Is Conflict - ', isConflict)
                    #print ('Node - 4,8', [node[4],node[8]])
                    #print ('Node - 10,14', [node[9],node[13]])
#                    isConflict = isConflict + int(self.checkColumnConflict(0, [node[4],node[8]]))
#                    isConflict = isConflict + int(self.checkColumnConflict(1, [node[9],node[13]]))
#                    if (isConflict==0):
                        #print ('Angle conflict', node)
#                        distance = distance + 2
                        #print (distance)


            #print ('checkLinearConflict', distance)

    return int(distance)


def coast2(node, node_result):
    # Для проверки стоимость от начального состояния (без учета конфликтов)
    # Аналогично функции coast, но без учета конфликтов
    if len(node) == len(node_result):
        distance = 0
        for i in range(len(node)-1):
            # i -размерность проверяемой ноды, попробуем не учитывать цену маршрута для последней ячейки (пустой)
            distance = distance + abs(node[i][0]-node_result[i][0]) + abs(node[i][1]-node_result[i][1])
    return int(distance)


def checkLinearConflict(index, line):
    # Проверка линейного конфликта
    # Вход:
    # line - строка с координатами для проверки
    # index - индекс данной линии в пазле
    # Выход:
    # isConflict - наличие конфликта Да/Нет
    isConflict = 0
    for i in range(len(line)-1):
        a = line[i]
        b = line[i+1]
        if a[0] == index:                               # контролируем только свою линию
            if (a[0] == b[0]) and (a[1]-b[1] == 1):
                isConflict = 2
                break
    return isConflict

def checkColumnConflict(index, line):
    # Проверка линейного конфликта в столбце
    # Вход:
    # line - строка с координатами для проверки
    # index - индекс данного столбца в пазле
    # Выход:
    # isConflict - наличие конфликта Да/Нет
    isConflict = 0
    for i in range(len(line)-1):
        a = line[i]
        b = line[i+1]
        if a[1] == index:                               # контролируем только свой столбец
            if (a[1] == b[1]) and (a[0]-b[0] == 1):
                isConflict = 2
                break
    return isConflict

