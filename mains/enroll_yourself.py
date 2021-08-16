import sys
import os
conf_path = os.getcwd()
sys.path.append(conf_path)
sys.path.append(conf_path+"my_face_recognition")
from my_face_recognition.biometric_functions import *
import cv2
import subprocess
from mains.send_mail import send_mail
import time
from util import constant
import base64


if __name__ == "__main__":
	img = cv2.imread(input("input a url to your photo: "))
	name = input("input a url to your full name: ")
	faces, dets = faceAlignmentAndCropping(img)
	if len(faces) != 1:
		print("Can't enroll!\nChoose better image of you where you and only you can be seen!")
		exit()
	enroll(faces[0], name)