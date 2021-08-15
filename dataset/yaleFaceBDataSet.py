import os
import abc
import random
from abc import abstractmethod

import numpy as np
from keras_preprocessing.image import load_img, img_to_array
from skimage import io
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.applications.vgg16 import preprocess_input
from tensorflow.python.keras.utils import np_utils

from util import constant
from util.common import Common



from .faceDataSet import FaceDataSet


class YaleFaceBDataSet(FaceDataSet):

    def __init__(self, path, ext_list, n_classes):
        super().__init__(path, ext_list, n_classes)

    def process_label(self, img_path):
        val = int(os.path.split(img_path)[1].split("_")[0].replace("yaleB", ""))
        if 14 > val:
            val = val - 11
        else:
            val = val - 12
        if val not in self.labels:
            self.number_labels += 1
        return val

    def fetch_img_path(self, img_path_list, path, keras_img_processing):
        images = []
        labels = []
        for (i, dir_path) in enumerate(img_path_list):
            im_path = os.listdir(path + "\\" + dir_path)
            im_path = [p for p in im_path if p.endswith(".pgm")]
            im_path = np.random.choice(im_path, size=250)
            for (j, img_path) in enumerate(im_path):
                if self.check_ext(path + "\\" + dir_path + "\\" + img_path):
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
                    if j > 250:
                        break
            if i >= (self.n_classes - 1):
                break
        return images, labels
