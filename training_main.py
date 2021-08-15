
import numpy as np

from dataset.yaleFaceBDataSet import YaleFaceBDataSet
from dataset.yaleFaceDataSet import YaleFaceDataSet
from dataset.lfwDataSet import LFWDataSet
# Config

from my_face_recognition.model.convolutionalModel import ConvolutionalModel
from my_face_recognition.model.vggModel import VggModel
from util import constant


ext_list = ['gif', 'centerlight', 'glasses', 'happy', 'sad', 'leflight',
            'wink', 'noglasses', 'normal', 'sleepy', 'surprised', 'rightlight']
n_classes = 15
# Set up dataSet
x = "yalefaceB"   # input("Which dataset you want to work with?")
if x == "yaleface":
    dataSet = YaleFaceDataSet(constant.YALE_FACE_DATA_PATH, ext_list, n_classes)
elif x == "lfw":
    dataSet = LFWDataSet(constant.LFW_DATA_PATH, ['jpg'], 5751)
elif x == "yalefaceB":
    dataSet = YaleFaceBDataSet(constant.YALE_FACE_B_DATA_PATH, ['pgm'], 28)
else:
    dataSet = YaleFaceDataSet(constant.YALE_FACE_DATA_PATH, ext_list, n_classes)

exec_conv_model = False  # false to vgg
if exec_conv_model:
    dataSet.get_data()
    cnn = ConvolutionalModel(dataSet)
    cnn.train(n_epochs=50)
    cnn.evaluate()
    cnn.predict(np.expand_dims(dataSet.objects[1], axis=0))
else:
    dataSet.get_data(vgg_img_processing=True)
    vgg = VggModel(dataSet)
    vgg.train(batch=10, n_epochs=20)
    vgg.evaluate()
