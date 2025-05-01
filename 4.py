from tensorflow.keras.applications import MobileNet
from tensorflow.keras.datasets import cifar10
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Input, Dense, Activation, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.models import Model

#load
(trainX, trainY), (testX, testY) = cifar10.load_data()
trainY = to_categorical(trainY, num_classes = 10)
testY = to_categorical(testY, num_classes = 10)

# Load MobileNet as a backbone (excluding the top fully connected layers)
mobile_net = MobileNet(weights='imagenet', include_top=False, input_shape=(32, 32, 3))
inputs = mobile_net.inputs
x = mobile_net.output
x = Flatten()(x)
x = Dense(256, activation = 'relu')(x)
x = Dense(8, activation = 'relu')(x)
outputs = Dense(10, activation = 'softmax')(x)
model = Model(inputs, outputs, name = 'NewClassifier')
model.summary(show_trainable = True)

for layer in model.layers[:-4]:
  layer.trainable = False
model.summary(show_trainable = True)

model.compile(loss = 'categorical_crossentropy', metrics = ['accuracy'])
model.fit(trainX, trainY, batch_size=32, validation_split = 0.1, epochs = 10)

model.evaluate(testX, testY)

#Unfreeze
for layer in model.layers[-10:-5]:
  layer.trainable = True
model.summary(show_trainable = True)
model.fit(trainX, trainY, batch_size=32, validation_split = 0.1, epochs = 10)

#Unfreeze more
for layer in model.layers[-13:-10]:
  layer.trainable = True
model.summary(show_trainable = True)
model.fit(trainX, trainY, batch_size=32, validation_split = 0.1, epochs = 10)

#Unfreeze entire model
for layer in model.layers:
  layer.trainable = True
model.summary(show_trainable = True)
model.fit(trainX, trainY, batch_size=32, validation_split = 0.1, epochs = 10)

model.evaluate(testX, testY)
