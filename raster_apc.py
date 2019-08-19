# -*- coding: utf-8 -*-
import numpy, gdal_calc
import os, sys, subprocess, processing 
from qgis.core import QgsRasterLayer, QgsRasterBandStats
from PyQt4.QtCore import QFileInfo
from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from qgis.analysis import *
import string 

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

def mapa_final_clp(n_variables,pesos,raster_inputs,raster_salida):
    
    
    ecuacion = ''
    for a,b in zip(range(n_variables),pesos):
        
        if a < n_variables-1:
            ecuacion+= (str(b)+str(' * ')+"'layer"+str(a+1)+"@1'"+' + ' )
        else:
            ecuacion+= (str(b)+str(' * ')+"'layer"+str(a+1)+"@1'")
    
    entries = []

    #abre el archivo raster1
    fileInfo = QFileInfo(raster_inputs[0])
    path = fileInfo.filePath()
    baseName = fileInfo.baseName()
    layer1 = QgsRasterLayer(path, baseName)
    var1 = QgsRasterCalculatorEntry()
    var1.ref = 'layer1@1'
    var1.raster = layer1
    var1.bandNumber = 1
    entries.append( var1 )
    
    if n_variables ==2:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
    elif n_variables ==3:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
    
    elif n_variables ==4:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
        
        fileInfo = QFileInfo(raster_inputs[3])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer4 = QgsRasterLayer(path, baseName)
        var4 = QgsRasterCalculatorEntry()
        var4.ref = 'layer4@1'
        var4.raster = layer4
        var4.bandNumber = 1
        entries.append( var4 )
    
    elif n_variables ==5:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
        
        fileInfo = QFileInfo(raster_inputs[3])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer4 = QgsRasterLayer(path, baseName)
        var4 = QgsRasterCalculatorEntry()
        var4.ref = 'layer4@1'
        var4.raster = layer4
        var4.bandNumber = 1
        entries.append( var4 )
        
        fileInfo = QFileInfo(raster_inputs[4])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer5 = QgsRasterLayer(path, baseName)
        var5 = QgsRasterCalculatorEntry()
        var5.ref = 'layer5@1'
        var5.raster = layer5
        var5.bandNumber = 1
        entries.append( var5 )
    

    calc = QgsRasterCalculator(ecuacion, 
                               raster_salida, 
                                'GTiff', 
                                layer1.extent(), 
                                layer1.width(), 
                                layer1.height(),
                                entries)
                                
    calc.processCalculation()


def mapa_final_compensatorio(n_variables,pesos,raster_inputs,raster_salida):
    
    
    ecuacion = ''
    for a,b in zip(range(n_variables),pesos):
        
        if a < n_variables-1:
            ecuacion+= (str(b)+str(' * ')+"'(1 - layer"+str(a+1)+"@1)'"+' + ' )
        else:
            ecuacion+= (str(b)+str(' * ')+"'(1 - layer"+str(a+1)+"@1)'")
    
    entries = []

    #abre el archivo raster1
    fileInfo = QFileInfo(raster_inputs[0])
    path = fileInfo.filePath()
    baseName = fileInfo.baseName()
    layer1 = QgsRasterLayer(path, baseName)
    var1 = QgsRasterCalculatorEntry()
    var1.ref = 'layer1@1'
    var1.raster = layer1
    var1.bandNumber = 1
    entries.append( var1 )
    
    if n_variables ==2:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
    elif n_variables ==3:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
    
    elif n_variables ==4:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
        
        fileInfo = QFileInfo(raster_inputs[3])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer4 = QgsRasterLayer(path, baseName)
        var4 = QgsRasterCalculatorEntry()
        var4.ref = 'layer4@1'
        var4.raster = layer4
        var4.bandNumber = 1
        entries.append( var4 )
    
    elif n_variables ==5:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
        
        fileInfo = QFileInfo(raster_inputs[3])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer4 = QgsRasterLayer(path, baseName)
        var4 = QgsRasterCalculatorEntry()
        var4.ref = 'layer4@1'
        var4.raster = layer4
        var4.bandNumber = 1
        entries.append( var4 )
        
        fileInfo = QFileInfo(raster_inputs[4])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer5 = QgsRasterLayer(path, baseName)
        var5 = QgsRasterCalculatorEntry()
        var5.ref = 'layer5@1'
        var5.raster = layer5
        var5.bandNumber = 1
        entries.append( var5 )
    

    calc = QgsRasterCalculator(ecuacion, 
                               raster_salida, 
                                'GTiff', 
                                layer1.extent(), 
                                layer1.width(), 
                                layer1.height(),
                                entries)
                                
    calc.processCalculation()

