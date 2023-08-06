import numpy as np
import gzip
from PIL import Image
import cv2
import os
import requests
import matplotlib.pyplot as plt
'''
First: Some Utilities
The following three functions are used to dowload the dataset if it is not available in the path specified when instantiating an object of the dataset class.
We uploaded the dataset files to google drive to be easily accessed from remote computers.
These fuctions were taken from a stackoverflow answer.
Generally, one call of download_file_from_google_drive downloads one file.
The following three functions is not part of the framework so they will not be documented.  
'''
def download_file_from_google_drive(id, destination, status):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id': id }, stream = True)
    token = get_confirm_token(response)

    print(f'Downloading {status}...')
    if token:
        params = { 'id': id, 'confirm': token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)    
    print("Finished Successfully.")

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

class Dataset():
    '''
    Abstract class represents a dataset. Generally, any dataset inherits from this class have to have path to the root file which contains all its files.
    Methods:
        __getItem__() simply returns an item of the dataset. An item is the combination of an image and its corresponding label. The item maybe training, validation or test item.
        length() gets the length of a certain (training, validation or test) subset of the dataset.
        load() returns the training, validation and test sets splitted in arrays. 
    '''
    def __init__(self, rootFilePath):
        self.rootFilePath = rootFilePath
    def __getItem__(self, index):
        raise NotImplementedError
    def length(self):
        raise NotImplementedError
    def load(self):
        raise NotImplementedError

