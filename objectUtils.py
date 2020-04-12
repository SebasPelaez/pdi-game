"""
Se importan los paquetes y librerias a utilizar en este script
"""
import cv2 
import Funciones as fun
import numpy as np

from matplotlib import pyplot as plt 

def _binarize_frame(frame,frame_in_component,height,width):
	"""
	Esta función binariza una imagen teniendo en cuenta dicha imagen
	en un componente específico del color.
	Input:
		- frame: Imagen a binarizar.
		- frame_in_component: Imagen en su componente a identificar.
		- height: Ancho de la imgen.
		- width: Alto de la imagen.
	Output:
		- bin_frame: Imagen binarizada.
	"""
	threshold = 160
	white_threshold = np.where(frame_in_component[:,0:width]>threshold)
	black_threshold = np.where(frame_in_component[:,0:width]<=threshold)

	bin_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	bin_frame[white_threshold] = 255
	bin_frame[black_threshold] = 0

	return bin_frame

def _compute_frame_area(frame):
	"""
	Esta función permite encontrar la mayor área de un objeto en  una
	imagén. Con esta función se puede identificar el objeto que esta-
	mos usando para pintar, ubicandolo por su área.
	Input:
		- frame: Imagen donde se quiere encontrar el área.
	Output:
		- area: Área máxima del objeto.
		- fit_idx: Indices en los cuales se encontró el área mayor.
	"""
	ret, labels = cv2.connectedComponents(frame)
	area = 0
	fit_idx = 0

	for i in range(1,ret): 
	    img_aux = frame*0
	    idx = np.where(labels==i)
	    img_aux[idx] = 1
	    pixels_sum = np.sum(img_aux)
	    if pixels_sum >= area:
	        area = pixels_sum
	        fit_idx = idx

	return area,fit_idx	           

def _find_object_coordinates(frame,fit_idx):
	"""
	Esta función permite encontrar cuales son las coordenadas del objeto
	con el cual estamos pintando la pantalla.
	Input:
		- frame: Imagen donde se quiere encontrar el área.
		- fit_idx: Indices en los cuales se encontró el área mayor.
	Output:
		- (y_max, x_min): Coordenada del primero punto.
		- (y_min, x_max): Coordenada del segundo punto.
	"""
	img_aux = frame * 0
	img_aux[fit_idx] = 255

	x,y=np.where(img_aux>0)
	x_min=np.min(x)
	y_min=np.min(y)
	x_max=np.max(x)
	y_max=np.max(y)

	return (y_max, x_min),(y_min, x_max)

def identify_object(frame):
	"""
	Esta función nos permite encontrar en que punto de la pantalla se encuentra
	el objeto con el que estamos pintanto el lienzo. Para realizar este proceso
	primero se extrae el componente R_LAB de la imagén (Este es el que mejor se
	adapta al objeto en cuestion), luego se binariza la imagen y posteriormente
	se encuentra el área y las coordendas del área mayor, finalmente se retorna
	las coordenas de este objeto.
	Input:
		- frame: Imagen donde se quiere encontrar el área.
	Output:
		- point_one: Coordenada del primero punto.
		- point_two: Coordenada del segundo punto.
		- half_point: Coordena del punto medio.
	"""

	point_one = tuple()
	point_two = tuple()
	half_point = tuple()

	height,width,chanels = frame.shape 

	_ , _ , _ , _ , _ , red_LAB =fun.componentes(frame)

	bin_frame = _binarize_frame(frame,red_LAB,height,width)
	area,fit_idx = _compute_frame_area(bin_frame)

	if area >= 1090:
		point_one, point_two = _find_object_coordinates(bin_frame,fit_idx)
		x_half = int((point_one[0]+point_two[0])/2)
		y_half = int((point_one[1]+point_two[1])/2)
		half_point = (x_half,y_half)

	return point_one, point_two, half_point