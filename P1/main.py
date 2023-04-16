import cv2

cap = cv2.VideoCapture("E:\\14_STUDIUM\\Multitouch\\Praktikum\\P1\\mt_camera_raw.AVI")
if(cap):
    print("Loaded")
    success, img = cap.read()

    while(success):
        success, img = cap.read()
        cv2.imshow("Img", img);
        cv2.waitKey(0)
