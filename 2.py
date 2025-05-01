import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, Flatten, Dense
num_classes = 10

inputs = Input((28, 28, 1))
x = Conv2D(32, kernel_size=(3, 3), padding = 'same', activation='relu')(inputs)  # 32 filters
x = Conv2D(64, kernel_size=(3, 3), padding = 'same', activation='relu')(x)  # 64 filters
x = Conv2D(128, kernel_size=(3, 3), padding = 'same', activation='relu')(x)  # 128 filters
x = Flatten()(x)

outputs = Dense(num_classes, activation='softmax', name='OutputLayer')(x)
model = Model(inputs, outputs, name='CNN_Classifier')
model.summary()