from keras.models import Sequential, model_from_json
import numpy as np
import json
from pprint import pprint

"""
Класс модели для нейронной сети:
Описание сети загружается из файла file_name_weights
Сохраненные веса загружаются из файла file_name_model
"""

class ModelII:
    file_name_weights = 'C:\\Python34\\puzzle15\\utils\\Solutions\\weights'
    file_name_model = 'C:\\Python34\\puzzle15\\utils\\Solutions\\model'

    sizeH = 4
    sizeV = 4
    datadim = 2*sizeH*sizeV                #определяем максимально возможный размер данных
    model = Sequential()

    
    def __init__(self):

        y_train = np.array([])
        y_val = np.array([])

        pprint('In build')
        pprint('Read model from json')

        with open(self.file_name_model) as json_data:
            data = json.load(json_data)
        json_data.close()
        pprint(data)
        self.model = model_from_json(data)
        self.model.summary()
        self.model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop')
        self.model.load_weights(self.file_name_weights)

        
        
