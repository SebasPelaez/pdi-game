"""
Se importan los paquetes y librerias a utilizar en este script
"""
import cv2
import numpy as np
import os

import ObjectUtils

def _get_border_image(paint_window, image_name):
	"""
	Esta función extrae por medio del método Canny los bordes de una imágen. Para 
	realizar este proceso primero se guarda la imagen original, posteriormente se
	carga y se transforma a escala de grises, luego se aplica el método Canny, se
	extraen los bordes y se guarda la image.
	Input:
		- paint_window: Imagen a la cuál se le extraen los bordes.
		- image_name: Nombre con el cuál se guardará la imagen.
	"""
	folder_images_path = os.path.join('Imagenes','Generadas')

	if not os.path.exists(folder_images_path):
	    os.makedirs(folder_images_path)

	image_path = os.path.join(folder_images_path,'{}.jpg'.format(image_name))
	image_border_path = os.path.join(folder_images_path,'{}_border.jpg'.format(image_name))
	
	cv2.imwrite(image_path,paint_window)
	image = cv2.imread(image_path,1)
	
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	border = cv2.Canny(gray,100,200)
	
	cv2.imwrite(image_border_path,border)
	
def _compute_score():
	"""
	Por medio de esta función se calcula el puntaje que el jugador obtuvo luego de
	que el tiempo de juego se le acabara. Para calcular este puntaje se hace   uso
	de dos métricas: IOU (Intersection Over Union) y Border Error (Error del borde).
	Para el cálculo de estas métricas se debe extraer el valor del área de la unión
	e intersección de dos imágenes, el número de pixeles en el borde de la   imagen
	original y el número de veces que la imagen pintada tocó estos bordes.
	IOU = (Area de intersección/Area de Union)
	BE = (#Pixeles del borde tocados/#Total de pixeles en la imagen original)
	Finalmente, el puntaje se calcula como: score = | IOU - BE | 
	"""
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
	"""
	Esta función permite identificar cuantos pixeles hay en una imagen binarizada.
	Para ejecutar este proceso, primero se obtiene una imagen, posteriormente  se
	llama al método de binarización del paquete OpenCV y se realiza una suma   de
	aquellos valores que esten en 1.
	Input:
		- image: Imagen que se desea contar.
	Output:
		- num_pixels: Cantidad de pixeles de la imagen binarizada.
	"""
	_ , image_binarized = cv2.threshold(image, 170, 255, cv2.THRESH_BINARY)
	mask = image_binarized == 255
	num_pixels = np.sum(mask)

	return num_pixels

def _get_overlap(image_A,image_B):
	"""
	Esta función encuentra el valor del área de intersección entre 2 imágenes.
	Input:
		- image_A: Imagen 1
		- image_B: Imagen 2
	Output:
		- overlap: Área de intersección entre las dos imágenes.
	"""
	image_intersection = cv2.bitwise_and(image_A,image_B)
	overlap = _count_pixels_in_binarized_images(image_intersection)

	return overlap

def _get_union(image_A,image_B):
	"""
	Esta función encuentra el valor del área de la unión entre 2 imágenes.
	Input:
		- image_A: Imagen 1
		- image_B: Imagen 2
	Output:
		- unión: Área de unión entre las dos imágenes.
	"""
	image_intersection = cv2.bitwise_or(image_A,image_B)
	union = _count_pixels_in_binarized_images(image_intersection)

	return union


def _get_draw_image():
	"""
	Esta función nos permite seleccionar aleatoriamente 1 de las posibles imá-
	genes para pintar. Para esto, se para en la carpeta de imágenes   disponi-
	bles, las cuenta y genera un número al azar, luego selecciona esta imágen
	y la retorna.
	Output:
		- random_imagen: Imagen tomada aleatoriamente.
	"""
	images = os.listdir(os.path.join('Imagenes','Dibujos'))
	random = np.random.randint(0,len(images))

	random_image_path = os.path.join('Imagenes','Dibujos',images[random])
	random_image = cv2.imread(random_image_path)

	return random_image

def delimit_screen(frame):
	"""
	Esta función permirte delimitar la pantalla en dos secciones, en la primera
	de ellas se encuentra el menú con las opciones para pintar, en la   segunda
	se encuentra el lienzo sobre el cual se pinta.
	Input:
		- frame: Pantalla que se desea delimitar.
	Output:
		- frame: Pantalla con los bordes delimitados.
	"""
	start_point = (menu_limit_area,0)
	end_point = (menu_limit_area,500)
	color = (0,0,0)
	thickness = 4
	frame = cv2.line(frame, start_point, end_point, color, thickness)

	return frame

