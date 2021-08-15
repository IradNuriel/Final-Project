import os
import sys
import time
import math
import numpy as np
from seal import *


def add_vectors(vec1, vec2, evaluator):
    vec1_plus_vec2 = []
    for i in range(len(vec1)):
        vec1_plus_vec2.append(evaluator.add(vec1[i], vec2[i]))
    return vec1_plus_vec2


def mul_vectors(vec1, vec2, evaluator):
    vec1_mul_vec2 = []
    for i in range(len(vec1)):
        vec1_mul_vec2.append(evaluator.multiply(vec1[i], vec2[i]))
    return vec1_mul_vec2


def sub_vectors(vec1, vec2, evaluator):
    vec1_minus_vec2 = []
    for i in range(len(vec1)):
        vec1_minus_vec2.append(evaluator.sub(vec1[i], vec2[i]))
    return vec1_minus_vec2


def save_encrypted_vector_in_memory(vec, name, path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(f"{path}/cipher_{name}"):
            os.mkdir(f"{path}/cipher_{name}")
        else:
            l = os.listdir(f"{path}/cipher_{name}")
            for bit in l:
                os.remove(os.path.join(f"{path}/cipher_{name}", bit))

    except OSError as err:
        print(err)
    n = len(vec)

    for (i, x) in enumerate(vec):
        x.save(f'{path}/cipher_{name}/element_{str(i).zfill(int(np.floor(np.log10(n))+1))}')


def save_encrypted_binary_vector_in_memory(b, name, path):
    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except OSError as err:
        print(err)
    b.save(f"{path}/cipher_{name}")


def load_encrypted_binary_vector_from_memory(ctx, name, path):
    if not os.path.exists(f"{path}/cipher_{name}"):
        print("WRONG CIPHER NAME")
        raise IOError
    b = Ciphertext()
    b.load(ctx, f"{path}/cipher_{name}")
    return b


def load_encrypted_vector_from_memory(ctx, name, path):
    vec = []
    if not os.path.exists(f"{path}/cipher_{name}"):
        print("WRONG CIPHER NAME")
        raise IOError
    l = os.listdir(f"{path}/cipher_{name}")
    for bit in l:
        x = Ciphertext()
        x.load(ctx, os.path.join(f"{path}/cipher_{name}", bit))
        vec.append(x)
    return vec


def sum_elements(vec, evaluator):
    sums = Ciphertext(vec[0])
    for enc in vec:
        evaluator.add_inplace(sums, enc)
    return sums


def encrypt_number_to_ciphertext_array(n, encryptor, length):
    n = format(n, "b")
    n = list(n)
    n = ['0']*(length-len(n)) + n
    enc = []
    for i in range(length):
        enc.append(encryptor.encrypt(Plaintext(n[i])))
    return enc


def encrypt_vector(vec, encryptor, length):
    enc = []
    for i in range(length):
        enc.append(encryptor.encrypt(Plaintext(f"{vec[i]:X}")))
    return enc


def encrypt_binary_vector(vec, encryptor):
    pol = ""
    for (i, a) in enumerate(vec):
        if a == 1:
            s = "1x^"+str(i)
            if pol == "":
                pol = s
            else:
                pol = s + " + " + pol
    pl = Plaintext(pol)
    return encryptor.encrypt(pl)


def hamming_dist(vec1, vec2, evaluator):
    a_minus_b = evaluator.sub(vec1, vec2)
    return a_minus_b











