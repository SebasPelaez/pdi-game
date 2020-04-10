import numpy as np
import cv2
import objectUtils
import os

MENU_LIMIT_AREA = 150
PAINT_WINDOW_SHAPE = (620,426)

def _get_border_image(paint_window, image_name):
	image_path = os.path.join('Imagenes','Generadas','{}.jpg'.format(image_name))
	image_border_path = os.path.join('Imagenes','Generadas','{}_border.jpg'.format(image_name))
	
	cv2.imwrite(image_path,paint_window)
	image = cv2.imread(image_path,1)
	
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	border = cv2.Canny(gray,100,200)
	
	cv2.imwrite(image_border_path,border)
	
def _compute_score():
	image_border_original_path = os.path.join('Imagenes','Generadas','unpainted_image_border.jpg')
	image_border_painted_path = os.path.join('Imagenes','Generadas','painted_image_border.jpg')
	image_original = cv2.imread(image_border_original_path)
	image_painted = cv2.imread(image_border_painted_path)

	image_original = image_original[30:,150:]
	image_painted = image_painted[30:,150:]

	image_intersection = _get_overlap(image_original,image_painted)
	image_union = _get_union(image_original,image_painted)

	pixels_in_original = _count_pixels_in_binarized_images(image_original)
	pixels_in_painted = _count_pixels_in_binarized_images(image_painted)

	iou = image_intersection/image_union
	border_error = image_intersection/pixels_in_original

	metric = np.absolute(iou-border_error)

	return metric

def _count_pixels_in_binarized_images(image):

	_ , image_binarized = cv2.threshold(image, 170, 255, cv2.THRESH_BINARY)
	mask = image_binarized == 255
	num_pixels = np.sum(mask)

	return num_pixels

def _get_overlap(image_A,image_B):

	image_intersection = cv2.bitwise_and(image_A,image_B)
	overlap = _count_pixels_in_binarized_images(image_intersection)

	return overlap

def _get_union(image_A,image_B):

	image_intersection = cv2.bitwise_or(image_A,image_B)
	union = _count_pixels_in_binarized_images(image_intersection)

	return union


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

def _paint_counter(window,time_elapsed):

	window = cv2.rectangle(window, (570,6), (620,26), (255,255,255), -1)
	cv2.putText(window, str(time_elapsed), (575, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

	return window

def _paint_results(window,score):
	cv2.putText(window, "FELICIDADES", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, "TU PUNTAJE", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, "ES", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, str(np.round(score,4)*100), (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)


def _paint_rules(window,colors,idx,brushes,brush_idx):

	cv2.putText(window, "Parate sobre el", (19, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, "color o la brocha", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, "que desees", (35, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)

	cv2.putText(window, "Color Seleccionado", (160, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
	window = cv2.rectangle(window, (312,6), (350,26), colors[idx], -1)
	cv2.putText(window, "Brocha Seleccionada", (360, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
	window = cv2.rectangle(window, (525,6), (550,26), (255,255,255), -1)
	cv2.putText(window, str(brushes[brush_idx]), (530, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

	return window

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
brushes = [10,20,30]
color_idx = 0
brush_idx = 0

paintWindow = _get_draw_image()
paintWindow = _paint_menu(paintWindow,colors)
paintWindow = _paint_rules(paintWindow,colors,color_idx,brushes,brush_idx)

cap = cv2.VideoCapture(0)
time_to_win = 50

_get_border_image(paintWindow, 'unpainted_image')

hidden_layer = np.zeros(PAINT_WINDOW_SHAPE)
hidden_layer = cv2.resize(hidden_layer,PAINT_WINDOW_SHAPE)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
   
    object_point_one, object_point_two, object_half_point = objectUtils.identify_object(frame)

    if object_point_one and object_point_two:

    	if object_point_one[0] >= MENU_LIMIT_AREA and object_point_two[0] >= MENU_LIMIT_AREA:

    		frame = cv2.rectangle(frame,object_point_one,object_point_two,colors[color_idx],4)
	    	frame = cv2.circle(frame, object_half_point, brushes[brush_idx], colors[color_idx], -1)
	    	cv2.circle(paintWindow, object_half_point, brushes[brush_idx], colors[color_idx], -1)
	    	cv2.circle(hidden_layer, object_half_point, brushes[brush_idx], colors[color_idx], -1)
    	
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
    paintWindow = _paint_counter(paintWindow,time_to_win)

    cv2.imshow('frame',frame)
    cv2.imshow("Paint", paintWindow)
    if (cv2.waitKey(20) & 0xFF == ord('q')) or time_to_win <= 0:
    	_get_border_image(paint_window=hidden_layer, image_name='painted_image')
    	break

    time_to_win -= 1


cv2.destroyAllWindows()

score = _compute_score()
results_window = _get_draw_image()
_paint_results(results_window,score)
cv2.imshow('RESULTADOS',results_window)
cv2.waitKey()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()