from my_face_recognition.biometric_functions import *
import cv2



def main():
    cap = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    reiter = cv2.VideoWriter(constant.WRITE_TO, fourcc, 15, (1280, 720))
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("end")
            break
        i += 1
        if i % 2 != 0:
            continue
        faces, dets = faceAlignmentAndCropping(frame)
        print(dets)
        for j, det in enumerate(dets):
            print(det)
            frame = cv2.rectangle(frame, (det.left(), det.top()), (det.right(), det.bottom()), color=(0, 255, 0), thickness=1)
            if len((os.listdir(constant.CIPHERS_PATH))) > 0:
                realname = who_is_this_face(faces[j])
                cv2.putText(frame, realname, (det.left(), det.top()-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color=(0, 255, 0), thickness=1)
        reiter.write(frame.astype(np.uint8))
        cv2.imshow("camera", frame)
        key = cv2.waitKey(1)
        if key != -1:
            if key == ord("q"):
                print("end")
                break
            if key == ord("n"):
                if len(faces) == 1:
                    name = input("insert user name:\n>>>")
                    if name == "cancel":
                        continue
                    enroll(faces[0], name)
                else:
                    print("only one person at a time can be enrolled.")

    cap.release()
    reiter.release()
    cv2.destroyAllWindows()


main()