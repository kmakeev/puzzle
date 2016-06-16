__author__ = 'Makeev K.P.'
# Игра в пазлы - Пятнашки
# Данное программа является тестовой и поставляется как есть

import kivy
import random
import time
import math
import numpy as np

import threading

from suds import WebFault
from suds.client import Client
from suds.cache import DocumentCache
import logging

from heapq import heappush, heappop
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.animation import Animation

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.properties import (ListProperty,
                             NumericProperty,
                             BooleanProperty)



from keras.preprocessing.sequence import pad_sequences

from utils.searh_values import searh_values


class GridEntry(Button):                            # класс для одной кнопки на PuzzleGrid
    num = NumericProperty(1)
    position = ListProperty([0, 0])
    

    def str_value(self, a):                         #Возврат числа как строки, и пустой строки для нуля
        if not self.num == 0:
            return str(a)
        return ''
    pass


class PuzzleLayout(FloatLayout):                    # собсвенный макет пожложки
    step = NumericProperty(0)                       # колчество сделанных шагов

    
    def __init__(self, *args, **kwargs):
        super(PuzzleLayout, self).__init__(*args, **kwargs)
        

class PuzzleGrid(GridLayout):                       #GridLayout для паззла
    puzzle = ListProperty()                         # сам пазл в виде цифр. будем генерировать
    puzzle_before_turn = ListProperty([1,1,1])      # пазл дo сделанного хода
    isWin = BooleanProperty(False)                  # признак того, что все собрали
    isTrain = BooleanProperty(True)
 
    def __init__(self, *args, **kwargs):            #конструктор
        super(PuzzleGrid, self).__init__(*args, **kwargs)
        print('In PuzzleGrid')

    def generateGrid(self, V, H):                   #генератирем PuzzleGrid
        a = 0
        self.cols = H
        print(' In Generate Puzzle', V, H)
        for row in range(V):
            for column in range(H):
                    grid_entry = GridEntry(num=self.puzzle[a], position=(row,column))
                    grid_entry.bind(on_press=self.button_pressed)
                    self.add_widget(grid_entry)
                    a += 1

    def button_pressed(self, button):  # Обработчика нажатия кнопки
        self.isTrain = self.parent.ids['isCheckBox'].active  # Таким образом можно определить объект по id в KV файле

        for i in range(len(self.children)):
            if self.children[i].num == 0:
                j = i
        index = self.children.index(button)
        grid_tmp1 = self.children[index]
        grid_tmp2 = self.children[j]
        delta_x = abs(int(grid_tmp1.position[0]) - int(grid_tmp2.position[0]))
        delta_y = abs(int(grid_tmp1.position[1]) - int(grid_tmp2.position[1]))
        if (delta_x + delta_y) == 1:
            a = grid_tmp1.num
            b = grid_tmp2.num
            position_tmp = grid_tmp1.position
            grid_tmp1.position = grid_tmp2.position
            grid_tmp2.position = position_tmp
            self.children[j] = grid_tmp1
            self.children[index] = grid_tmp2  # Замена объектов для отображения
            c = self.puzzle.index(a)
            d = self.puzzle.index(b)
            e = self.puzzle[c]
            self.puzzle[c] = self.puzzle[d]
            self.puzzle[d] = e  # Замена значений в массиве puzzle
            self.parent.step += 1  # У родителя (PuzzleLayout) увеличиваем счетчик
            self.isWin = not self.isWin  # сигналим изменение

            


    def press(self, pos):                                   #Эммитируем нажатиа на кнопку в которой указана передаваемая позиция
        
        for i in range(len(self.children)):                 #ищем объект кнопки, содержащий переданную позицию
            if self.children[i].position == pos:
                j = i
                break
             
        self.button_pressed(self.children[j])               #эммитируем нажатие найденного объекта кнопки
        
   
