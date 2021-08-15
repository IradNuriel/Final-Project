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
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    cnts = {}
    i = 0
    while i < 10:
        ret, frame = cap.read()
        if not ret:
            print("end")
            break
        faces, dets = faceAlignmentAndCropping(frame)
        if len(faces) > 0:
            i += 1
        print(dets)
        
        for j, det in enumerate(dets):
            print(det)
            frame = cv2.rectangle(frame, (det.left(), det.top()), (det.right(), det.bottom()), color=(0, 255, 0), thickness=1)
            realname = who_is_this_face(faces[j])
            cv2.putText(frame, realname, (det.left(), det.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color=(0, 255, 0), thickness=1)
            if realname not in cnts.keys():
                cnts.update({realname: 0})
            cnt = cnts[realname]
            cnt += 1
            cnts.update({realname: cnt})
        cv2.imshow("camera", frame)
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()
    maxname = ""
    maxvalue = 0
    for (name, value) in cnts.items():
        if maxvalue < value:
            maxname = name
            maxvalue = value

    if maxname in authenticated:
        subprocess.run([f"{constant.LOCKED_BATCH_PATH}\\locker.bat"], input=base64.decodebytes(bytes('MDg2NGFzenhjdg==', "ascii")), cwd=constant.LOCKED_DIR_PATH)
        num_explorers = subprocess.check_output(('TASKLIST', "/FO", "CSV")).decode().count("explorer.exe")
        subprocess.run(['explorer', '/separate,', f"{constant.LOCKED_DIR_PATH}\\Locker"])
        time.sleep(3)
        while subprocess.check_output(('TASKLIST', "/FO", "CSV")).decode().count("explorer.exe") > num_explorers:
            continue
        subprocess.run([f"{constant.LOCKED_BATCH_PATH}\\locker.bat"], input="y".encode(), cwd=constant.LOCKED_DIR_PATH)
    else:
        send_mail(maxname)


if __name__ == "__main__":
    main()
