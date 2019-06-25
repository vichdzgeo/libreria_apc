# -*- coding: utf-8 -*-

import qgis
from qgis.core import *
from qgis.analysis import *
from os.path import join
from PyQt4.QtCore import *
from osgeo import gdal, ogr, osr
import os
import sys
sys.path.append("/usr/share/qgis/python/plugins/")
import processing as pr
import time

'''
# Area de Planeacion Colaborativa (APC)
# Libreria para el procesamiento de datos geograficos en Python
# ver. 2.7) y Qgis (2.18).

# Autores: Fidel Serrano,Victor Hernandez

# Objetivo: Facilitar la creacion de scripts en los procesos de información
# geográfica
'''

def v_interseccion(vector_a, vector_b, path_s):
    '''
    v_interseccion(vector_a,vector_b,path_s)
    Esta funcion calcula la interseccion  de dos capas vectoriales es decir,
    vector_a y vector_b

    :param vector_a: Ruta o path de la capa A
    :type vector_a: String

    :param vector_b: Ruta o path de la capa B
    :type vector_b: String

    :param path_s: Ruta o path de salida de la capa
    :type path_s: String

    '''
    vector_a =  QgsVectorlayer(vector_a, "", "ogr")
    vector_b =  QgsVectorlayer(vector_b, "", "ogr")
    pr.runalg("saga:intersect", vector_a, vector_b, 0, path_s)


def area_km2(path_vector, nombre_campo):
    """
    Esta funcion genera un campo nuevo y calcula el area de cada
    poligono en kilometros cuadrados.

    :param path_vector: ruta de la capa vectorial, debe estar en una proyeccion
                        cartografica que exrprese sus unidades lineales,
                        ej: UTM14N o CCL
    :type path_vector: String

    :param nombre_campo: ingresar el nombre del campo ej: area_km2
    :type nombre_campo: string
    """

    if len(nombre_campo) > 10:
        print("el nombre del campo debe contener maximo 10 caracteres")
    else:
        vector = qgis.core.QgsVectorLayer(path_vector, "", "ogr")
        vector.dataProvider().addAttributes([QgsField(nombre_campo.lower(),
                                                      QVariant.Double)])

        vector.startEditing()

        for f in vector.getFeatures():
            a_km2 = ((f.geometry().area())/1000000)
            f[str(nombre_campo)] = a_km2
            vector.updateFeature(f)

        vector.commitChanges()


def area_ha(path_vector, nombre_campo):
    """
    Esta funcion genera un campo nuevo y calcula el area de cada
    poligono en hectareas Parametros:

    :param path_vector: ruta de la capa vectorial, debe estar en una \
                        proyeccion cartografica que exrprese sus unidades \
                        lineales, ej: UTM14N o CCL
    :type path_vector: String

    :param nombre_campo: ingresar el nombre del campo ej: area_ha
    :type nombre_campo: string
    """

    if len(nombre_campo) > 10:
        print("el nombre del campo debe contener maximo 10 caracteres")
    else:
        vector = qgis.core.QgsVectorLayer(path_vector,"","ogr")
        vector.dataProvider().addAttributes([QgsField(nombre_campo.lower(),
                                                      QVariant.Double)])

        vector.startEditing()

        for f in vector.getFeatures():
            a_ha = ((f.geometry().area())/10000)
            f[str(nombre_campo)] = a_ha
            vector.updateFeature(f)

        vector.commitChanges()


def vcopia(path_vector, path_salida):
    """
    Crea una copia de la capa a partir de la ruta de la capa,
    la capa es creada con el mismo sistema de referencia que el origen.

    :param path_vector: ruta de la capa original
    :type path_vector: String

    :param path_salida: ruta de donde sera almacenada la capa
    :type path_salida: String
    """
    vlayer = QgsVectorLayer(path_vector, "", "ogr")
    clonarv = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                      path_salida,
                                                      'utf-8',
                                                      vlayer.crs(),
                                                      "ESRI Shapefile")


