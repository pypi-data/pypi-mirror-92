import pickle
import os

class Storage():
    def __init__(self):
        pass
    def save_model(self, model, file_name, save_path):
        '''
        This method saves the passed model into the passed path with the passed name.
        Attributes:
        model: Object of type model representing the current state of the model you want to save.
        file_name: Beautiful name of your choice for the file to be pickled. If you want to save many models, then every model MUST have a unique name. If an already exists file name passed, then the saved old model will be lost.
        save_path: The file path you want to save your model in. 
        '''
        file_path = os.path.join(save_path, file_name + ".pickle")
        if os.path.exists(file_path):
            print("WARNING: There is another model with the same name. The old one will be lost.")
        pickled_file = open(file_path, "wb")
        pickle.dump(model, pickled_file)
        pickled_file.close()
    def load_model(self, file_name, load_path):
        '''
        This method loads a model from the passed path with the passed name.
        Attributes:
        file_name: Name of the file you saved your model in. If there is not a .pickle file with the same name, the methods returns None.
        save_path: The file path you want to load your model from.
        '''
        file_path = os.path.join(load_path, file_name + ".pickle")
        if not os.path.exists(file_path):
            print("File not found")
            return None
        unpickled_file = open(file_path, "rb")
        model = pickle.load(unpickled_file)
        unpickled_file.close()
        return model