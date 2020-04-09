import numpy as np
import cv2
import objectUtils
import os

MENU_LIMIT_AREA = 150

def _get_border_image(paint_window, image_name):
	image_path = os.path.join('Imagenes','Generadas','{}.jpg'.format(image_name))
	image_border_path = os.path.join('Imagenes','Generadas','{}_border.jpg'.format(image_name))
	cv2.imwrite(image_path,paint_window)
	image = cv2.imread(image_path,1)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	border = cv2.Canny(gray,100,200)
	cv2.imwrite(image_border_path,border)
	
def _pixel_counter():
	image_border_original_path = os.path.join('Imagenes','Generadas','frame_border.jpg')
	image_border_painted_path = os.path.join('Imagenes','Generadas','paint_border.jpg')
	image_original = cv2.imread(image_border_original_path)
	image_painted = cv2.imread(image_border_painted_path)
	#image_painted = image_painted[80:,:]

	image_original = cv2.resize(image_original,(600,470))
	image_painted = cv2.resize(image_painted,(600,470))

	image_intersection = cv2.bitwise_and(image_original,image_painted)
	_,image_binarized = cv2.threshold(image_intersection, 170, 255, cv2.THRESH_BINARY) #investigar después porque 170

	mask = image_binarized == 255
	return np.sum(mask)

def _get_draw_image():
	images = os.listdir(os.path.join('Imagenes','Dibujos'))
	random = np.random.randint(0,len(images))

	random_image_path = os.path.join('Imagenes','Dibujos',images[random])
	random_image = cv2.imread(random_image_path)

	return random_image

def delimit_screen(frame):
	start_point = (MENU_LIMIT_AREA,0)
	end_point = (MENU_LIMIT_AREA,500)
	color = (0,0,0)
	thickness = 4
	frame = cv2.line(frame, start_point, end_point, color, thickness)

	return frame

def _paint_menu(window,colors):

	# Setup the Paint interface
	window = cv2.line(window, (150,0), (150,500), (0,0,0), 4)
	window = cv2.rectangle(window, (10,68), (140,108), colors[0], -1)
	window = cv2.rectangle(window, (10,115), (140,155), colors[1], -1)
	window = cv2.rectangle(window, (10,162), (140,202), colors[2], -1)
	window = cv2.rectangle(window, (10,209), (140,249), colors[3], -1)

	window = cv2.circle(window, (75,275), 10, (0,0,0), -1)
	window = cv2.circle(window, (75,315), 20, (0,0,0), -1)
	window = cv2.circle(window, (75,375), 30, (0,0,0), -1)

	cv2.putText(window, "AZUL", (55, 92), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
	cv2.putText(window, "VERDE", (53, 142), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
	cv2.putText(window, "ROJO", (55, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
	cv2.putText(window, "AMARILLO", (40, 235), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

	return window

def _paint_rules(window,colors,idx,brushes,brush_idx):

	cv2.putText(window, "Parate sobre el", (19, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, "color o la brocha", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, "que desees", (35, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)

	cv2.putText(window, "Color Seleccionado", (160, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
	window = cv2.rectangle(window, (312,6), (350,26), colors[idx], -1)
	cv2.putText(window, "Brocha Seleccionada", (360, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
	window = cv2.rectangle(window, (525,6), (550,26), (255,255,255), -1)
	cv2.putText(window, str(brushes[brush_idx]), (530, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

	return window

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
brushes = [10,20,30]
color_idx = 0
brush_idx = 0

paintWindow = np.zeros((471,636,3)) + 255
paintWindow = _get_draw_image()
paintWindow = _paint_menu(paintWindow,colors)
paintWindow = _paint_rules(paintWindow,colors,color_idx,brushes,brush_idx)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
   
    object_point_one, object_point_two, object_half_point = objectUtils.identify_object(frame)

    if object_point_one and object_point_two:

    	if object_point_one[0] >= MENU_LIMIT_AREA and object_point_two[0] >= MENU_LIMIT_AREA:

    		frame = cv2.rectangle(frame,object_point_one,object_point_two,colors[color_idx],4)
	    	frame = cv2.circle(frame, object_half_point, brushes[brush_idx], colors[color_idx], -1)
	    	cv2.circle(paintWindow, object_half_point, brushes[brush_idx], colors[color_idx], -1)
    	
    	else:

    		if object_half_point[0] >= 10 and object_half_point[0] <= 140:

	    		if object_half_point[1] >= 68 and object_half_point[1] <= 108:
	    			color_idx = 0
	    		elif object_half_point[1] >= 115 and object_half_point[1] <= 155:
	    			color_idx = 1
	    		elif object_half_point[1] >= 162 and object_half_point[1] <= 202:
	    			color_idx = 2
	    		elif object_half_point[1] >= 209 and object_half_point[1] <= 249:
	    			color_idx = 3

	    	if object_half_point[0] >= 75 and object_half_point[0] <= 100:

	    		if object_half_point[1] >= 275 and object_half_point[1] <= 295:
	    			brush_idx = 0
	    		elif object_half_point[1] >= 315 and object_half_point[1] <= 335:
	    			brush_idx = 1
	    		elif object_half_point[1] >= 375 and object_half_point[1] <= 395:
	    			brush_idx = 2
	       	
    frame = delimit_screen(frame)
    frame = _paint_menu(frame,colors)
    paintWindow = _paint_rules(paintWindow,colors,color_idx,brushes,brush_idx)

    cv2.imshow('frame',frame)
    cv2.imshow("Paint", paintWindow)
    if cv2.waitKey(20) & 0xFF == ord('q'):
    	_get_border_image(paint_window=frame, image_name='frame')
    	_get_border_image(paint_window=paintWindow, image_name='paint')
    	break


contador_pixeles = _pixel_counter()
print(contador_pixeles)
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()