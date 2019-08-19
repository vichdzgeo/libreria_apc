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
##normalizar=Boolean False
##salida=output raster

import numpy, gdal_calc
import os, sys, subprocess, processing 
from qgis.core import QgsRasterLayer, QgsRasterBandStats
from PyQt4.QtCore import QFileInfo
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.analysis import *
import string 


#____________funciones_______________________________
def raster_min_max(path_raster):
    '''
    esta función regresa el valor mínimo y máximo de un
    raster

    Ejemplo de uso: 
    min, max = raster_min_max('/../raster.tif')
    '''
    rlayer = QgsRasterLayer(path_raster,"raster")

    extent = rlayer.extent()
    provider = rlayer.dataProvider()

    stats = provider.bandStatistics(1,
                                    QgsRasterBandStats.All,
                                    extent,
                                    0)

    min = stats.minimumValue
    max = stats.maximumValue
    return min,max

def norm_estandar(path_raster, path_raster_n):
    min,max = raster_min_max(path_raster)

    clp_norm ='(A - ' + str(min) + ') / (' + str(max) + ' - ' +str(min) +')' 
    gdal_calc.Calc(calc=clp_norm, 
            A=path_raster,
            outfile=path_raster_n)



def norm_inversa(path_raster, path_raster_n):
    min,max = raster_min_max(path_raster)
    norm ='(1 - A' ') / (' + '1  - ' +str(min) +')' 
    gdal_calc.Calc(calc=norm, 
            A=path_raster,
            outfile=path_raster_n)


def ecuacion_clp(n_variables,pesos):
    
    abc = list(string.ascii_uppercase)
    ecuacion = ''
    for a,b in zip(range(n_variables),pesos):
        
        if a < n_variables-1:
            ecuacion+= (str(b)+str(' * ')+str(abc[a])+' + ' )
        else:
            ecuacion+= (str(b)+str(' * ')+str(abc[a]))
    return ecuacion 


def ecuacion_comp(n_variables,pesos):
    
    abc = list(string.ascii_uppercase)
    ecuacion = ''
    for a,b in zip(range(n_variables),pesos):
        
        if a < n_variables-1:
            ecuacion+= (str(b)+str(' * ')+"(1 - " +str(abc[a])+")"+' + ' )
        else:
            ecuacion+= (str(b)+str(' * ')+"(1 - " +str(abc[a])+")")
    return ecuacion

def ecuacion_p_comp(n_variables,pesos):
    
    abc = list(string.ascii_uppercase)
    ecuacion = 'numpy.power('
    for a,b in zip(range(n_variables),pesos):
        
        if a < n_variables-1:
            ecuacion+= ('numpy.power('+str(b)+",2)"+str(' * ')+"(1 - " +"numpy.power("+str(abc[a])+",2)"+")"+' + ' )
        else:
            ecuacion+= ('numpy.power('+str(b)+",2)"+str(' * ')+"(1 - " +"numpy.power("+str(abc[a])+",2)"+")")
    ecuacion+= ',1/2)'
    return ecuacion 

def ecuacion_no_comp(n_variables,pesos):
    
    abc = list(string.ascii_uppercase)
    ecuacion = 'numpy.power('
    for a,b in zip(range(n_variables),pesos):
        
        if a < n_variables-1:
            ecuacion+= ('numpy.power('+str(b)+",10)"+str(' * ')+"(1 - " +"numpy.power("+str(abc[a])+",10)"+")"+' + ' )
        else:
            ecuacion+= ('numpy.power('+str(b)+",10)"+str(' * ')+"(1 - " +"numpy.power("+str(abc[a])+",10)"+")")
    ecuacion+= ', 1/10)'
    return ecuacion 

def crea_capa(ecuacion,rasters_input,salida): 
    path_A=''
    path_B=''
    path_C=''
    path_D=''
    path_E=''
    path_F=''
    path_G=''
    path_H=''
    total_raster = len(rasters_input)
    
    for a,b in zip(range(total_raster), rasters_input):
        if a == 0:
            path_A=b
        elif a == 1:
            path_B=b
        elif a == 2:
            path_C=b
        elif a == 3:
            path_D=b
        elif a == 4:
            path_E=b
        elif a == 5:
            path_F=b
        elif a == 6:
            path_G=b
        elif a == 7:
            path_H=b


    if total_raster == 1:
            gdal_calc.Calc(calc=ecuacion, 
                            A=path_A, 
                            outfile=salida,
                            NoDataValue=3.40282e+38)
                            
    if total_raster == 2:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        outfile=salida,
                        NoDataValue=3.40282e+38)

    if total_raster == 3:
            gdal_calc.Calc(calc=ecuacion, 
                            A=path_A, 
                            B=path_B,
                            C=path_C, 
                            outfile=salida,
                            NoDataValue=3.40282e+38)
                            
    if total_raster == 4:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        outfile=salida,
                        NoDataValue=3.40282e+38)

    if total_raster == 5:
            gdal_calc.Calc(calc=ecuacion, 
                            A=path_A, 
                            B=path_B,
                            C=path_C, 
                            D=path_D,
                            E=path_E, 
                            outfile=salida,
                            NoDataValue=3.40282e+38)
                            
    if total_raster == 6:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        outfile=salida,
                        NoDataValue=3.40282e+38)

    if total_raster == 7:
            gdal_calc.Calc(calc=ecuacion, 
                            A=path_A, 
                            B=path_B,
                            C=path_C, 
                            D=path_D,
                            E=path_E, 
                            F=path_F,
                            G=path_G, 
                            outfile=salida,
                            NoDataValue=3.40282e+38)
                            
    if total_raster == 8:
        gdal_calc.Calc(calc=ecuacion, 
                        A=path_A, 
                        B=path_B,
                        C=path_C, 
                        D=path_D,
                        E=path_E, 
                        F=path_F,
                        G=path_G, 
                        H=path_H,
                        outfile=salida,
                        NoDataValue=3.40282e+38)



#_____________________PROGRAMA_______________________

pesos = []
lista_inputs = []    


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
ecuacion  = ecuacion_clp(n_variables,pesos)
crea_capa(ecuacion,lista_inputs,salida)


if normalizar==1:
    salida_normalizada = salida.split(".")[0]+"_norm."+salida.split(".")[1]
    norm_estandar(salida,salida_normalizada)

    
   