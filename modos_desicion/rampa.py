# -*- coding: utf-8 -*-
import numpy, gdal_calc
import os, sys, subprocess, processing 
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.analysis import *
import string 

def raster_min_max(path_raster):
    '''
    esta funciÃ³n regresa el valor mÃ­nimo y mÃ¡ximo de un
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

def weber_fechner(fp,categorias,path_raster):
    dicc_e = {}
    min,max = raster_min_max(path_raster)
    pm = max - min 
    cats = numpy.power(fp , categorias)
    e0 = pm/cats
    for i in range(1 , categorias + 1):
        dicc_e['e'+str(i)]= round((max - (numpy.power(fp,i) * e0)),2)

    dicc_cortes ={}
    for i in range(1 , categorias + 1):
        dicc_cortes['corte'+str(i)]= round(1 - dicc_e['e'+str(i)],2)

    print (dicc_cortes)


layer = iface.activeLayer()
path_rlayer =  layer.dataProvider().dataSourceUri()
lista_val = weber_fechner(2 ,4,path_rlayer)
colDic={'ma':'#730000', 'a':'#ff5500','M':'#ffff00','b':'#4ce600','mb':'#267300'}
  
lst = [ QgsColorRampShader.ColorRampItem(lista_val[0], QColor(colDic['ma'])), \
    QgsColorRampShader.ColorRampItem(lista_val[1], QColor(colDic['a'])), \
    QgsColorRampShader.ColorRampItem(lista_val[2], QColor(colDic['M'])), \
    QgsColorRampShader.ColorRampItem(lista_val[3], QColor(colDic['b'])), \
    QgsColorRampShader.ColorRampItem(lista_val[4], QColor(colDic['mb']))]
 
myRasterShader = QgsRasterShader()
myColorRamp = QgsColorRampShader()
 
myColorRamp.setColorRampItemList(lst)
myColorRamp.setColorRampType(QgsColorRampShader.INTERPOLATED)
myRasterShader.setRasterShaderFunction(myColorRamp)
 
myPseudoRenderer = QgsSingleBandPseudoColorRenderer(\
    layer.dataProvider(), layer.type(),  myRasterShader)
 
layer.setRenderer(myPseudoRenderer)
 
layer.triggerRepaint()

print lista_val
