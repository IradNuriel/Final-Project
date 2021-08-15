import abc
from abc import abstractmethod

class MLModel(metaclass=abc.ABCMeta):

    def __init__(self, dataSet=None, weights_path=None):
        if dataSet is not None:
            self.objects = dataSet.objects
            self.labels = dataSet.labels
            self.obj_validation = dataSet.obj_validation
            self.labels_validation = dataSet.labels_validation
            self.number_labels = dataSet.number_labels
            self.n_classes = dataSet.n_classes
        if weights_path is not None:
            self.init_model(weights_path)
        else:
            self.init_model()

    @abstractmethod
    def init_model(self, weights_path=None):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def predict(self, object):
        pass

    @abstractmethod
    def evaluate(self):
        score = self.get_model().evaluate(self.obj_validation, self.labels_validation, verbose=0)
        print("%s: %.2f%%" % (self.get_model().metrics_names[1], score[1] * 100))

    @abstractmethod
    def get_model(self):
        pass