def crear_campo( path_vector, nombre_campo, tipo):
    ''' Esta funcion crea un campo segun el tipo especificado.
    Parametros:
    :param path_vector: La ruta del archivo shapefile al cual se le quiere \
                        agregar el campo
    :type path_vector: String

    :param nombre_campo: Nombre del campo nuevo
    :type nombre_campo: Sting

    :param tipo: es el tipo de campo que se quiere crear

    Int: para crear un campo tipo entero
    Double: para crear un campo tipo doble o flotante
    String: para crear un campo tipo texto
    Date: para crear un campo tipo fecha
    :type tipo: String
    '''

    if len(nombre_campo) > 10:
        print("el nombre del campo debe contener maximo 10 caracteres")
    else:
        if tipo == "Int":
            nombre = QgsVectorLayer(path_vector, "", "ogr")
            nombre.dataProvider().addAttributes([QgsField(nombre_campo.lower(),
                                                          QVariant.Int)])
            return nombre
        elif tipo == "Double":
            nombre=QgsVectorLayer(path_vector, "", "ogr")
            nombre.dataProvider().addAttributes([QgsField(nombre_campo.lower(),
                                                          QVariant.Double)])
            return nombre
        elif tipo == "String":
            nombre=QgsVectorLayer(path_vector, "", "ogr")
            nombre.dataProvider().addAttributes([QgsField(nombre_campo.lower(),
                                                          QVariant.String)])
            return nombre
        elif tipo == "Date":
            nombre=QgsVectorLayer(path_vector, "", "ogr")
            nombre.dataProvider().addAttributes([QgsField(nombre_campo.lower(),
                                                          QVariant.Date)])
            return nombre
        else:
            print ("el tipo no existe o hay error en su declaracion")


def id_texto(path_layer,nombre_id,):
    '''
    Esta función genera un id numerico en un campo de tipo texto
    :param path_layer: ruta del Shapefile
    :type path_layer: String

    :param nombre_id: Nombre del campo no mayor a 10 caracteres
    :type nombre_id: String
    '''

    crear_campo(path_layer,nombre_id,"String")
    layer =QgsVectorLayer(path_layer,"","ogr")
    cont =1
    layer.startEditing()
    for ag in layer.getFeatures():
        ag[nombre_id]=str(cont)
        cont +=1
        layer.updateFeature(ag)

    layer.commitChanges()

def id_int(path_layer,nombre_id,):
    '''
    Esta función genera un id numerico en un campo de tipo entero
    :param path_layer: ruta del Shapefile
    :type path_layer: String

    :param nombre_id: Nombre del campo no mayor a 10 caracteres
    :type nombre_id: String
    '''

    crear_campo(path_layer,nombre_id,"Int")
    layer =QgsVectorLayer(path_layer,"","ogr")
    cont =1
    layer.startEditing()
    for ag in layer.getFeatures():
        ag[nombre_id]=cont
        cont +=1
        layer.updateFeature(ag)

    layer.commitChanges()

