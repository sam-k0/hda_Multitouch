import cv2

background = None
original = None
MIN_THRESHOLD = 40
CONTOURS_VAL_MIN = 20
CONTOURS_VAL_MAX = 100
cap = cv2.VideoCapture("E:\\14_STUDIUM\\Multitouch\\Praktikum\\P1\\mt_camera_raw.AVI")
if(cap):
    print("Loaded")
    success, img = cap.read()
    background = img

    while(success):
        success, img = cap.read()
        original = img

        #img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed = cv2.absdiff(background, img)
        #processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        processed = cv2.blur(processed, (3,3))

        processed = cv2.absdiff(background, processed)
        
        processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        ret, processed = cv2.threshold(processed, MIN_THRESHOLD,255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(processed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        if hierarchy is not None:
            for idx in range(len(hierarchy[0])):
                if CONTOURS_VAL_MAX > cv2.contourArea(contours[idx]) > CONTOURS_VAL_MIN and len(contours[idx]) > 4:
                    cv2.ellipse(original, cv2.fitEllipse(contours[idx]), (0,0,255), 1, cv2.LINE_AA)
                    cv2.drawContours(original, contours, idx, (255,0,0), 1, cv2.LINE_AA, hierarchy=hierarchy)


        cv2.imshow("Img", processed);
        cv2.imshow("Img2", original);
        cv2.waitKey(0)