def mapa_final_p_compensatorio(n_variables,pesos,raster_inputs,raster_salida):


    ecuacion = '('
    for a,b in zip(range(n_variables),pesos):
        
        if a < n_variables-1:
            ecuacion+= ("("+str(b)+"^2) * "+"'(1 - (layer"+str(a+1)+"@1 ^2))'"+' + ' )
        else:
            ecuacion+= ("("+str(b)+"^2) * "+"'(1 - (layer"+str(a+1)+"@1 ^2))'")
    ecuacion+=') ^ 1/2'
    entries = []

    #abre el archivo raster1
    fileInfo = QFileInfo(raster_inputs[0])
    path = fileInfo.filePath()
    baseName = fileInfo.baseName()
    layer1 = QgsRasterLayer(path, baseName)
    var1 = QgsRasterCalculatorEntry()
    var1.ref = 'layer1@1'
    var1.raster = layer1
    var1.bandNumber = 1
    entries.append( var1 )
    
    if n_variables ==2:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
    elif n_variables ==3:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
    
    elif n_variables ==4:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
        
        fileInfo = QFileInfo(raster_inputs[3])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer4 = QgsRasterLayer(path, baseName)
        var4 = QgsRasterCalculatorEntry()
        var4.ref = 'layer4@1'
        var4.raster = layer4
        var4.bandNumber = 1
        entries.append( var4 )
    
    elif n_variables ==5:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
        
        fileInfo = QFileInfo(raster_inputs[3])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer4 = QgsRasterLayer(path, baseName)
        var4 = QgsRasterCalculatorEntry()
        var4.ref = 'layer4@1'
        var4.raster = layer4
        var4.bandNumber = 1
        entries.append( var4 )
        
        fileInfo = QFileInfo(raster_inputs[4])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer5 = QgsRasterLayer(path, baseName)
        var5 = QgsRasterCalculatorEntry()
        var5.ref = 'layer5@1'
        var5.raster = layer5
        var5.bandNumber = 1
        entries.append( var5 )
    

    calc = QgsRasterCalculator(ecuacion, 
                                raster_salida, 
                                'GTiff', 
                                layer1.extent(), 
                                layer1.width(), 
                                layer1.height(),
                                entries)
                                
    calc.processCalculation()


