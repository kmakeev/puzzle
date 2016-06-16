"""
Полученик признака наличия узла (состояния пазла) в списке открытых узлов и стоимость от начала до него
Вход:
openset - список всех открытых узлов 
sets - текущий пазл
g - значение оценки стоимости
Выход:
iInOpenset - признак присутствия узла в списке открытых, значение стоимости
"""


def chekInOpenSet(sets, openset, g):
    iInOpenset = [False, []]
    assert isinstance(openset, list)
    for i in openset:
        if i[3] == sets:
            iInOpenset = [True, i[1]]  # Оцениваем по g - количеству ходов
            break
    # print ('iInOpenset ', iInOpenset)
    return iInOpenset
