import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Flatten

num_classes = 10
inputs = Input((28, 28, 1))
x = Flatten()(inputs)
x = Dense(512, activation='relu')(x)
x = Dense(256, activation='relu')(x)
x = Dense(128, activation='relu')(x)
outputs = Dense(num_classes, activation='softmax', name="OutputLayer")(x)
model = Model(inputs, outputs, name="FCNN_Classifier")
model.summary()