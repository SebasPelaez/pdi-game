"""
Se importan los paquetes y librerias a utilizar en este script
"""
import numpy as np
import pyhdust.images as phim
from skimage import color
from cv2 import *

def chori(a):
    """
    Esta función convierte la imagen entrante en doble para poder operarla.
    Para ello se normalizan las intensidades de la imagen, se vuelve a con-
    vertir la imagen a tipo sin signo de 8 bits, posteriormente se  obtiene
    componente azul, verde y rojo de la imagen para finalmente apilan hori-
    zontalmente las componentes RGB de la imagen usando funcion de numpy.

    Input:
        - a: Imagen a transformar.
    Output:
        - tot: Imagen convertida.
    """
    a.astype('float64')
    cn=a/np.max(a)
    cn.astype('uint8')
    b=cn[:,:,0]
    g=cn[:,:,1]
    r=cn[:,:,2]
    tot=np.hstack((r,g,b))
    
    return tot

def componentes(c):
    """
    Esta función obteniene todos los componentes, espectros y represen-
    taciones de color de la image. Los formatos en los cuales se va   a
    transformar la imagen son: RGB, HSV, CMYK, B_LAB, LCH, R_LAB 
    
    Input:
        - c: Imagen a la cual se le quieren sacar los componentes.
    Output:
        - (a1,a2,a3,a4,a5,a6): Posibles representaciones de la imagen.
    """
    a1=chori(c)
    a2 =cvtColor(c, COLOR_BGR2HSV)
    a2=chori(a2)
    a3=phim.rgb2cmyk(np.asarray(c))
    a3=chori(a3)
    a4 =cvtColor(c, COLOR_BGR2LAB)
    a4_1=chori(a4)
    a5=color.lab2lch(a4)
    a5=chori(a5)
    k=a4[:,:,2]
    a6=np.hstack((k,k,k))
    
    return a1,a2,a3,a4_1,a5,a6

