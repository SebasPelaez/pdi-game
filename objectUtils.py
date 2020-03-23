import cv2 

import funciones as fun
import numpy as np

from matplotlib import pyplot as plt 

def _binarize_frame(frame,frame_in_component,height,width):

	threshold = 160
	white_threshold = np.where(frame_in_component[:,0:width]>threshold)
	black_threshold = np.where(frame_in_component[:,0:width]<=threshold)

	bin_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	bin_frame[white_threshold] = 255
	bin_frame[black_threshold] = 0

	return bin_frame

def _compute_frame_area(frame):

	ret, labels = cv2.connectedComponents(frame)
	area = 0
	fit_idx = 0

	for i in range(1,ret): 
	    img_aux = frame*0                               # Se crea una matriz en cero con las dimensiones de la imagen original
	    idx = np.where(labels==i)                     # Se recorren las etiquetas de los objetos en la imagen
	    img_aux[idx] = 1                                    # A cada pixel se les lleva el valor de 1
	    pixels_sum = np.sum(img_aux)
	    if pixels_sum >= area:                            # Aproximar area de la placa en pixeles usando libreria IV usada en clase 1
	        area = pixels_sum                              # Se lleva el lugar y el area de la placa a dos vbles nueva
	        fit_idx = idx

	return area,fit_idx	           

def _find_object_coordinates(frame,fit_idx):

	img_aux = frame * 0
	img_aux[fit_idx] = 255

	x,y=np.where(img_aux>0)                           # Se extraen las secciones de la placa donde la intensidad sea mayor que cero
	                                                  # donde este el color blanco
	x_min=np.min(x)                                   # Se selecciona el valor minimo del vector en el eje x donde haya blanco
	y_min=np.min(y)                                   # Se selecciona el valor minimo del vector en el eje y donde haya blanco
	x_max=np.max(x)                                   # Se selecciona el valor maximo del vector en el eje x donde haya blanco
	y_max=np.max(y)                                   # Se selecciona el valor maximo del vector en el eje y donde haya blanco

	return (y_max, x_min),(y_min, x_max)


def identify_object(frame):

	point_one = tuple()
	point_two = tuple()

	height,width,chanels = frame.shape 

	_ , _ , _ , _ , _ , red_LAB =fun.componentes(frame)

	bin_frame = _binarize_frame(frame,red_LAB,height,width)
	area,fit_idx = _compute_frame_area(bin_frame)

	if area >= 1090:
		point_one, point_two = _find_object_coordinates(bin_frame,fit_idx)

	return point_one, point_two