def colonia_ageb(path_salida, path_agebs, path_colonias,ageb_id, col_id,
                 campos_resampling, nombre_temp):

    '''
    Esta función realiza un escalamiento de datos que estan a nivel geométrico
    de colonía y los pasa a nivel de ageb.


    :param path_salida: Ruta de la salida de la capa a nivel de ageb
    :type path_salida: String

    :param path_agebs: ruta de la capa de agebs
    :type path_agebs: String

    :param path_colonias:  ruta de la capa de colonias
    :type path_colonias: String

    :param ageb_id: nombre del campo de id de los agebs
    :type ageb_id: String

    :param col_id: nombre del campo de id de la colonia
    :type col_id: String

    :param campos_resampling: nombre de los campos de la cap de colonia
    :type campos_resampling: List the strings

    :param nombre_temp: nombre del archivo que se genera al intersectar la \
                        copia de colonias con la de agebs
    :type nombre_temp: String
    '''
    new_geom_id = ageb_id
    new_geom = QgsVectorLayer(path_agebs, "", "ogr")
    old_geom = QgsVectorLayer(path_colonias, "", "ogr")

    print ("llenando con ceros los campos que son nulos ...")
    old_geom.startEditing()
    for poligono in old_geom.getFeatures():
        for resampling in campos_resampling:
            if poligono[resampling] is None:
                poligono[resampling] = 0.0
            old_geom.updateFeature(poligono)

    old_geom.commitChanges()

    print ("calculando areas ...")
    new_geom.dataProvider().addAttributes([QgsField("area_new",
                                                    QVariant.Double)])
    new_geom.updateFields()
    new_geom.startEditing()
    for poligono in new_geom.getFeatures():
        poligono["area_new"] = poligono.geometry().area()
        new_geom.updateFeature(poligono)
    new_geom.commitChanges()

    old_geom.dataProvider().addAttributes([QgsField("area_old",
                                                    QVariant.Double)])
    old_geom.updateFields()
    old_geom.startEditing()
    for poligono in old_geom.getFeatures():
        poligono["area_old"] = poligono.geometry().area()
        old_geom.updateFeature(poligono)
    old_geom.commitChanges()

    print ("intersectando...")

    QgsOverlayAnalyzer().intersection(new_geom,
                                      old_geom,
                                      join(path_salida, nombre_temp))
    intersection = QgsVectorLayer(join(path_salida,
                                       nombre_temp),
                                  "intersection", "ogr")
    intersection.dataProvider().addAttributes([QgsField("area_bit",
                                                        QVariant.Double)])
    intersection.updateFields()
    intersection.startEditing()
    for poligono in intersection.getFeatures():
        poligono["area_bit"] = poligono.geometry().area()
        intersection.updateFeature(poligono)
    intersection.commitChanges()

    for resamplingField in campos_resampling:
            new_geom.dataProvider().addAttributes([QgsField(resamplingField,
                                                            QVariant.Double)])
            new_geom.updateFields()

    new_geom.startEditing()

    for poligono in new_geom.getFeatures():

        print ("procesando el poligono", poligono[new_geom_id], ":")
        for resamplingField in campos_resampling:

            request = QgsFeatureRequest().setFilterExpression(
                '"'
                + new_geom_id
                + '" = '
                + str(poligono[new_geom_id]))
            request.setFlags(QgsFeatureRequest. NoGeometry)

            new_field_value = 0.0
            for bit in intersection.getFeatures(request):
                new_field_value += (bit["area_bit"]
                                    / bit["area_old"]) \
                                    * float(bit[resamplingField])

            poligono[resamplingField] = new_field_value
            new_geom.updateFeature(poligono)

    new_geom.commitChanges()

def est_raster_media(path_vector, path_raster, nombre_campo):
    '''
    Esta funcion calcula la media de los valores de pixel de un raster
    contenidos en un área superpuesta de una capa vectorial.

    Parametros:
    :param path_vector: ruta de la capa que contendra los datos extraidos del \
                        archivo raster
    :type path_vector:String

    :param path_raster: ruta de la capa raster de la cual se extraera el valor
    :type path_raster: String

    :param nombre_campo: nombre del campo que se creara para agregar los \
                         valores de la capa raster a la capa vectorial
    :type nombre_campo: String

    '''
    vector=QgsVectorLayer(path_vector, "", "ogr")
    zoneStat = QgsZonalStatistics(vector, path_raster,
                                  nombre_campo, 1, QgsZonalStatistics.Mean)
    zoneStat.calculateStatistics(None)


def raster_poligono(path_tif, path_s_vector, nombre_campo, epsg):
    """
    Realiza el proceso de vectorización de una capa raster
    Parametros:

    :param path_tif: ruta de la capa raster
    :type path_tif: String

    :param path_s_vector: ruta de salida de la capa vectorial
    :type path_s_vector: String

    :param nombre_campo: nombre de un nuevo campo que contiene los valores \
                         de pixel
    :type nombre_campo: String

    :param epsg: Código EPSG para la zona 14N UTM con datum WGS84 el \
                 código es 32614
    :type epsg: Int
    """
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)

    fileInfo = QFileInfo(path_tif)
    baseName = fileInfo.baseName()

    sourceRaster = gdal.Open(path_tif)
    band = sourceRaster.GetRasterBand(1)

    outShapefile = baseName
    driver = ogr.GetDriverByName("ESRI Shapefile")

    path_v = path_s_vector + outShapefile+ ".shp"
    outDatasource = driver.CreateDataSource(path_v)
    outLayer = outDatasource.CreateLayer(str(outShapefile), srs)
    newField = ogr.FieldDefn(nombre_campo, ogr.OFTInteger)
    outLayer.CreateField(newField)
    gdal.Polygonize(band, None, outLayer, 0, [], callback=None)
    outDatasource.Destroy()
    sourceRaster = None


