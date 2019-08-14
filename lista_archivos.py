# -*- coding: utf-8 -*-
import os 
def lista_archivos(path_carpeta,extension):
    '''
    Esta funcion regresa una lista que contiene los
    archivos contenidos en un directorio segun el tipo de extensión declarado.

    Parametros:
    :param path_carpeta: Ruta de la carpeta que contiene los datos
    :type path_carpeta: String

    :param extension: tipo de extensión, agregar un . al inicio ej '.tif'
    :type extension: String

    ::

        ejemplo:
        lista_shapes=apc.lista_archivos(path_sig,'.shp')

    '''
    for root, dirs, files in os.walk(path_carpeta):
        lista = []
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == extension:
                lista.append(extension)
    return lista

path = "C:/Dropbox (LANCIS)/SIG/desarrollo/sig_papiit/entregables/"

lista = lista_archivos(path,'.tiff')

print (lista)