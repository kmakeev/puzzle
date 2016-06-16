"""
Замена элемента в кортеже
Вход:
t - исходный кортеж
new_el - элемент для вставки в кортеж
pos - позиция для вставки
Выход:
Кортеж со вставленным элементом
"""


def turple_repl(new_el, pos, t):
    assert isinstance(t, tuple)
    pos = int(pos)
    return (t[:pos]+(new_el,)+t[pos+1:])   
