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
authenticated = ["Irad Nuriel"]
forbidden = ["Ronel Shor Packer"]


def main():
    cap = cv2.VideoCapture(0)  # open camera
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    cnts = {}
    i = 0
    while i < 10:  # find the person in each of 10 frames and count it
        ret, frame = cap.read()  # read frame
        if not ret:
            print("end")
            break
        faces, dets = faceAlignmentAndCropping(frame)  # detect faces in the frame
        if len(faces) > 0:
            i += 1
        
        for j, det in enumerate(dets):  # for each face in the frame
            frame = cv2.rectangle(frame, (det.left(), det.top()), (det.right(), det.bottom()), color=(0, 255, 0), thickness=1)
            realname = who_is_this_face(faces[j])  # find the person name
            cv2.putText(frame, realname, (det.left(), det.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color=(0, 255, 0), thickness=1)  # put bounding box with name of person above
            # add to the count of the person
            if realname not in cnts.keys():
                cnts.update({realname: 0})
            cnt = cnts[realname]
            cnt += 1
            cnts.update({realname: cnt})
        cv2.imshow("camera", frame)  # show frame
        cv2.waitKey(1)
    cap.release()  # release the camera
    cv2.destroyAllWindows()
    # find max name
    maxname = ""
    maxvalue = 0
    for (name, value) in cnts.items():
        if maxvalue < value:
            maxname = name
            maxvalue = value
    
    # if max name is authenticated, open folder, else send mail
    if maxname in authenticated:
        subprocess.run([f"{constant.LOCKED_BATCH_PATH}\\locker.bat"], input=base64.decodebytes(bytes('MDg2NGFzenhjdg==', "ascii")), cwd=constant.LOCKED_DIR_PATH)  # unhide folder
        num_explorers = subprocess.check_output(('TASKLIST', "/FO", "CSV")).decode().count("explorer.exe")  # get number of file explorer processes
        subprocess.run(['explorer', '/separate,', f"{constant.LOCKED_DIR_PATH}\\Locker"])  # open folder in new process
        time.sleep(3)
        while subprocess.check_output(('TASKLIST', "/FO", "CSV")).decode().count("explorer.exe") > num_explorers:  # wait till file explorer closed
            continue
        subprocess.run([f"{constant.LOCKED_BATCH_PATH}\\locker.bat"], input="y".encode(), cwd=constant.LOCKED_DIR_PATH)  # hide folder
    else:
        send_mail(maxname)  # send mail


if __name__ == "__main__":
    main()