def union_csv_shape(path_csv, path_vector, n_campo_comun, path_salida):
    '''
        Función para unir una base de datos csv a un archivo shapefile, \
        por medio de un campo en común.
        El resultado es una nueva capa vectorial con la unión tabular.
        Parametros:

        :param path_csv: ruta del archivo csv.
        :type path_csv: String

        :param path_vector: ruta de la capa vectorial
        :type path_vector: String

        :param n_campo_comun: nombre del campo en comun
        :type n_campo_comun: String

        :param path_salida: ruta de salida para la nueva capa vectorial que \
                            contiene la union
        :type path_salida: String

        .. warning::

            Para el separador de directorios en la ruta usar "/"

    '''
    vector = QgsVectorLayer(path_vector, "", "ogr")
    QgsMapLayerRegistry.instance().addMapLayer(vector)

    #abre  el archivo csv
    bd_csv_uri = "file:///" \
                 + path_csv \
                 + "?delimiter=%s&encoding=%s" % (",", "utf-8")
    bd_csv = QgsVectorLayer(bd_csv_uri, "", "delimitedtext")
    QgsMapLayerRegistry.instance().addMapLayer(bd_csv)

    # Nombre de los campos de ID para relacionar las tablas
    vector_id = n_campo_comun
    bd_csv_id = n_campo_comun

    # union del archivo csv y vector.
    unionC = QgsVectorJoinInfo()
    unionC.prefix = ''
    unionC.joinLayerId = bd_csv.id()
    unionC.joinFieldName = vector_id
    unionC.targetFieldName = bd_csv_id
    unionC.memoryCache = True
    vector.addJoin(unionC)

    QgsVectorFileWriter.writeAsVectorFormat(vector,
                                            path_salida,
                                            'utf-8',
                                            vector.crs(),
                                            "ESRI Shapefile")


def v_cortar(path_mask, path_zona, path_salida):
    '''
    Esta función permite cortar dos capas vectoriales
    Parametros:

    :param path_mask: ruta de la capa vectorial que sirve como mascara de corte.
    :type path_mask: String

    :param path_zona: ruta de la capa vectorial de la capa a cortar.
    :type path_mask: String

    :param path_salida: ruta de la capa generada por el proceso.
    :type path_mask: String
    '''
    pr.runalg("saga:polygonclipping", path_mask, path_zona, path_salida)


def lista_shp(path_carpeta):
    '''


    :param path_carpeta: ruta que contiene los archivos shape a procesar
    :type path_carpeta: String
    '''
    for root, dirs, files in os.walk(path_carpeta):
        lista = []
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.shp':
                lista.append(extension)
    return lista


def wgs84_a_utm(path_gws84, path_utm, zona_norte):
    '''
    Esta función reproyecta una capa que su sistema de referencía es WGS84 a
    UTM

    :param path_wgs84: Ruta de la capa vectorial
    :type path _wgs84: String

    :param path_utm: Ruta con nombre de la nueva capa reproyectada en UTM
    :param path_utm: String

    :param zona_norte: Número de zona UTM que le corresponde
    :type zona_norte: Int

    .. Note::

       Las zonas UTM para México son :

       ==== =================
       Zona Meridiano central
       ==== =================
       11   87°W
       12   93°W
       13   99°W
       14   105°W
       15   111°W
       16   117°W
       ==== =================
    '''


    vlayer = QgsVectorLayer(path_gws84,"","ogr")

    if zona_norte==11:
        crs = QgsCoordinateReferenceSystem("EPSG:32611")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm,
                                                           'utf-8',
                                                           crs,
                                                           "ESRI Shapefile")
    elif zona_norte==12:
        crs = QgsCoordinateReferenceSystem("EPSG:32612")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm,
                                                           'utf-8',
                                                           crs,
                                                           "ESRI Shapefile")
    elif zona_norte==13:
        crs = QgsCoordinateReferenceSystem("EPSG:32613")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm,
                                                           'utf-8',
                                                           crs,
                                                           "ESRI Shapefile")
    elif zona_norte==14:
        crs = QgsCoordinateReferenceSystem("EPSG:32614")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm,
                                                           'utf-8',
                                                           crs,
                                                           "ESRI Shapefile")
    elif zona_norte==15:
        crs = QgsCoordinateReferenceSystem("EPSG:32615")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm,
                                                           'utf-8',
                                                           crs,
                                                           "ESRI Shapefile")
    elif zona_norte==16:
        crs = QgsCoordinateReferenceSystem("EPSG:32616")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm,
                                                           'utf-8',
                                                           crs,
                                                           "ESRI Shapefile")
    else:
        print ("error en el numero de zona")


