import numpy as np
import cv2
import objectUtils

MENU_LIMIT_AREA = 150

def delimit_screen(frame):
	start_point = (MENU_LIMIT_AREA,0)
	end_point = (MENU_LIMIT_AREA,500)
	color = (0,0,0)
	thickness = 4
	frame = cv2.line(frame, start_point, end_point, color, thickness)

	return frame

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
   
    object_point_one, object_point_two = objectUtils.identify_object(frame)

    if ((object_point_one and object_point_two) and
     (object_point_one[0] >= MENU_LIMIT_AREA and object_point_two[0] >= MENU_LIMIT_AREA)):

    	frame = cv2.rectangle(frame,object_point_one,object_point_two,(0, 255, 0),4)

    frame = delimit_screen(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()