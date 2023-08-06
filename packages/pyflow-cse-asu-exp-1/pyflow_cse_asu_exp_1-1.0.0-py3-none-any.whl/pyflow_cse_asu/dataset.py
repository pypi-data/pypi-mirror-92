import numpy as np
import gzip
from PIL import Image
import cv2
import os
import requests
import matplotlib.pyplot as plt

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
    def __init__(self, rootFilePath):
        self.rootFilePath = rootFilePath
    def __getItem__(self, index):
        raise NotImplementedError
    def __len__(self):
        raise NotImplementedError
    def load(self):
        raise NotImplementedError

class Mnist(Dataset):
    trainingImagesId = '1AFEVsHzlT8H_avcouMl694PwFEyNzirr'
    trainingLabelsId = '1rhFLe9WbSK8bnbXnglX9b4AgOB7tfPsS'
    testImagesId = '1duWaOCrpieH9O9GKMR-xIUSzRJNFyVOQ'
    testLabelsId = '1IEhyDpgPgKv-S6Sx7AIufUmjmH97Om6w'
    def __init__(self, rootFilePath, seed = 42, split_ratio = 0.2): 
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
        self.iterate_on_attr = iterate_on
    def load(self):
        return self.training_images, self.training_labels, self.validation_images, self.validation_labels, self.test_images, self.test_labels
    def __getItem__(self, index, from_set = "training", all = False):
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
        set = set.lower()
        if set == "training":
            return len(self.training_images)
        elif set == "test":
            return len(self.test_images)
        elif set == "validation":
            return len(self.validation_images)
    def __iter__(self):
        self.__index = 0
        return self # zip(self.images, self.labels)
    def __next__(self):
        if self.__index < self.length(self.iterate_on_attr):
            next = self.__getItem__(self.__index, from_set = self.iterate_on_attr)
            self.__index += 1
            return next
        else:
            raise StopIteration
    def generate(self, from_set = "training", index= 0):
        internal_index = index
        while True:
            if internal_index < self.length(from_set):
                yield self.__getItem__(internal_index, from_set = from_set)
                internal_index += 1
            else: 
                break
    def showSample(self, from_set = "training", startFrom= 0, coloumn= 5, row= 5, figsize= (10, 10)):
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
        return int.from_bytes(f.read(num_bytes), endianness)
    def get_images(self, compressedFilePath):
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