class Mnist(Dataset):
    '''
    Class representing the Mnist "iterable" dataset. 
    The class stores the google drive file Id of each of the mnist dataset files. These Ids are essential to download the files if they are not available in the specified root path.
    It also stores the names of gzip files that contains the training and test sets. 
    "Set" here refers to the the combination of an image and a label.
    The class stores the splitted training, validation and test sets in numpy arrays.
    The class finally stores __index and iterate_on_attr attributes which used in iterating on the datasets
    '''
    trainingImagesId = '1AFEVsHzlT8H_avcouMl694PwFEyNzirr'
    trainingLabelsId = '1rhFLe9WbSK8bnbXnglX9b4AgOB7tfPsS'
    testImagesId = '1duWaOCrpieH9O9GKMR-xIUSzRJNFyVOQ'
    testLabelsId = '1IEhyDpgPgKv-S6Sx7AIufUmjmH97Om6w'
    def __init__(self, rootFilePath, seed = 42, split_ratio = 0.2): 
        '''
        The __init__ function is called whenever the class is instantiated. 
        Arguments: 
            rootFilePath: String represents the path to the root folder in which the dataset files are stored. If the files were not found, the object notifies the user that it will procceed downloading the dataset files online from the internet.
            seed: Integer represents the seed of the random process of numpy. numpy.random is used to randomly shuffle the training set. The user can set the seed of the random shuffling to match a constant seed he/she wants across the code.
            split_ratio: float represents the ratio by which the mnist training files are split into validation and training sets. The split_ratio equals the required portion of validation set of the total given mnist training set. If the user needs to do the split manually, the he/she can set the split_ratio to zero and the object stores only training and test sets.
        '''
        super(Mnist, self).__init__(rootFilePath)
        self.trainingImagesName = os.path.join(self.rootFilePath, 'train-images-idx3-ubyte.gz')
        self.trainingLabelsName = os.path.join(self.rootFilePath, 'train-labels-idx1-ubyte.gz')
        self.testImagesName = os.path.join(self.rootFilePath, 't10k-images-idx3-ubyte.gz')
        self.testLabelsName = os.path.join(self.rootFilePath, 't10k-labels-idx1-ubyte.gz')
        if not os.path.exists(self.trainingImagesName)\
           or not os.path.exists(self.trainingLabelsName)\
           or not os.path.exists(self.testImagesName)\
           or not os.path.exists(self.testLabelsName):
           response = input('Some files are missing. Do you want to download the dataset online? [y/n]')
           if response.lower() == "n":
               raise SystemExit()
           else:
               download_file_from_google_drive(self.trainingImagesId, self.trainingImagesName, "Training Images")
               download_file_from_google_drive(self.trainingLabelsId, self.trainingLabelsName, "Training Labels")
               download_file_from_google_drive(self.testImagesId, self.testImagesName, "Test Images")
               download_file_from_google_drive(self.testLabelsId, self.testLabelsName, "Test Labels")
        training_and_validation_images = self.get_images(self.trainingImagesName).copy()
        training_and_validation_labels = self.get_labels(self.trainingLabelsName).copy()
        np.random.seed(seed)
        state = np.random.get_state()
        np.random.shuffle(training_and_validation_images)
        np.random.set_state(state)
        np.random.shuffle(training_and_validation_labels)
        training_end_index = int((1 - split_ratio)*len(training_and_validation_images))
        self.training_images = training_and_validation_images[:training_end_index]
        self.training_labels = training_and_validation_labels[:training_end_index]
        self.validation_images = training_and_validation_images[training_end_index:]
        self.validation_labels = training_and_validation_labels[training_end_index:]
        self.test_images = self.get_images(self.testImagesName)
        self.test_labels = self.get_labels(self.testLabelsName)
        self.__index = 0
        self.iterate_on_attr = "training"
    def iterate_on(self, iterate_on):
        '''
        Specifies which set (training, validation or test) is to be iterated on.
        Arguments:
            iterate_on: string indicates the set to be iterated on.
        '''
        self.iterate_on_attr = iterate_on
    def load(self):
        '''
        Returns:
            training_images: array of shape (<num_of_training_imgs>, 28, 28) contains training images, each of 28x28 shape.
            training_labels: array of shape (<num_of_training_imgs>, 1) contains the labels corresponding to the training images.
            validation_images: array of shape (<num_of_validation_imgs>, 28, 28) contains validation images, each of 28x28 shape.
            validation_labels: array of shape (<num_of_validation_imgs>, 1) contains the labels corresponding to the validation images.
            test_images: array of shape (10000, 28, 28) contains test images, each of 28x28 shape.
            test_labels: array of shape (10000, 1) contains the labels corresponding to the test images.
        '''
        return self.training_images, self.training_labels, self.validation_images, self.validation_labels, self.test_images, self.test_labels
    def __getItem__(self, index, from_set = "training", all = False):
        '''
        Gets an item of a specific set at a specific index.
        Arguments:
            index: Integer represents the index of the specified set from which an item (image + label) is gotten.
            from_set: String represents the set from which the item (image + label) is gotten.
            all: Boolean that if set true, the function returns a specific item the is combined of one training image, one training label, one validation image, one validation label, one test image and one test label.
        Returns:
            PILImage: Python Imaging Library (PIL) image from an array at the given index from the given set.
            intLabels: Integer represents the label that corresponds to the returned PIL Image.
        '''
        from_set = from_set.lower()
        if from_set == "training" and not all:
            PILImage = Image.fromarray(self.training_images[index], mode= 'L') 
            # mode = 'L' indicates 8 bits black and white images
            intLabels = self.training_labels[index].item()
        elif from_set == "test" and not all:
            PILImage = Image.fromarray(self.test_images[index], mode= 'L') 
            intLabels = self.test_labels[index].item()
        elif from_set == "validation" and not all:
            PILImage = Image.fromarray(self.validation_images[index], mode= 'L') 
            intLabels = self.validation_labels[index].item()
        elif all:
            return Image.fromarray(self.training_images[index], mode= 'L'),\
            self.training_labels[index].item(),\
            Image.fromarray(self.validation_images[index], mode= 'L'),\
            self.validation_labels[index].item(),\
            Image.fromarray(self.test_images[index], mode= 'L'),\
            self.test_labels[index].item()
        return PILImage, intLabels
    def length(self, set = "training"):
        '''
        Gets the length of a specified set.
        Arguments:
            set: String represents the set which its length is required.
        Returns:
            The length of the specified set.
        '''
        set = set.lower()
        if set == "training":
            return len(self.training_images)
        elif set == "test":
            return len(self.test_images)
        elif set == "validation":
            return len(self.validation_images)
    def __iter__(self):
        '''
        The function required to make the dataset iterable.
        '''
        self.__index = 0
        return self 
    def __next__(self):
        '''
        The function that gets the next item from the iterable.
        Returns:
            The next item from the set specified by the iterate_on_attr.
        '''
        if self.__index < self.length(self.iterate_on_attr):
            next = self.__getItem__(self.__index, from_set = self.iterate_on_attr)
            self.__index += 1
            return next
        else:
            raise StopIteration
    def generate(self, from_set = "training", index= 0):
        '''
        Generator function that continously generates items from the specifed set starting from a given index.
        Arguments:
            from_set: String indicates the set that items are being generated from.
            index: Integer indicates the place from which the function starts the generation.
        Yields (Actually it returns continously):
            An item of the given set at the given item. 
        '''
        internal_index = index
        while True:
            if internal_index < self.length(from_set):
                yield self.__getItem__(internal_index, from_set = from_set)
                internal_index += 1
            else: 
                break
    def showSample(self, from_set = "training", startFrom= 0, coloumn= 5, row= 5, figsize= (10, 10)):
        '''
        Plots a sample of images and labels from a given set.
        Arguments:
            from_set: String indicates the set that the shown sample is from.
            startFrom: Integer indicates the index from which the function will visualize a set of images.
            coloumn: Integer indicates number of coloumns of images is required. 
            row: Integer indicates number of rows of images is required. 
            figsize: Tuple of two integers indicates the area of an image (passed to matplotlib.pyplot.plot).
        '''
        from_set = from_set.lower()
        fig = plt.figure(figsize= figsize)
        mnist_iter = self.generate(from_set, startFrom)
        for i in range(1, coloumn*row+1):
            img, label = next(mnist_iter)
            ax = fig.add_subplot(row, coloumn, i)
            ax.title.set_text('Label: ' + str(label))
            plt.imshow(img)
            plt.axis('off')
        plt.show()
    def read_idx_file(self, f, num_bytes= 4, endianness= 'big'):
        '''
        Reads specific number of bytes from a given .idx file (used to store the mnist dataset) taking endianness into consideration.
        Arguments:
            f: .idx (index) file.
            num_bytes: Integer number of bytes to be read from the given .idx file.
            endianness: String specifies the endianness of the given file. (C.O. Lesson: Endianness-> The way computer stores the bytes in memory. Big endian processor stores the most significant byte in the highest memory address and vice versa)
        Returns:
            Series of integers from the read bytes.
        '''
        return int.from_bytes(f.read(num_bytes), endianness)
    def get_images(self, compressedFilePath):
        '''
        Transforms the raw bytes read from the idx file into images.
        Arguments:
            compressedFilePath: String represents the path of the compressed gzip file.
        Returns:
            images: Array of integers ranging from 0 to 255 representing the images in the given file.
        '''
        with gzip.open(compressedFilePath, 'r') as f:
            magicNumber = self.read_idx_file(f) # Used to make sure that the file is read correctly.
            try:
                assert magicNumber == 2051 
            except:
                print('Error getting images (Magic number error)')
                raise SystemExit()
            num_images = self.read_idx_file(f) 
            num_rows = self.read_idx_file(f)
            num_coloumns = self.read_idx_file(f)
            rest_values = f.read()
            images = np.frombuffer(rest_values, dtype = np.uint8).reshape((num_images, num_rows, num_coloumns))
            return images
    def get_labels(self, compressedFilePath):
        '''
        Transforms the raw bytes read from the idx file into labels.
        Arguments:
            compressedFilePath: String represents the path of the compressed gzip file.
        Returns:
            labels: Array of integers ranging from 0 to 9 representing the labels corresponding to the images in the given file.
        '''
        with gzip.open(compressedFilePath, 'r') as f:
            magicNumber = self.read_idx_file(f) # Used to make sure that the file is read correctly.
            try:
                assert magicNumber == 2049 
            except:
                print('Error in training labels (Magic number error)')
                raise SystemExit()
            num_labels = self.read_idx_file(f)
            rest_values = f.read()
            labels = np.frombuffer(rest_values, dtype = np.uint8).reshape((num_labels, 1))
            return labels

# test the iterable training dataset MNIST
mnist = Mnist('../mnist/new')
# print(mnist.length("validation"))
# counter = 0
# for image, label in mnist_training:
#     if counter == 3:
#         print (image)
#         print (label)
#     counter += 1
# print(counter)

# test the generator function.
mnist.showSample(from_set= "training", startFrom= 0)