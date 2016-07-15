from keras.models import Sequential, model_from_json
from keras.layers import LSTM, Dense, Dropout, Embedding, Activation
from keras.preprocessing.sequence import pad_sequences
import keras.utils.io_utils as HDF5Matrix
import numpy as np
import json

sizeH = 4                       # определяем максимально возможный размер данных, с
sizeV = 4                       #  которыми будет оперировать модель сети
datadim = 2*4*4

# пути для чтения данных для тренировки модели/тестирования модели
# последовательно присваиваются для всех размерностей сформированных данных

file_nameY = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\4x4\\ForTrainAndTest\\Y_train'
file_nameX = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\4x4\\ForTrainAndTest\\X_train'

x_train_all = np.array([])
x_val_all = np.array([])
y_train_all = np.array([])
y_val_all = np.array([])
y_train = np.array([])
y_val = np.array([])
x_train_old = HDF5Matrix.load_array(file_nameX)                     # массив входных данных
y_train = HDF5Matrix.load_array(file_nameY)                         # массив эталлонных значений для входных данных
x_train_old.shape = (-1, 2*4*4)                                     # Загружаем данные для размерности 4 на 4
# Дополним нулями позицию справа до максимально возможной
x_train = np.array(pad_sequences(x_train_old, maxlen=datadim, padding='post'))
x_train.shape = (-1, 2*datadim)                                       # Одна запись - два списка позиций (из - в )
y_train.shape = (-1, 1)
print('Y_TRAIN LENGTH- ', len(y_train))
print('X_TRAIN LENGTH- ', len(x_train))
x_train_all = np.append(x_train_all, x_train)                       # Получившиемя данные добавляем в общий массив
y_train_all = np.append(y_train_all, y_train)

# Теперь обрабатываем дынные для тестирования модели

file_nameY = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\4x4\\ForTrainAndTest\\Y_test'
file_nameX = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\4x4\\ForTrainAndTest\\X_test'

x_val_old = HDF5Matrix.load_array(file_nameX)
y_val = HDF5Matrix.load_array(file_nameY)
x_val_old.shape = (-1, 2*4*4)
x_val = np.array(pad_sequences(x_val_old, maxlen=datadim, padding='post'))
x_val.shape = (-1, 2*datadim)
y_val.shape = (-1, 1)
print('Y_TEST LENGTH- ', len(y_val))
print('X_TEST LENGTH- ', len(x_val))
x_val_all = np.append(x_val_all, x_val)
y_val_all = np.append(y_val_all, y_val)

# Аналогично для размерности 3х3
sizeH = 3                       
sizeV = 3

file_nameY = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\3x3\\ForTrainAndTest\\Y_train'
file_nameX = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\3x3\\ForTrainAndTest\\X_train'

x_train_old = HDF5Matrix.load_array(file_nameX)
y_train = HDF5Matrix.load_array(file_nameY)
x_train_old.shape = (-1, 2*3*3)
x_train = np.array(pad_sequences(x_train_old, maxlen=datadim, padding='post'))
x_train.shape = (-1, 2*datadim)
y_train.shape = (-1, 1)
print('Y_TRAIN LENGTH- ', len(y_train))
print('X_TRAIN LENGTH- ', len(x_train))
x_train_all = np.append(x_train_all,x_train)
y_train_all = np.append(y_train_all,y_train)


file_nameY = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\3x3\\ForTrainAndTest\\Y_test'
file_nameX = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\3x3\\ForTrainAndTest\\X_test'

x_val_old = HDF5Matrix.load_array(file_nameX)
y_val = HDF5Matrix.load_array(file_nameY)
x_val_old.shape = (-1, 2*3*3)
x_val = np.array(pad_sequences(x_val_old, maxlen=datadim, padding='post'))
x_val.shape = (-1, 2*datadim)
y_val.shape = (-1, 1)
print('Y_TEST LENGTH- ', len(y_val))
print('X_TEST LENGTH- ', len(x_val))
x_val_all = np.append(x_val_all,x_val)
y_val_all = np.append(y_val_all,y_val)

# Аналогично для размерности 2х2
sizeH = 2
sizeV = 2
file_nameY = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\2x2\\ForTrainAndTest\\Y_train'
file_nameX = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\2x2\\ForTrainAndTest\\X_train'
x_train_old = HDF5Matrix.load_array(file_nameX)
y_train = HDF5Matrix.load_array(file_nameY)
x_train_old.shape = (-1, 2*2*2)
x_train = np.array(pad_sequences(x_train_old, maxlen=datadim, padding='post'))
x_train.shape = (-1, 2*datadim)
y_train.shape = (-1, 1)
print('Y_TRAIN LENGTH- ', len(y_train))
print('X_TRAIN LENGTH- ', len(x_train))
x_train_all = np.append(x_train_all, x_train)
y_train_all = np.append(y_train_all, y_train)

file_nameY = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\2x2\\ForTrainAndTest\\Y_test'
file_nameX = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\2x2\\ForTrainAndTest\\X_test'
x_val_old = HDF5Matrix.load_array(file_nameX)
y_val = HDF5Matrix.load_array(file_nameY)
x_val_old.shape = (-1, 2*2*2)
x_val = np.array(pad_sequences(x_val_old, maxlen=datadim, padding='post'))
x_val.shape = (-1, 2*datadim)
y_val.shape = (-1, 1)
print('Y_TEST LENGTH- ', len(y_val))
print('X_TEST LENGTH- ', len(x_val))

x_val_all = np.append(x_val_all, x_val)
y_val_all = np.append(y_val_all, y_val)

x_train_all.shape = (-1, 2*datadim)
y_train_all.shape = (-1, 1)

print('Y_TRAIN LENGTH- ', len(y_train_all))
print('X_TRAIN LENGTH- ', len(x_train_all))

x_val_all.shape = (-1, 2*datadim)
y_val_all.shape = (-1, 1)

print('Y_TEST LENGTH- ', len(y_val_all))
print('X_TEST LENGTH- ', len(x_val_all))

# Формируем модель сети
model = Sequential()
model.add(Embedding(2*datadim, 256, input_length=None))
model.add(LSTM(output_dim=128, activation='tanh', inner_activation='sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop')
model.summary()
model.fit(x_train_all, y_train_all, batch_size=128, nb_epoch=10)

file_name_weights = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\weights'
file_name_model = 'C:\\Python34\\Puzzle15\\utils\\Solutions\\model'
model.save_weights(file_name_weights, overwrite=True)
json_string = model.to_json()
with open(file_name_model, 'w') as outfile:
    json.dump(json_string, outfile)
outfile.close()

# Печать на экран предсказаний только что созданной модели сети
for i in range(20):
    X = x_val_all[i]
    X.shape = (-1, 2*datadim)
    print('X - ', X)
    prediction = model.predict_on_batch(X)
    print('Prediction', prediction)
    print('Y val - ', y_val_all[i])
                            

