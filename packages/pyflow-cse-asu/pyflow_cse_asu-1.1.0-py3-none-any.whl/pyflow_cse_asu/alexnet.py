from Model import *
from dataset import Mnist
#alexnet
#Instantiate an empty model
model_test=model()
# C1 Convolutional Layer
model_test.add(Conv(filters=96,n_prev=1,kernel_size=11, strides=4, padding="valid",activation="relu"))
# S2 Pooling Layer
model_test.add(Pool(pool_size=3,n_prev=96, strides=2, padding="valid", mode = "max"))
# C3 Convolutional Layer
model_test.add(Conv(filters=256,n_prev=96,kernel_size=5, strides=1, padding="same",activation="relu"))
# S4 Pooling Layer
model_test.add(Pool(pool_size=3,n_prev=256, strides=2, padding="valid", mode = "max"))
# C5 Convolutional Layer
model_test.add(Conv(filters=384,n_prev=256,kernel_size=3, strides=1, padding="same",activation="relu"))
# C6 Convolutional Layer
model_test.add(Conv(filters=384,n_prev=384,kernel_size=3, strides=1, padding="same",activation="relu"))
# C7 Convolutional Layer
model_test.add(Conv(filters=256,n_prev=384,kernel_size=3, strides=1, padding="same",activation="relu"))
# S8 Pooling Layer
model_test.add(Pool(pool_size=3,n_prev=256, strides=2, padding="valid", mode = "max"))
#Flatten the CNN output so that we can connect it with fully connected layers
model_test.add("flatten")
# FC8 Fully Connected Layer
model_test.add(Dense(9216,4096, activation="relu"))
# FC9 Fully Connected Layer
model_test.add(Dense(4096,1000, activation="relu"))

#Output Layer with softmax activation
model_test.add(Dense(1000,10, activation="softmax"))

mnist = Mnist('/', split_ratio=0)
train_images, train_labels, _, _, _, _ = mnist.load()
#Compile the model
model_test.fit(train_images, train_labels, epochs=3, validation_split=0.1, batchsize=1, plot=1, metrics="all")
#show model summary
model_test.summary()