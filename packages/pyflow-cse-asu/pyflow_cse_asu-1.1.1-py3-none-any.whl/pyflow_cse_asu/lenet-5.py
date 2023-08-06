#lenet5
model_test=model()


#define data object
mnist = Mnist('/', split_ratio= 0)
train_images, train_labels, _, _, test_images, test_labels = mnist.load()
#normalization
train_images = train_images / 255.0
test_images = test_images / 255.0
#reshape dataset 4D train/test features , 1D train/test labels 
train_images = train_images.reshape((60000,28,28,1))
train_labels=train_labels.reshape((60000))
test_images = test_images.reshape((10000,28,28,1))
test_labels=test_labels.reshape((10000))
#show sample of the dataset
mnist.showSample(from_set= "training", startFrom= 0)

#Instantiate an empty model
model_test=model()
# C1 Convolutional Layer
model_test.add(Conv(filters=6,n_prev=1,kernel_size=5, strides=1, padding="same",activation="tanh"))
# S2 Pooling Layer
model_test.add(Pool(pool_size=2,n_prev=6, strides=2, padding="valid", mode = "max"))
# C3 Convolutional Layer
model_test.add(Conv(filters=16,n_prev=6,kernel_size=5, strides=1, padding="valid",activation="tanh"))
# S4 Pooling Layer
model_test.add(Pool(pool_size=2,n_prev=16, strides=2, padding="valid", mode = "max"))
# C5 Convolutional Layer
model_test.add(Conv(filters=120,n_prev=16,kernel_size=5, strides=1, padding="valid",activation="tanh"))
#Flatten the CNN output so that we can connect it with fully connected layers
model_test.add("flatten")
# FC6 Fully Connected Layer
model_test.add(Dense(120,84, activation="tanh"))
#Output Layer with softmax activation
model_test.add(Dense(84,10, activation="softmax"))

#Compile the model
model_test.fit(train_images , train_labels,epochs=3,validation_split=0.1,batchsize=1,plot=1,metrics="all")
#show model summary
model_test.summary()

#test the trained model using the testing dataset
model_test.evaluate(test_images , test_labels,metrics="accuracy")