def _paint_menu(window,colors):
	"""
	Esta función es la encargada de pintar el menú de configuraciones en pantalla.
	Dicho menú tiene varias caracteristicas, primero una lnea vertica en la cual se
	hace la referencia a la división entre menú y lienzo para pintar, segundo tiene
	4 rectangulos que simbolizan los 4 colores que la persona puede seleccionar,ter-
	cero tiene 3 opciones de tamaño de brocha, una pequeña, mediana y grande.
	Input:
		- window: Ventana en la cual se quiere pintar el menú.
		- colors: Vector con los colores disponibles para el usuario seleccionar.
	Output:
		- window: Ventana con el menú pintado.
	"""
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
	"""
	Esta función es la encargada de pintar en pantalla el tiempo que le resta
	al jugador antes de que terminer la partida.
	Input:
		- window: Pantalla sobre la cual se quiere pintar el contador.
		- time_elapsed: Tiempo restante.
	Output:
		- window: Pantalla con el tiempo pintado.
	"""
	window = cv2.rectangle(window, (570,6), (620,26), (255,255,255), -1)
	cv2.putText(window, str(time_elapsed), (575, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

	return window

def _paint_results(window,score):
	"""
	Esta función es la encargada de pintar en pantalla la información 
	final de la partida jugada, cual fue el puntaje y el resultado de
	sus errores.
	Input:
		- window: Pantalla sobre la cual se quiere mostrar los resultados.
		- score: Puntaje obtenido.
	"""
	cv2.putText(window, "FELICIDADES", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, "TU PUNTAJE", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, "ES", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, str(np.round(score,4)*100), (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

def _paint_rules(window,colors,idx,brushes,brush_idx):
	"""
	Esta función es la encargada de pintar sobre la pantalla las indicaciones
	con las cuales se puede jugar la partida. Estas indicaciones estan desglo-
	sadas en textos cortos que muestran en que secciones se debe parar el  ju-
	gador para cambiar los colores y los tamaños de las brochas.
	Input:
		- window: Ventana sobre la cual se van a pintar las reglas del juego.
		- colors: Vector con los colores disponibles para el usuario seleccionar.
		- idx: Indice que especifica cual es el color que actualmente se esta usando.
		- brushes: Vector con los tamaños disponibles para el usuario seleccionar.
		- brush_idx: Indice que especifica cual es la brocha que actualmente se esta usando.
	Output:
		- window: Venta con las reglas del juego especificadas.
	"""
	cv2.putText(window, "Parate sobre el", (19, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, "color o la brocha", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)
	cv2.putText(window, "que desees", (35, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1, cv2.LINE_AA)

	cv2.putText(window, "Color Seleccionado", (160, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
	window = cv2.rectangle(window, (312,6), (350,26), colors[idx], -1)
	cv2.putText(window, "Brocha Seleccionada", (360, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
	window = cv2.rectangle(window, (525,6), (550,26), (255,255,255), -1)
	cv2.putText(window, str(brushes[brush_idx]), (530, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

	return window

def play_game(menu_limit_area,paint_window_shape,colors,brushes,time_to_win):
	"""
	Esta función es la encargada de inicializar y renderizar el juego. Este proceso
	iniciar asignado el valor de las brocha y el color con el cual se    empezará a
	pintar, posteriormente se inicializa el lienzo, encontrando una imagen  aleato-
	ria, luego pintando el menú y por ultimo las reglas. Siguiendo a esto se guarda
	el estado de la imagen sin pintar que será usado luego para calcular las métri-
	cas, además de esto se crea una ventana fantasma que guarda todo lo que el  ju-
	gador pinte y finalmente se inicializa la captura de video.

	Luego de inicializar todos los componentes, el juego entra en un ciclo que cons-
	tantemente esta capturando los movimientos del jugador y pintandolos sobre   dos
	lienzos (el oculto y el que se muestra en pantalla). Este ciclo tiene fin  cuan-
	do ocurren una de tres cosas:
	1) El usuario cierra abruptamente la pantalla.
	2) El usuario presiona la tecla q.
	3) Se le acaba el tiempo de juego.
	
	Después de que el ciclo termina se guarda el estado del lienzo oculto, esto con
	el fin de que se deje constancia de que fue lo que el jugador pinto.   Teniendo
	en cuenta esta imagén y la que se guardo al comienzo se calculan el puntaje fi-
	nal obtenido y posteriormente se muestra en pantalla con los resultados  combi-
	nados de su pintura y la imagen a pintar. Luego de analizar estos resultados el
	juego se da por terminado.

	Input:
		- menu_limit_area: Tamaño de la pantalla con la cual se dividirá el menú y 
		el lienzo.
		- paint_window_shape: Tamaño de la pantalla de pintura, incluye el menú  y
		el lienzo.
		- colors: Vector con los colores disponibles para el usuario seleccionar.
		- brushes: Vector con los tamaños disponibles para el usuario seleccionar.
		- time_to_win: Tiempo máximo de juego.
	"""

	color_idx = 0
	brush_idx = 0

	paintWindow = _get_draw_image()
	paintWindow = _paint_menu(paintWindow,colors)
	paintWindow = _paint_rules(paintWindow,colors,color_idx,brushes,brush_idx)
	_get_border_image(paintWindow, 'unpainted_image')

	hidden_layer = np.zeros(paint_window_shape)
	hidden_layer = cv2.resize(hidden_layer,paint_window_shape)

	cap = cv2.VideoCapture(0)

	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read()
	   
	    object_point_one, object_point_two, object_half_point = ObjectUtils.identify_object(frame)

	    if object_point_one and object_point_two:

	    	if object_point_one[0] >= menu_limit_area and object_point_two[0] >= menu_limit_area:

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

	score = _compute_score() * 100
	results_window = _get_draw_image()
	_paint_results(results_window,score)
	cv2.imshow('RESULTADOS',results_window)
	
	cv2.waitKey()
	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	"""
	Función MAIN, ejecuta el juego
	"""
	menu_limit_area = 150
	paint_window_shape = (620,426)
	colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
	brushes = [5,10,15]
	time_to_win = 500

	play_game(menu_limit_area,paint_window_shape,colors,brushes,time_to_win)