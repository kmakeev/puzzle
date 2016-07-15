from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, Array, Float 
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import logging

from model_v_2 import ModelII
from wsgiref.simple_server import make_server
import numpy as np


"""
Класс синглтона для модели нейронной сети
"""
class Singleton(object):

    model = ModelII()
    _instance = None
    
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


"""
Класс soap - сервиса для обработки запросов
"""
class PuzzleService(ServiceBase):

   
    @rpc(Unicode, _returns=Array(Float))
    def say_hello(ctx, name):
        my_singletone = Singleton()
        print(my_singletone.model)
        a = [.0, .2, 0.1, .0] 
        return a

    @rpc(Iterable(Float(max_occurs='unbounded')),_returns=Float)
    def train_on_batch(ctx, value):
        my_singletone = Singleton()
        x_val = np.array([])
        y_val = np.array([1])
        for i in value:
            x_val = np.append(x_val,[i])
        #print(x_val)
        x_val.shape = (-1,2*my_singletone.model.datadim)
        loss = my_singletone.model.model.train_on_batch(x_val,y_val)
        return float(loss[0])

    @rpc(Iterable(Float(max_occurs='unbounded')), _returns=Array(Float))
    def get_predict_on_batch(ctx, value):
         
        for_predict = np.array([])
        my_singletone = Singleton()
        #print(my_singletone.model)
        #print(my_singletone.model.sizeH, my_singletone.model.sizeV)
       
        for i in value:
            #print(i)
            for_predict = np.append(for_predict,[i])
            
        #print(type(for_predict))
        #print(for_predict)
        for_predict.shape = (-1,2*my_singletone.model.datadim)
        #for_predict.shape = (-1,2,2*2*2)
        #print(for_predict)
        prediction = my_singletone.model.model.predict_on_batch(for_predict)
        #print(prediction)
        #print(prediction[0][0])
        return prediction[0][0]

application = Application([PuzzleService],'http://my.example.soap',
                            in_protocol=Soap11(validator='lxml'),
                            out_protocol=Soap11())

wsgi_application = WsgiApplication(application)
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
logging.info("listening to http://127.0.0.1:8000")
logging.info("wsdl is at: http://localhost:8000/?wsdl")
server = make_server('127.0.0.1', 8000, wsgi_application)
server.serve_forever()


    