def proy_a_wgs84(path_capa, path_wgs84):
    crs = QgsCoordinateReferenceSystem("EPSG:4326")
    vlayer = QgsVectorLayer(path_capa, "", "ogr")
    proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                       path_wgs84,
                                                       'utf-8',
                                                       crs,
                                                       "ESRI Shapefile")


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


def nombre_archivo(ruta):
    '''
    Esta funcion extrae de la ruta el nombre del archivo shapefile sin extensión
    Parametros:

    :param ruta: ruta de la capa shapefile
    :type ruta: String

    '''
    nombre_cort = ruta.split("/")[-1:]
    nombre = nombre_cort[0].split(".")[0]
    return nombre


def validacion_prj(path_carpeta):
    '''
    Esta función recibe una carpeta que contenga los archivos shapefile
    y verifica que para cada archivo shapefile exista un archivo prj,
    Regresa en una lista los archivos que no cumplen con esta condición
    Parametros:

    :param path_carpeta: ruta donde se encuentran los archivos shapefile
    :type path_carpeta: String

    '''
    sin_proj = []
    lista_shp = lista_archivos(path_carpeta, "shp")
    lista_prj = lista_archivos(path_carpeta, "prj")

    for arch_shape in lista_shp:
        capa = arch_shape.split(".")[0]
        coinc = 0
        for prj in lista_prj:
            if capa == prj.split(".")[0]:
                coinc += 1
        if coinc == 0:
            sin_proj.append(
                "Warning: no existe el archivo prj para la capa " + arch_shape)
    return sin_proj


def extension_capa(path_capa): #subfunción de crear_metadatos
    vlayer = QgsVectorLayer(path_capa, "", "ogr")
    lista=[]
    if vlayer.crs().authid() == "EPSG:4326":
        lista.append(path_capa)
        ext = vlayer.extent()
        xmin = ext.xMinimum()
        xmax = ext.xMaximum()
        ymin = ext.yMinimum()
        ymax = ext.yMaximum()
        extend = {"norte": ymax,
                  "sur": ymin,
                  "este": xmax,
                  "oeste": xmin}
        lista.append(extend)

    else:
        nombre = nombre_archivo(path_capa)

        ruta_temp = "/".join(
            path_capa.split("/")[:-1]) + "/tp_wgs84_" + nombre + ".shp"
        lista.append(ruta_temp)
        proy_a_wgs84(path_capa, ruta_temp)
        vlayer_wgs84 = QgsVectorLayer(ruta_temp, "", "ogr")
        ext = vlayer_wgs84.extent()
        xmin = ext.xMinimum()
        xmax = ext.xMaximum()
        ymin = ext.yMinimum()
        ymax = ext.yMaximum()
        extend = {"norte": ymax,
                  "sur": ymin,
                  "este": xmax,
                  "oeste": xmin}
        lista.append(extend)

    return lista

def borrar_shape(ruta_shape): #subfunción
    path_dir = "/".join(ruta_shape.split("/")[:-1]) + "/"
    lista_archivos = os.listdir(path_dir)
    for archivo in lista_archivos:
        if archivo.split(".")[0] == nombre_archivo(ruta_shape):
            os.remove(path_dir+archivo)


def extension_vector(ruta_capa): #subfunción
    '''Esta función regresa una lista con las coordendas de la extensión
    geográfica de la capa.

    :param ruta_capa: ruta de la capa vectorial en formato shapefile
    :type ruta_capa: String


    '''
    ruta= extension_capa(ruta_capa)
    borrar_shape(ruta)

def campos_md(ruta_shape): #subfunción
    layer = QgsVectorLayer(ruta_shape,"","ogr")
    nuevo_path = "/".join(ruta_shape.split("/")[:-1]) + "/"
    nombre="md_"+nombre_archivo(ruta_shape)+".md"
    archivo = open(nuevo_path+nombre,"w")

    archivo.write("Campo | Tipo | Descripción \n")
    archivo.write("--- | --- | --- |\n")

    campos = [field.name()
              +" | "
              + field.typeName()
              + " | " for field in layer.fields()]

    for campo in campos:
        archivo.write(campo+"\n")
    archivo.close()


