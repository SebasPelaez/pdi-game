
# coding: utf-8

# In[ ]:

import pyhdust.images as phim                 # Comando utilizado para instalar libreria pyhdust (pip install pyhdust)
from skimage import color
from cv2 import *     
import numpy as np

def chori(a):
    a.astype('float64')                       # Se convierte la imagen entrante en doble para poder operarla
    cn=a/np.max(a)                            # Se normalizan las intensidades de la imagen
    cn.astype('uint8')                        # Se vuelve a convertir la imagen a tipo sin signo de 8 bits
    b=cn[:,:,0]                               # Se obtiene componente azul de la imagen
    g=cn[:,:,1]                               # Se obtiene componente verde de la imagen
    r=cn[:,:,2]                               # Se obtiene componente roja de la imagen
    tot=np.hstack((r,g,b))                    # Se apilan horizontalmente las componentes RGB de la imagen usando funcion de numpy
    
    return tot


def componentes(c):
    a1=chori(c)                               # Se lleva imagen a la funcion chori para descomponerla en RGB
    a2 =cvtColor(c, COLOR_BGR2HSV)            # Se cambia de espacio de color de RGB para HSV usando funcion de cv2
    a2=chori(a2)                              # Se lleva imagen en HSV a la funcion chori para descomponer en RGB
    a3=phim.rgb2cmyk(np.asarray(c))           # Se cambia de espacio de color de RGB a CMYK usando funcion de cv2
    a3=chori(a3)                              # Se lleva imagen en CMYK a la funcion chori para descomponer en RGB
    a4 =cvtColor(c, COLOR_BGR2LAB)            # Se cambia de espacio de color de RGB a LAB usando funcion de cv2
    a4_1=chori(a4)                         # Se lleva imagen en LAB a la funcion chori para descomponer en RGB
    a5=color.lab2lch(a4)                      # Se cambia de espacio de color de LAB a LCH usando funcion de cv2
    a5=chori(a5)                              # Se lleva imagen en LCH a la funcion chori para descomponer en RGB
    k=a4[:,:,2]                               # Se elige la tercera imagen que es la componente roja del espacio LAB 
    a6=np.hstack((k,k,k))                     # Se apila la imagen elegida horizontalmente
    
    return a1,a2,a3,a4_1,a5,a6

