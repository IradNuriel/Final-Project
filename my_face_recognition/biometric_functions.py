import gc
import os
import pickle

from numpy import expand_dims
from keras.preprocessing import image
from keras_vggface.utils import preprocess_input
from homomorphic_encryption_stuff.EncryptionStuff import hamming_dist, save_encrypted_binary_vector_in_memory, load_encrypted_binary_vector_from_memory
from homomorphic_encryption_stuff.getEncryptionInfo import *
from dataset.yaleFaceBDataSet import YaleFaceBDataSet
from my_face_recognition.model.vggModel import VggModel
from util import constant
from face_detection.FaceAlignment import *



def initialize_model_params(weights_path):
    dataSet = YaleFaceBDataSet(constant.YALE_FACE_B_DATA_PATH, ['pgm'], 28)
    model = VggModel(dataSet, weights_path)
    features_model = model.get_feature_model()
    enrolled_users = get_all_enrolled_users()
    
    return features_model, enrolled_users


def __process_img(img):
    img = image.smart_resize(img, size=(constant.IMG_WIDTH, constant.IMG_HEIGHT))
    img = image.img_to_array(img)
    img = preprocess_input(expand_dims(img.astype(np.float64), axis=0), version=2)
    return img


def predict(m, img):
    pixels = __process_img(img)
    preds = m.predict(pixels)
    return preds[0]


def get_all_enrolled_users():
    users_names = os.listdir(constant.CIPHERS_PATH)
    users_names = [user_name.replace("cipher_", "") for user_name in users_names]
    all_users = {}
    for username in users_names:
        users_features = load_encrypted_binary_vector_from_memory(context, username, constant.CIPHERS_PATH)
        all_users.update({username: users_features})
    return all_users


def who_is_this(features, encrypted):
    if not encrypted:
        features = np.where(features > 0, 1, 0)
        features = list(features) + [0] * (encoder.slot_count() - len(features))
        features = encryptor.encrypt(encoder.encode(features))
    closest = "non-enrolled user"
    closest_val = 5523
    for (user, user_features) in users.items():
        hd = hamming_dist(features, user_features, evaluator, relin_keys, galois_keys, context)
        hd = int(decryptor.decrypt(hd).to_string(), 16)
        if hd < closest_val:
            closest = user
            closest_val = hd
    return closest


def enroll(img, name):
    features = predict(feature_model, img)
    features = np.where(features > 0, 1, 0)
    features = list(features) + [0] * (encoder.slot_count() - len(features))
    encrypted_features = encryptor.encrypt(encoder.encode(features))
    del features
    gc.collect()
    if name in users.keys():
        this_is = who_is_this(encrypted_features, encrypted=True)
        if this_is == name:
            print("Already enrolled!\nNot enrolling this time.")
        return
    save_encrypted_binary_vector_in_memory(encrypted_features, name, constant.CIPHERS_PATH)
    users.update({name: encrypted_features})
    return


def who_is_this_face(img):
    features = predict(feature_model, img)
    features = np.where(features > 0, 1, 0)
    features = list(features) + [0] * (encoder.slot_count() - len(features))
    encrypted_features = encryptor.encrypt(encoder.encode(features))
    del features
    gc.collect()
    this_is = who_is_this(encrypted_features, encrypted=True)
    return this_is.replace("_", " ")


feature_model, users = initialize_model_params(constant.WEIGHTS_PATH)