class PuzzleApp(App):                                       #Класс приложения

    puzzle = []
    sizeH = 4
    sizeV = 4
    datadim = 2*4*4
    start = tuple([[0,0] for i in range(sizeH*sizeV)])                       #кортеж с координатами чисел. Размер массива определяется величиной sizeH, SizeV
    puzzle_before_turn = tuple([[0,0] for i in range(sizeH*sizeV)])          #кортеж с координатами предыдущего состояния (нужен для обучения)   
    iiValues = []                                                            #Массив значений для всех возможных ходов, определнных II.
    puzzle_Layout = PuzzleLayout();
    puzzle_Grid = PuzzleGrid()
    content = Button()
    popup = Popup()
    step = 0;
    path_map = []                           #карта пройденных состояний

    start_Th = threading.Event()

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.CRITICAL)

    try:
        client = Client('http://localhost:8000/?wsdl')          #Класс клиента wsdl -схемы
        client.set_options(cache=DocumentCache())
    except:
    #except WebFault as e:
        print('Error connect to Soap service')

   
    def build(self):                                            
       
        self.puzzle_Layout = PuzzleLayout();
        self.generatePuzzle()
        self.puzzle_Grid = PuzzleGrid(puzzle=self.puzzle)
        self.puzzle_Grid.bind(isWin=self.launch_popup)
        self.puzzle_Grid.generateGrid(self.sizeV,self.sizeH)
        self.puzzle_Layout.add_widget(self.puzzle_Grid)

        self.generateStart()
                 
        return self.puzzle_Layout

    def change_scale(self, scale):                              #Изменение размера полей пазла                 
        #print('in change scale', scale);
        a = int(math.sqrt(scale))
        b = int(round(scale/a - 0.45))
        self.puzzle_Layout.remove_widget(self.puzzle_Grid)
        self.sizeV = a
        self.sizeH = b
        self.generatePuzzle()
        self.puzzle_Layout.step = 0
        self.path_map = [] 
        self.puzzle_Grid = PuzzleGrid(puzzle = self.puzzle)
        self.puzzle_Grid.bind(isWin=self.launch_popup)
        self.puzzle_Grid.generateGrid(self.sizeV,self.sizeH)
        self.puzzle_Layout.add_widget(self.puzzle_Grid)
        self.generateStart()
        
       

    def generatePuzzle(self):                                   #Генерация нового пазла
 
        isGenerate = 1
        while isGenerate:
            self.puzzle = []
            index = 0
            while len(self.puzzle)<self.sizeH*self.sizeV-1:
                x = int(random.random()*self.sizeH*self.sizeV)
                if (not x in self.puzzle)&(x!=0):
                    self.puzzle.append(x)
                    coordinates = [0,0]
                    coordinates[0] = index // self.sizeH
                    coordinates[1] = index % self.sizeH
                    y = x-1
                    self.start = self.turple_repl(coordinates, y,self.start)               
                    index +=1
            summ = 0                            #Проверка на сходимость  
            for i in self.puzzle:
                if i != 0:
                    b = 0
                    c = self.puzzle.index(i)
                    for j in self.puzzle[c:len(self.puzzle)]:
                        if j<i:
                            b += 1
                    summ = summ + b
            #summ +=self.sizeH
            #print('Summ', summ, self.sizeH)

            #summ = summ + 2                              #2 Если 3Х3 4 если 4 на 4    
            isGenerate = summ % 2
            #print('In PuzzleApp ', isGenerate)
        self.puzzle.append(0)                            #ноль всегда последний

    def launch_popup(self,instance,value):               #Dызыватеся после каждого сделанного хода по изменению свойства isWin, в т.ч. и для проверки окончания игры             
        #print('In popup')
        #print(instance)
        self.puzzle_before_turn = self.start
        self.generateStart()
        
        if self.puzzle_Grid.isTrain:
            loss = 1.0
            if len(self.iiValues)!=0:
                print(self.iiValues)
                while ((1-loss)<self.iiValues[-1]):
                    #print(self.puzzle_before_turn)
                    #print(self.start)
                    X_old_bt = np.array(self.puzzle_before_turn)
                    X_old_bt.shape = (-1, 2*self.sizeH*self.sizeV)
                    X_old = np.array(self.start)
                    X_old.shape = (-1, 2*self.sizeH*self.sizeV)
                    #print(X_old_bt)
                    #print(X_old)
                    X_old_bt = np.array(pad_sequences(X_old_bt, maxlen=self.datadim, padding='post'))
                    X_old = np.array(pad_sequences(X_old, maxlen=self.datadim, padding='post'))
                    #print(X_old_bt)
                    #print(X_old)
                    X = np.array([],dtype = np.float32)
                    X = np.append(X,X_old_bt)
                    X = np.append(X, X_old)
                    #print(X)
                    X.shape = (-1,2*self.datadim)
                    #print(X[0].tolist())
                    loss = self.client.service.train_on_batch({'float': X[0].tolist()})
                    #print('Loss - ',loss)
                    #print(self.iiValues, self.iiValues[-1])
                self.iiValues = []
            else:
               # print(self.puzzle_before_turn)
               # print(self.start)
                X_old_bt = np.array(self.puzzle_before_turn)
                X_old_bt.shape = (-1, 2*self.sizeH*self.sizeV)
                X_old = np.array(self.start)
                X_old.shape = (-1, 2*self.sizeH*self.sizeV)
                #print(X_old_bt)
                #print(X_old)
                X_old_bt = np.array(pad_sequences(X_old_bt, maxlen=self.datadim, padding='post'))
                X_old = np.array(pad_sequences(X_old, maxlen=self.datadim, padding='post'))
                #print(X_old_bt)
                #print(X_old)
                X = np.array([],dtype = np.float32)
                X = np.append(X,X_old_bt)
                X = np.append(X, X_old)
                #print(X)
                X.shape = (-1,2*self.datadim)
                #print(X[0].tolist())
                loss = self.client.service.train_on_batch({'float': X[0].tolist()})
                print('Loss - ',loss)
                
        
        self.puzzle = instance.puzzle
        #print(self.puzzle)
        if self.check_result():
            self.content = Button(text='You win!', font_size=48)
            self.popup = Popup(title='Message', content=self.content, size_hint = (0.4, 0.4), auto_dismiss=False)
            #self.content.bind(on_press=self.popup.dismiss)
            self.content.bind(on_press=self.newGame)    
            self.popup.open()
            Clock.unschedule(self.my_playII)
    
    def newGame(self,instance):                             #Начало новой игры по окончании предыдушей
        #print('in New Game');
        
        self.puzzle_Layout.remove_widget(self.puzzle_Grid)
        #self.sizeV = self.puzzle_Layout.sizeV
        #self.sizeH = self.puzzle_Layout.sizeH
        self.generatePuzzle()
        self.puzzle_Layout.step = 0
        self.path_map = [] 
        self.puzzle_Grid = PuzzleGrid(puzzle = self.puzzle)
        self.puzzle_Grid.bind(isWin=self.launch_popup)
        self.puzzle_Grid.generateGrid(self.sizeV,self.sizeH)
        self.puzzle_Layout.add_widget(self.puzzle_Grid)
        self.generateStart()
        self.popup.dismiss()
        

    def stopPlayEvr(self):                              #Останов игры после поиска решения эвристикой
        #print('In Stop')
        #print('Is Alive', self.p1.isAlive())
        #if (self.start_Th.isSet() & self.p1.isAlive():
        Clock.unschedule(self.my_play)
        self.start_Th.clear()
        #print ('Event start - ', self.start_Th.isSet())
        

    def generateStart(self):                            #Генерация начального пазла
        #print('In Generate Start')
        #self.start = ([0,0],[0,0],[0,0],[0,0],
        #            [0,0],[0,0],[0,0],[0,0],
        #           [0,0],[0,0],[0,0],[0,0],
        #    
        #            [0,0],[0,0],[0,0],[3,3])
        self.start = tuple([[0,0] for i in range(self.sizeH*self.sizeV)]) 
        
        for x in self.puzzle_Grid.puzzle:
            index = self.puzzle_Grid.puzzle.index(x)
            coordinates = [0,0]
            coordinates[0] = index // self.sizeH
            coordinates[1] = index % self.sizeH
            if (x==0):
                #self.start[self.sizeH*self.sizeV-1]=coordinates
                self.start = self.turple_repl(coordinates, self.sizeH*self.sizeV-1,self.start)
            else:
                y = x-1
                #self.start[y]=coordinates
                self.start = self.turple_repl(coordinates, y,self.start)
            #print(x)
            #print(coordinates)
        #print(self.start)

        

    
    def playOnEvr(self):                                # Старт игры эвристикой
        
        #print('Start thread')
        #print ('Event start - ', self.start_Th.isSet())
        if not self.start_Th.isSet():
           self.start_Th.set()
           self.p1 = threading.Thread(target=self.playOnEvrStart)           #Запуск поиска решения в отдельном потоке
           self.p1.start()
        #print(self.p1)
 
        


    def playOnEvrStart(self):                           #Ищем решения эвристики включаем игру 
        #print('In Thread play on app')
        #print(self.puzzle_Grid.puzzle)
        
        self.generateStart()
        goal = tuple([[i,j] for i in range(self.sizeV) for j in range(self.sizeH)])
        #print('start', self.start)
        #print('goal', goal)
       
        
        closed = []                             #список обработанных состояний
        self.path_map = []                      #очищаем карту
        
        g =  0                                  #оценка стоимости пути от начального узла до узла n
        h = self.coast(self.start, goal)
        f = h + g
        #penset.append([h,g,f,start])
        openset_heap = []
        
        heappush(openset_heap,[h,g,f,self.start,self.start])    #множество состояний, которые предстоит обработать
        #path_map.append([g,start])
        
        while len(openset_heap)!=0:
            #a = self.minSet(openset)
            x = heappop(openset_heap)
            
           
            if (len(closed) % 1000)==0: 
                #print ('X full - ',x)
                print ('X - ', x[3], 'F- ', x[2], ' H -',x[0], ' G - ' ,x[1] )
                print ('In open - ', len(openset_heap))
                print ('In closed - ', len(closed))

            #print ('Goal - ', goal)

                #self.printOpenset(openset_heap) 
            #self.printClosed(closed)
                
            #openset.remove(a)
            #hashA = hash(str(a[3]))
            #print ('Hash - ',hashA)
            if x[3]==goal:
                print(' Start - ', self.start)
                print(' Finish X - ', x[3], 'F- ', x[2], ' H -',x[0], ' G - ' ,x[1])
                current_node = x
               # print ('current_node', current_node)
                self.path_map.append(goal)
                while current_node[3] != self.start:
                    self.path_map.append(current_node[3])
                    current_node = current_node[4]
                    #print(' Current Node  ', current_node)
                
                #print ('In Step - ', len(self.path_map))
                
                self.step = len(self.path_map) - 1

                Clock.schedule_interval(self.my_play, 0.7)                 #настраиваем вызов по таймеру каждую секунду для одного шага
                break
            if ((self.p1.isAlive()) & (not self.start_Th.isSet())):         #проверка нажатия стоп при выполнении отдельного потока
                print ('Stop in Thread')
                break
                
                

            #print ('Append in closed ', x)
            
            closed.append(x[3])
            
            b = x[3]
            c = b[self.sizeH*self.sizeV-1]
            #print (' A not in closed, turn - ', g)
            #print ('X- ', x)
            tentative_g_score = x[1]+1
            new_ = []                        #список смежных состояний
            #print('New in', c,b)
            new_ = self.searh_graph(c,b)        #раскрытие/постановка в очередь смежных состоний
           # print ('New set - ', new_)
            if len(new_)!=0:
                for i in new_:
                    #print (i)
                    if i in closed:
                        #print ('Next in closed')
                        #print (i)
                        continue
                    #tentative_g_score = self.coast(start,i)             #x[2] + self.coast(a[3],i)       #
                    
                    iInOpenSet = self.chekInOpenSet(i,openset_heap, tentative_g_score)                       #Будем получать сразу два признака, наличия в списке открытых узлов и стоимость от начала до него
                    
                    if iInOpenSet[0] == False:
                        #print ('IS better sets' , 'G - ', tentative_g_score)
                        tentative_is_better = True
                    else:
                        if tentative_g_score < iInOpenSet[1]:
                            #print ('Better sets in open', tentative_g_score, iInOpenSet)
                            tentative_is_better = True
                        else:
                            #print ('tentative_g_score > iInOpenSet', tentative_g_score, iInOpenSet[1])
                            tentative_is_better = False
                    if tentative_is_better == True:
                        g = tentative_g_score
                        h=self.coast(i,goal)
                        f = h + g
                        #x = iInOpenSet[2]
                        heappush(openset_heap,[h,g,f,i,x])
                        #print ('Add set in openset - ', [f,h,g,i,x])
                                        
                    #print ('In open - ', len(openset_heap))
                    #print ('In closed - ', len(closed))
            else:
                print ('Not search :(')
                break


       
    def playOnII(self):                                         #Старт игры на основе ИНС
        Clock.schedule_interval(self.my_playII, 2)


    def stopPlayII(self):                                       #Стоп Игры на основе ИНС
        #print('In Stop II')
        Clock.unschedule(self.my_playII)

    def my_playII(self, dt):                                    #Игра с помощью сервиса искуственной нейронной сети

        #print('In my play II')
        self.generateStart()
        #print('Start', self.start)
        values = searh_values(self.start, self.sizeH, self.sizeV)
        #print('Values - ', values)
        values.shape = (-1,2,2*self.sizeH*self.sizeV)
        pos = [0,0]
        maxIIValue = 0
        self.iiValues = []   
        for X in values:
            X.shape = (-1,2*self.sizeH*self.sizeV)
            #print('X old - ', X_old)
            X = np.array(pad_sequences(X, maxlen=self.datadim , padding='post'))
            #print('X - ', X)
            X.shape = (-1,2*self.datadim)
            #print('X - ', X)
            #print('X to list -',X[0].tolist())
            #param = {'float': X[0][0].tolist()}
            #print(param)
            prediction = self.client.service.get_predict_on_batch({'float': X[0].tolist()})
            X.shape = (-1,self.datadim, 2)
            #print('X - ', X)
            #print('Pos - ', X[0][self.datadim/2+self.sizeH*self.sizeV-1])
            #print('Prediction II', prediction[0][0])
            self.iiValues.append(prediction[0][0])
            if (prediction[0][0]>maxIIValue):
                maxIIValue = prediction[0][0]
                pos = X[0][self.datadim/2+self.sizeH*self.sizeV-1]
        self.iiValues.sort()
        print('Values - ', self.iiValues)
        print('MaxIIValue - ', maxIIValue)
        print('Pos in MaxIIValue - ', pos)
        self.puzzle_Grid.press(pos.tolist())

        #Clock.unschedule(self.my_playII)

                
    def my_play(self, dt):                                  #Игра с помощью найденного эвристического решения          
        
        if self.step!=0:
            #print(self.path_map[self.step])
            pos = self.path_map[self.step][self.sizeH*self.sizeV-1]
            print('Go to -', pos)
            self.puzzle_Grid.press(pos)              #передаем куда пошла пустая 16-клетка
            self.step = self.step - 1
        else:
            self.start_Th.clear()
            Clock.unschedule(self.my_play)
            print(self.start_Th.isSet())
            
            
    def prediction_value(self,val):                 #функция, которая возвращает 1, если входной параметр float32 >0,5 и 0 а противоположном случае
        #print('Val - ', val)    
        if (val>0.5):
            ret = 1
        if (val<=0.5):
            ret  = 0
        return ret
         

    def chekInOpenSet(self, sets, openset,g):           #Полученик признака наличия узла (состояния пазла) в списке открытых узлов и стоимость от начала до него
        iInOpenset = [False,[]]
        for i in openset:
            if i[3]==sets:
                iInOpenset = [True,i[1]]
                break
       
        return iInOpenset
            
    def printOpenset(self, open_):                      #Печать перечня списка открытых узло
        for i in open_:
            print(i)
            
    def printClosed(self, closed_):                     #Печать перечны узлов, находящихся в списке закрытых
        for i in closed_:
            print(i)
  

        
    """
    раскрытие/постановка в очередь смежных состояний

    Вход:
    sizeH, sizeV - - размер полей позла по гороизонтали и вертикали
    set_ - текущий пазл
    position - позиция, в которой находится пустое поле (0)

    Выход:
    Кортеж с возможными вариантами пазла из текущей позиции
    """
    def searh_graph(self,position, set_):       
        graphs = ()
        if position[0]>0:        
            tmp = [position[0]-1,position[1]]
            reply_set_=self.turple_repl(tmp,self.sizeH*self.sizeV-1,set_)
            reply_set_=self.turple_repl(position,set_.index(tmp),reply_set_)
            graphs = self.turple_repl(reply_set_[::],len(graphs),graphs)
           
        if (position[0]<(self.sizeV-1)):                     
            tmp = [position[0]+1,position[1]]
            reply_set_=self.turple_repl(tmp,self.sizeH*self.sizeV-1,set_)
            reply_set_=self.turple_repl(position,set_.index(tmp),reply_set_)
            graphs = self.turple_repl(reply_set_[::],len(graphs),graphs)

        if position[1]>0:          
            tmp = [position[0],position[1]-1]
            reply_set_=self.turple_repl(tmp,self.sizeH*self.sizeV-1,set_)
            reply_set_=self.turple_repl(position,set_.index(tmp),reply_set_)
            graphs = self.turple_repl(reply_set_[::],len(graphs),graphs)
           
        if (position[1]<(self.sizeH-1)):                     
            tmp = [position[0],position[1]+1]
            reply_set_=self.turple_repl(tmp,self.sizeH*self.sizeV-1,set_)
            reply_set_=self.turple_repl(position,set_.index(tmp),reply_set_)
            graphs = self.turple_repl(reply_set_[::],len(graphs),graphs)
  
        return graphs
        
    """
    Вставка элемента в кортеж
    Вход:
    t - исходный кортеж
    new_el - элемент для вставки в кортеж
    pos - позиция для вставки
    Выход:
    Кортеж со вставленным элементом
    """
    def turple_repl(self,new_el, pos,t):
        pos = int(pos)
        return (t[:pos]+(new_el,)+t[pos+1:])

    """
    Расчет стоимости (дистанции/количества шагов) пути от позиции node до node_result

    Вход:
    sizeH, sizeV - sizeH, sizeV - размер полей по гороизонтали и вертикали
    node стартовая позиция
    node_result - конечная позиция

    Выход:
    distance - расчитанная дистанция

    """    

    def coast (self, node, node_result):
       
        

        if len(node)==len(node_result):
            distance = 0
                        
            for i in range(len(node)):              # i -размерность проверяемой ноды, попробуем не учитывать цену маршрута для последней ячейки (пустой)
                distance = distance + abs(node[i][0]-node_result[i][0]) + abs(node[i][1]-node_result[i][1])

            if ((distance!=0)&(self.sizeV>2)):
                for i in range(self.sizeV):
                    a = self.sizeH*i                                # с какой позиции начинанется линия
                    if(i!=self.sizeV-1):                              # Не для последней строчки
                        distance = distance + self.checkLinearConflict(i, node[int(a):int(a+self.sizeH)])
                    else:
                        distance = distance + self.checkLinearConflict(i, node[int(a):int(a+self.sizeH-2)])     # В последней строчке, не учитываем последнее значение

                for i in range(self.sizeH):
                    column = []                         #Можно было бы сделать проще, с помощью срезов
                    if(i!=self.sizeH-1):
                        for j in range(self.sizeV):
                             column.append(node[i+j*self.sizeH])
                    elif(self.sizeV>3):
                        for j in range(self.sizeV-1):
                            column.append(node[i+j*self.sizeH])
                    distance = distance + self.checkColumnConflict(i, column)
                if (node[(self.sizeH-1)*self.sizeV-1]!=[self.sizeV-2, self.sizeH-1])|(node[(self.sizeH)*self.sizeV-2]!=[self.sizeH-1, self.sizeV-1]):
                    distance = distance + 2
                #Закомментирован код для проверки угловых конфликтов в пазле sizeH, sizeV = 4,4, можно вернуть передалав на универсальный
