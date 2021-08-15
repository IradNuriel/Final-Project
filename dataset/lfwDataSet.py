import os
import abc
import random
from abc import abstractmethod

import numpy
from keras_preprocessing.image import load_img, img_to_array
from skimage import io
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.applications.vgg16 import preprocess_input
from tensorflow.python.keras.utils import np_utils

from util import constant
from util.common import Common


from .faceDataSet import FaceDataSet


class LFWDataSet(FaceDataSet):

    def __init__(self, path, ext_list, n_classes):
        super().__init__(path, ext_list, n_classes)

    def process_label(self, img_path):
        val = int(os.path.split(img_path)[1].split(".")[0].replace("subject", "")) - 1
        if val not in self.labels:
            self.number_labels+=1
        return val

    def fetch_img_path(self, img_path_list, path, keras_img_processing):
        images = []
        labels = []
        for (i, dir_path) in enumerate(img_path_list):
            im_path = os.listdir(path + "\\" + dir_path)
            j = 0
            for img_path in im_path:
                if self.check_ext(path + "\\" + dir_path + "\\" + img_path):
                    j += 1
                    img_abs_path = os.path.abspath(os.path.join(path + "\\" + dir_path, img_path))
                    if keras_img_processing:
                        image = load_img(img_abs_path, target_size=(constant.IMG_WIDTH,
                                                                    constant.IMG_HEIGHT))
                        image = img_to_array(image)
                        image = Common.reshape_from_img(image)
                        image = preprocess_input(image)
                    else:
                        image = io.imread(img_abs_path, as_gray=False)
                    label = i
                    images.append(image)
                    labels.append(label)
                if j > 200:
                    break
            if i >= (self.n_classes-1):
                break
        return images, labels