def mapa_final_no_compensatorio(n_variables,pesos,raster_inputs,raster_salida):


    ecuacion = '('
    for a,b in zip(range(n_variables),pesos):
        
        if a < n_variables-1:
            ecuacion+= ("("+str(b)+"^10) * "+"'(1 - (layer"+str(a+1)+"@1 ^10))'"+' + ' )
        else:
            ecuacion+= ("("+str(b)+"^10) * "+"'(1 - (layer"+str(a+1)+"@1 ^10))'")
    ecuacion+='  ) ^ 1/10'
    entries = []

    #abre el archivo raster1
    fileInfo = QFileInfo(raster_inputs[0])
    path = fileInfo.filePath()
    baseName = fileInfo.baseName()
    layer1 = QgsRasterLayer(path, baseName)
    var1 = QgsRasterCalculatorEntry()
    var1.ref = 'layer1@1'
    var1.raster = layer1
    var1.bandNumber = 1
    entries.append( var1 )
    
    if n_variables ==2:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
    elif n_variables ==3:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
    
    elif n_variables ==4:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
        
        fileInfo = QFileInfo(raster_inputs[3])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer4 = QgsRasterLayer(path, baseName)
        var4 = QgsRasterCalculatorEntry()
        var4.ref = 'layer4@1'
        var4.raster = layer4
        var4.bandNumber = 1
        entries.append( var4 )
    
    elif n_variables ==5:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
        
        fileInfo = QFileInfo(raster_inputs[3])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer4 = QgsRasterLayer(path, baseName)
        var4 = QgsRasterCalculatorEntry()
        var4.ref = 'layer4@1'
        var4.raster = layer4
        var4.bandNumber = 1
        entries.append( var4 )
        
        fileInfo = QFileInfo(raster_inputs[4])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer5 = QgsRasterLayer(path, baseName)
        var5 = QgsRasterCalculatorEntry()
        var5.ref = 'layer5@1'
        var5.raster = layer5
        var5.bandNumber = 1
        entries.append( var5 )
    

    calc = QgsRasterCalculator(ecuacion, 
                                raster_salida, 
                                'GTiff', 
                                layer1.extent(), 
                                layer1.width(), 
                                layer1.height(),
                                entries)
                                
    calc.processCalculation()



def raster_calc_qgis(ecuacion,raster_inputs,raster_salida):
    n_variables=len(raster_inputs)

    entries = []

    #abre el archivo raster1
    fileInfo = QFileInfo(raster_inputs[0])
    path = fileInfo.filePath()
    baseName = fileInfo.baseName()
    layer1 = QgsRasterLayer(path, baseName)
    var1 = QgsRasterCalculatorEntry()
    var1.ref = 'layer1@1'
    var1.raster = layer1
    var1.bandNumber = 1
    entries.append( var1 )
    
    if n_variables ==2:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
    elif n_variables ==3:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
    
    elif n_variables ==4:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
        
        fileInfo = QFileInfo(raster_inputs[3])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer4 = QgsRasterLayer(path, baseName)
        var4 = QgsRasterCalculatorEntry()
        var4.ref = 'layer4@1'
        var4.raster = layer4
        var4.bandNumber = 1
        entries.append( var4 )
    
    elif n_variables ==5:
        fileInfo = QFileInfo(raster_inputs[1])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer2 = QgsRasterLayer(path, baseName)
        var2 = QgsRasterCalculatorEntry()
        var2.ref = 'layer2@1'
        var2.raster = layer2
        var2.bandNumber = 1
        entries.append( var2 )
        
        fileInfo = QFileInfo(raster_inputs[2])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer3 = QgsRasterLayer(path, baseName)
        var3 = QgsRasterCalculatorEntry()
        var3.ref = 'layer3@1'
        var3.raster = layer3
        var3.bandNumber = 1
        entries.append( var3 )
        
        fileInfo = QFileInfo(raster_inputs[3])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer4 = QgsRasterLayer(path, baseName)
        var4 = QgsRasterCalculatorEntry()
        var4.ref = 'layer4@1'
        var4.raster = layer4
        var4.bandNumber = 1
        entries.append( var4 )
        
        fileInfo = QFileInfo(raster_inputs[4])
        path = fileInfo.filePath()
        baseName = fileInfo.baseName()
        layer5 = QgsRasterLayer(path, baseName)
        var5 = QgsRasterCalculatorEntry()
        var5.ref = 'layer5@1'
        var5.raster = layer5
        var5.bandNumber = 1
        entries.append( var5 )
    

    calc = QgsRasterCalculator(ecuacion, 
                                raster_salida, 
                                'GTiff', 
                                layer1.extent(), 
                                layer1.width(), 
                                layer1.height(),
                                entries)
                                
    calc.processCalculation()


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


    