#                if (node[1]==[0, 1])&(node[4]==[1, 0])&(node[0]!=[0, 0]):
                    #print ('Destrust Angle conflict')
                    #print ('Node -' , node )
                    #print ('Node 2-3 - ', node[1:3])
                    #print ('Node 4-5- ', node[4:6])
#                    isConflict = 0
#                    isConflict = isConflict + int(self.checkLinearConflict(0, node[1:3]))
#                    isConflict = isConflict + int(self.checkLinearConflict(1, node[7:9]))
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

    def coast2 (self, node, node_result):                       #Для проверки стоимость от начального состояния (без учета конфликтов)
        if len(node)==len(node_result):
            distance = 0
                        
            for i in range(len(node)-1):              # i -размерность проверяемой ноды, попробуем не учитывать цену маршрута для последней ячейки (пустой)
                distance = distance + abs(node[i][0]-node_result[i][0]) + abs(node[i][1]-node_result[i][1])
                      
        return int(distance)
                           
    def checkLinearConflict(self, index, line):
#
#Проверка линейного конфликта
#Вход:
#line - строка с координатами для проверки
#index - индекс данной линии в пазле
#
#Выход:
#isConflict - наличие конфликта Да/Нет

        isConflict = 0
        for i in range(len(line)-1):
            a = line[i]
            b = line[i+1]
            #print ('A - ',a,'B - ',b )
            if (a[0]==index):                               #контролируем только свою линию
                if ((a[0]==b[0])&(a[1]-b[1]==1)):
                    #print ('LinearConflict', index)
                    #print ('In checkLinearConflict - ', line)
                    isConflict = 2
                    break
        return isConflict

    def checkColumnConflict(self, index, line):
#Проверка линейного конфликта в столбце
#Вход:
#line - строка с координатами для проверки
#index - индекс данного столбца в пазле
#Выход:
#isConflict - наличие конфликта Да/Нет
        
        isConflict = 0
        for i in range(len(line)-1):
            a = line[i]
            b = line[i+1]
            #print ('A - ',a,'B - ',b )
            if (a[1]==index):                               #контролируем только свой столбец
                if ((a[1]==b[1])&(a[0]-b[0]==1)):
                    print ('ColumnConflict', index)
                    print ('In ChekColumnConflict - ', line)
                    isConflict = 2
                    break
        return isConflict
       


    def check_result(self):
#Проверка текущего состояния на выигрошное
        result = True
        for i in range(1,len(self.puzzle),1):
            if self.puzzle[i-1]!=i:
                result = False
                break     
        if result: print(' In chek win, puzzle - ',self.puzzle)
  
        return result
    
if __name__ == '__main__':
    PuzzleApp().run()
    
