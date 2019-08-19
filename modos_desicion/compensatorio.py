# -*- coding: utf-8 -*-
##Raster=group
##A=raster
##wA=number 0.5
##B=raster
##wB=number 0.5
##C=optional raster
##wC=optional number
##D=optional raster
##wD=optional number
##E=optional raster
##wE=optional number
##F=optional raster
##wF= optional number
##G=optional raster
##wG=optional number

##final=boolean False
##normalizar_final = Boolean False
##salida=output raster
from qgis.core import QgsRasterLayer, QgsRasterBandStats
from raster_apc import *


pesos = []
lista_inputs = []    
if compensatorio==1:

    layer_A = processing.getObject(A)
    if layer_A.isValid() is True:
        path_A= layer_A.dataProvider().dataSourceUri()
        lista_inputs.append(path_A)
        pesos.append(wA)
    layer_B = processing.getObject(B)
    if layer_B.isValid() is True:
        path_B= layer_B.dataProvider().dataSourceUri()
        lista_inputs.append(path_B)
        pesos.append(wB)
    if C != None:
        layer_C = processing.getObject(C)
        path_C= layer_C.dataProvider().dataSourceUri()
        lista_inputs.append(path_C)
        pesos.append(wC)
    if D != None:      
        layer_D = processing.getObject(D)
        path_D= layer_D.dataProvider().dataSourceUri()
        lista_inputs.append(path_D)
        pesos.append(wD)
    if E != None:
        layer_E = processing.getObject(E)
        path_E= layer_E.dataProvider().dataSourceUri()
        lista_inputs.append(path_E)
        pesos.append(wE)
    if F != None:    
        layer_F = processing.getObject(F)
        path_F= layer_F.dataProvider().dataSourceUri()
        lista_inputs.append(path_F)
        pesos.append(wF)
    if G != None:
        layer_G = processing.getObject(G)
        path_G= layer_G.dataProvider().dataSourceUri()
        lista_inputs.append(path_G)
        pesos.append(wF)
    
    n_variables = len(pesos)
    if final==0:
        ecuacion  = ecuacion_comp(n_variables,pesos)
        crea_capa(ecuacion,lista_inputs,salida)
    else:
        mapa_final_compensatorio(n_variables,pesos,lista_inputs,salida)
        if normalizar_final==1:
            salida_normalizada = salida.split(".")[0]+"_norm."+salida.split(".")[1]
            norm_inversa(salida,salida_normalizada)
        
    
    
    
    
   