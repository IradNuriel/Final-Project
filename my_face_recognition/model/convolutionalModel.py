import numpy
from tensorflow.python.keras.layers import Convolution2D, Activation, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.python.keras.models import Sequential

from ..machineLearningModel import MLModel
from util import constant
from util.common import Common


class ConvolutionalModel(MLModel):

    def __init__(self, dataSet=None, weights_path=None):
        if dataSet is None:
            raise Exception("DataSet is required in this model")
        self.shape = numpy.array([constant.IMG_WIDTH, constant.IMG_HEIGHT, 1])
        super().__init__(dataSet, weights_path)
        self.cnn.compile(loss=constant.LOSS_FUNCTION,
                         optimizer=Common.get_sgd_optimizer(),
                         metrics=[constant.METRIC_ACCURACY])

    def init_model(self, weights_path=None):  # build model
        self.cnn = Sequential()
        self.cnn.add(Convolution2D(32, 3, padding=constant.PADDING_SAME, input_shape=self.shape))
        self.cnn.add(Activation(constant.RELU_ACTIVATION_FUNCTION))
        self.cnn.add(Convolution2D(32, 3, 3))
        self.cnn.add(Activation(constant.RELU_ACTIVATION_FUNCTION))
        self.cnn.add(MaxPooling2D(pool_size=(2, 2)))
        self.cnn.add(Dropout(constant.DROP_OUT_O_25))

        self.cnn.add(Convolution2D(64, 3, padding=constant.PADDING_SAME))
        self.cnn.add(Activation(constant.RELU_ACTIVATION_FUNCTION))
        self.cnn.add(Convolution2D(64, 3, 3))
        self.cnn.add(Activation(constant.RELU_ACTIVATION_FUNCTION))
        self.cnn.add(MaxPooling2D(pool_size=(2, 2)))
        self.cnn.add(Dropout(constant.DROP_OUT_O_25))

        self.cnn.add(Flatten())
        self.cnn.add(Dense(constant.NUMBER_FULLY_CONNECTED))
        self.cnn.add(Activation(constant.RELU_ACTIVATION_FUNCTION))
        self.cnn.add(Dropout(constant.DROP_OUT_0_50))
        self.cnn.add(Dense(self.n_classes))
        self.cnn.add(Activation(constant.SOFTMAX_ACTIVATION_FUNCTION))
        if weights_path:
            self.cnn.load_weights(weights_path)
        self.cnn.summary()

    def train(self, n_epochs=20, batch=32):
        self.cnn.fit(self.objects, self.labels,
                     batch_size=batch,
                     validation_data=(self.obj_validation, self.labels_validation),
                     epochs=n_epochs, shuffle=True)

    def get_model(self):
        return self.cnn

    def predict(self, image):
        image = Common.to_float(image)
        result = self.cnn.predict(image)
        print(result)

    def evaluate(self):
        super(ConvolutionalModel, self).evaluate()
