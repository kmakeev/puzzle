from turple_repl import turple_repl
"""
раскрытие/постановка в очередь смежных состояний
Вход:
sizeH, sizeV - - размер полей позла по гороизонтали и вертикали
set_ - текущий пазл
position - позиция, в которой находится пустое поле (0)
Выход:
Кортеж с возможными вариантами пазла из текущей позиции
"""


def searh_graph(position, set_, sizeH, sizeV):
    graphs = ()
    if position[0] > 0:
        tmp = [position[0]-1, position[1]]
        reply_set_ = turple_repl(tmp, sizeH*sizeV-1, set_)
        reply_set_ = turple_repl(position, set_.index(tmp), reply_set_)
        graphs = turple_repl(reply_set_[::], len(graphs), graphs)
    if position[0] < (sizeV-1):
        tmp = [position[0]+1, position[1]]
        reply_set_ = turple_repl(tmp, sizeH*sizeV-1, set_)
        reply_set_ = turple_repl(position, set_.index(tmp), reply_set_)
        graphs = turple_repl(reply_set_[::], len(graphs), graphs)
    if position[1] > 0:
        tmp = [position[0], position[1]-1]
        reply_set_ = turple_repl(tmp, sizeH*sizeV-1, set_)
        reply_set_ = turple_repl(position,set_.index(tmp), reply_set_)
        graphs = turple_repl(reply_set_[::], len(graphs), graphs)
    if position[1] < (sizeH-1):
        tmp = [position[0], position[1]+1]
        reply_set_ = turple_repl(tmp, sizeH*sizeV-1, set_)
        reply_set_ = turple_repl(position, set_.index(tmp), reply_set_)
        graphs = turple_repl(reply_set_[::], len(graphs), graphs)
    return graphs
