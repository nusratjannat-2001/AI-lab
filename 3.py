from tensorflow.keras.applications import MobileNet
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Model

# Load MobileNet as a backbone (excluding the top fully connected layers)
mobile_net = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
inputs = mobile_net.inputs
x = mobile_net.output
x = Flatten()(x)
x = Dense(256, activation = 'relu')(x)
outputs = Dense(10, activation = 'softmax')(x)
model = Model(inputs, outputs, name = 'NewClassifier')
model.summary(show_trainable = True)