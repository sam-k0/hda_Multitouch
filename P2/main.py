import cv2
from time import sleep
import math
import classes as p2
background = None
original = None
MIN_THRESHOLD = 8
CONTOURS_VAL_MIN = 30
CONTOURS_VAL_MAX = 100

COLOR_RED = (0,0,255)
COLOR_GREEN = (0,255,0)

myTracker = p2.Tracker(threshold=20)

cap = cv2.VideoCapture("C:\\Users\\Samuel\\Documents\\Studium\\MI - Multitouch Interfaces\\hda_Multitouch\\P1\\mt_camera_raw.AVI")
#cap = cv2.VideoCapture("E:\\14_STUDIUM\\Multitouch\\Praktikum\\mat\\mt_camera_raw.AVI")
if(cap):
    print("Loaded")
    success, img = cap.read()
    background = img

    while(success):
        success, img = cap.read()
        if not success:
            cv2.destroyAllWindows()
            print("Done.")
            break   

        
        # Tracker settings
        myTracker.clearCurrentFrame(); #clears all blobs

        original = img
        firstDiff = cv2.absdiff(background, img)
        firstBlur = cv2.blur(firstDiff, (15,15))
        secondDiff = cv2.absdiff(firstDiff, firstBlur)
        secondBlur = cv2.blur(secondDiff, (6,6))
        processed = cv2.cvtColor(secondBlur, cv2.COLOR_BGR2GRAY)

        ret, processed = cv2.threshold(processed, MIN_THRESHOLD,255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(processed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        if hierarchy is not None:
            for idx in range(len(hierarchy[0])):
                if CONTOURS_VAL_MAX > cv2.contourArea(contours[idx]) > CONTOURS_VAL_MIN and len(contours[idx]) > 4:
                    cEllipse = cv2.fitEllipse(contours[idx])
                    # pass new to tracker list for this frame
                    bruhMoment=cv2.moments(contours[idx])
                    cx = int(bruhMoment['m10']/bruhMoment['m00'])
                    cy = int(bruhMoment['m01']/bruhMoment['m00'])

                    myTracker.addBlobToFrame((cx,cy))
                    
                    cv2.ellipse(original, cEllipse, COLOR_RED, 1, cv2.LINE_AA)
                    cv2.drawContours(original, contours, idx, COLOR_GREEN, 1, cv2.LINE_AA, hierarchy=hierarchy)

        b:p2.Blob      
        for b in myTracker.currentFrameBlobs:
            cv2.circle(img, b.getTuple(), 1, COLOR_RED, -1)
        # evaluate tracker
        myTracker.updateTouches()

        t: p2.Touch
        print("Printing touches ({}):".format(len(myTracker.touches)))
        for t in myTracker.touches:
            print("Touch {} has blob pos {}:{}".format(t.id, t.blob.x, t.blob.y))
            cv2.putText(original, str(t.id), t.getTuple(), cv2.FONT_HERSHEY_SIMPLEX, 0.5,COLOR_GREEN)

        
        cv2.imshow("Img", processed);
        cv2.imshow("Img2", original);
        #sleep(0.5)
        cv2.waitKey(0)
 