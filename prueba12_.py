import os
import apc
from datetime import datetime, date, time, timedelta

path_sig="C:/Dropbox (LANCIS)/CAPACITACION/cursos_no_formales/curso_python_gis_2_18/materiales/insumos/"
path_tif=path_sig+"prec/"

for age in range(2000, 2003):
    lista_tif=apc.lista_archivos([],path_tif+str(age)+"/",path_tif+str(age)+"/",[],"tif")
    fecha=date(age, 01, 01)
    path=path_tif+str(age)
    for dia in range(len(lista_tif)):

        fecha_a=fecha+timedelta(days=dia)
        fe=fecha_a.strftime("%Y%m%d")
        p_tif=path+"/Prec_%s_Liv_06_UTM.tif"%fe
        print p_tif