def metadatos(ruta_shape):
    vlayer = QgsVectorLayer(ruta_shape,"","ogr")
    nuevo_path = "/".join(ruta_shape.split("/")[:-1]) + "/"
    nombre="md_"+nombre_archivo(ruta_shape)+".md"
    archivo = open(nuevo_path + nombre,"w")
    archivo.write("# Metadatos de la capa "+nombre_archivo(ruta_shape)+"\n")
    archivo.write("## Ruta \n")
    archivo.write(ruta_shape+"\n")
    archivo.write("## Sistema de coordendas "+"\n")
    archivo.write(vlayer.crs().authid() + "\n")
    ruta_temp = ""

    lista=[]
    if vlayer.crs().authid() == "EPSG:4326":
        lista.append(ruta_shape)
        ext = vlayer.extent()
        xmin = ext.xMinimum()
        xmax = ext.xMaximum()
        ymin = ext.yMinimum()
        ymax = ext.yMaximum()
        extend = {"norte": ymax,
                  "sur": ymin,
                  "este": xmax,
                  "oeste": xmin}
        lista.append(extend)

    else:
        nombre = nombre_archivo(ruta_shape)

        ruta_temp = "/".join(
            ruta_shape.split("/")[:-1]) + "/tp_wgs84_" + nombre + ".shp"
        lista.append(ruta_temp)
        proy_a_wgs84(ruta_shape, ruta_temp)
        vlayer_wgs84 = QgsVectorLayer(ruta_temp, "", "ogr")
        ext = vlayer_wgs84.extent()
        xmin = ext.xMinimum()
        xmax = ext.xMaximum()
        ymin = ext.yMinimum()
        ymax = ext.yMaximum()
        extend = {"norte": ymax,
                  "sur": ymin,
                  "este": xmax,
                  "oeste": xmin}
        lista.append(extend)
    archivo.write("## Total de elementos \n")
    archivo.write(str(vlayer.featureCount())+"\n")
    archivo.write("## Extensión geográfica \n")
    archivo.write("Norte = " + str(lista[1]["norte"]) + "\n")
    archivo.write("Sur = " + str(lista[1]["sur"]) + "\n")
    archivo.write("Este = " + str(lista[1]["este"]) + "\n")
    archivo.write("Oeste = " + str(lista[1]["oeste"]) + "\n")

    archivo.write("## Lista de campos \n\n")
    campos = [field.name() for field in vlayer.fields()]
    archivo.write("### Total de campos\n")
    archivo.write(str(len(campos))+"\n\n")
    archivo.write("Campo | Tipo | Descripción | Rango | Unidades\n")
    archivo.write("--- | --- | --- | --- | --- | \n")


    for field in vlayer.fields():
        lista=[]
        if not field.typeName()=="String" or field.typeName()=="Date":
            for feature in vlayer.getFeatures():

                if  not feature[field.name()] == NULL:
                    lista.append(feature[field.name()])

            archivo.write(field.name()
                          + " | "
                          + field.typeName()
                          + " | "
                          + " | "
                          + str(min(lista))
                          + " - "
                          + str(max(lista))
                          + " | "
                          + "\n")
        else:
            #print field.name()," | ",field.typeName()," | "," | "," ","\n"
            archivo.write(field.name()
                          + " | "
                          + field.typeName()
                          + " | "
                          + " | "
                          + " |"
                          + "\n")



    archivo.close()


    print ("metadatos creados")
    return ruta_temp

def crear_metadatos(ruta_shape):
    '''
    Esta función generá un archivo MD que contiene la ruta, extensión geográfica
    , nombre de campos y tipo, rango (en caso de aplicar). elementos básicos
    para la generación de metadatos en geonetwork.

    :param ruta_shape: ruta de la capa vectorial en formato shapefile
    :type ruta_shape: String

    '''
    capa = metadatos(ruta_shape)
    if capa == "":
        print ("se ha creado el archivo md en el direcctorio")
    else:
        borrar_shape(capa)
        print ("se ha creado el archivo md en el direcctorio")

def campos_minusculas(path_shape):
    layer = QgsVectorLayer(path_shape,"","ogr")
    campos = [field.name() for field in layer.fields()]
    for campo in campos:
        for field in layer.pendingFields():
            if campo == field.name():
                with edit(layer):
                    idx = layer.fieldNameIndex(field.name())
                    layer.renameAttribute(idx,field.name().lower())
    print ("Proceso terminado")
