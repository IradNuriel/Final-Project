import time

import keras
from keras.preprocessing import image
from keras_vggface.utils import decode_predictions
from keras_vggface.utils import preprocess_input
from numpy import expand_dims
from tensorflow.python.keras import Input
from tensorflow.python.keras.applications.inception_v3 import preprocess_input
from tensorflow.python.keras.layers import MaxPooling2D, Dense, Flatten, Convolution2D, BatchNormalization, Activation
from tensorflow.python.keras.models import Model
from keras_vggface.vggface import VGGFace
from datetime import datetime
from my_face_recognition.machineLearningModel import MLModel
from my_face_recognition.layers.arcfaceLayer import ArcFace
from util import constant
import os


class VggModel(MLModel):

    def __init__(self, dataSet=None, weights_path=None):
        super().__init__(dataSet, weights_path)
        self.runID = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        try:
            if weights_path is None:
                os.mkdir("weights\\" + self.runID)
        except OSError as err:
            print(err)
        opt = keras.optimizers.Adam(learning_rate=0.001)
        self.vgg.compile(loss=keras.losses.binary_crossentropy,
                         optimizer=opt,
                         metrics=[constant.METRIC_ACCURACY])

    def init_model(self, weights_path=None):  # build model
        inp = Input(shape=(constant.IMG_WIDTH, constant.IMG_HEIGHT, 3))
        label = Input(shape=(self.n_classes,))
        base_model = VGGFace(weights=None, include_top=False, input_tensor=inp, pooling='max', model='vgg16', classes=2622)
        base_model.summary()

        for layer in base_model.layers:
            layer.trainable = False

        x = base_model.get_layer('pool5').output
        # Stacking a new simple convolutional network on top of it
        x = Flatten(name='flatten')(x)
        x = Dense(4096, name='fc6')(x)
        x = Activation('relu', name='fc6/relu')(x)
        x = Dense(4096, name='fc7')(x)
        x = Activation('relu', name='fc7/relu')(x)

        if not constant.ARCFACE:
            x = Dense(2622, name='fc8')(x)
            x = Activation('softmax', name='fc8/softmax')(x)
            self.vgg = Model(inputs=base_model.input, outputs=x)
        else:
            x = BatchNormalization()(x)
            x = ArcFace(num_classes=self.n_classes, dynamic=True)([x, label])
            self.vgg = Model(inputs=[base_model.input, label], outputs=x)
        if weights_path:
            self.vgg.load_weights(weights_path)
        self.vgg.summary()

    def get_model(self):
        return self.vgg

    def train(self, n_epochs=50, batch=32):
        callbacks = [
            keras.callbacks.ModelCheckpoint("weights\\" + self.runID + "\\save_at_{epoch}.h5"),
        ]
        if constant.ARCFACE:

            self.vgg.fit([self.objects, self.labels], self.labels,
                         batch_size=batch,
                         epochs=n_epochs,
                         verbose=1,
                         validation_data=([self.obj_validation, self.labels_validation], self.labels_validation),
                         callbacks=callbacks,
                         use_multiprocessing=True)

        else:
            self.vgg.fit(self.objects, self.labels,
                         batch_size=batch,
                         epochs=n_epochs,
                         validation_data=(self.obj_validation, self.labels_validation),
                         callbacks=callbacks)

    def __process_img(self, img):
        img = image.load_img(img)
        img = image.img_to_array(img)
        return preprocess_input(expand_dims(img, axis=0), version=2)

    def predict(self, img_path):
        pixels = self.__process_img(img_path)
        preds = self.vgg.predict(pixels)
        return decode_predictions(preds)

    def evaluate(self):
        score = self.get_model().evaluate([self.obj_validation, self.labels_validation], self.labels_validation,
                                          verbose=0)
        print("%s: %.2f%%" % (self.get_model().metrics_names[1], score[1] * 100))

    def get_feature_model(self):
        opt = keras.optimizers.Adam(learning_rate=0.001)
        if constant.ARCFACE:
            vgg_features = Model(inputs=[self.vgg.inputs], outputs=[self.vgg.layers[-3].output])
        else:
            vgg_features = Model(inputs=[self.vgg.inputs], outputs=[self.vgg.get_layer('flatten').output])
        vgg_features.compile(loss=keras.losses.binary_crossentropy,
                             optimizer=opt,
                             metrics=[constant.METRIC_ACCURACY])
        vgg_features.summary()
        return vgg_features
