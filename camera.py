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

def _paint_menu(window,colors):

	colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
	colorIndex = 0

	# Setup the Paint interface
	window = cv2.line(window, (150,0), (150,500), (0,0,0), 4)
	window = cv2.rectangle(window, (10,5), (140,50), colors[0], -1)
	window = cv2.rectangle(window, (10,60), (140,105), colors[1], -1)
	window = cv2.rectangle(window, (10,115), (140,160), colors[2], -1)
	window = cv2.rectangle(window, (10,170), (140,215), colors[3], -1)

	window = cv2.circle(window, (75,245), 10, (0,0,0), -1)
	window = cv2.circle(window, (75,285), 20, (0,0,0), -1)
	window = cv2.circle(window, (75,345), 30, (0,0,0), -1)
	window = cv2.circle(window, (75,425), 40, (0,0,0), -1)

	cv2.putText(window, "AZUL", (55, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
	cv2.putText(window, "VERDE", (53, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
	cv2.putText(window, "ROJO", (55, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
	cv2.putText(window, "AMARILLO", (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

	return window

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

paintWindow = np.zeros((471,636,3)) + 255
paintWindow = _paint_menu(paintWindow,colors)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
   
    object_point_one, object_point_two, object_half_point = objectUtils.identify_object(frame)

    if ((object_point_one and object_point_two) and
     (object_point_one[0] >= MENU_LIMIT_AREA and object_point_two[0] >= MENU_LIMIT_AREA)):

    	frame = cv2.rectangle(frame,object_point_one,object_point_two,(0, 255, 0),4)
    	frame = cv2.circle(frame, object_half_point, 10, (0,255,0), -1)
    	cv2.circle(paintWindow, object_half_point, 10, (0,255,0), -1)

    frame = delimit_screen(frame)
    cv2.imshow('frame',frame)
    cv2.imshow("Paint", paintWindow)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()