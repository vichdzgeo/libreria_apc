# -*- coding: utf-8 -*-

import qgis
from qgis.core import *
from qgis.analysis import *
from os.path import join
from PyQt4.QtCore import *
from osgeo import gdal, ogr, osr
import os
import processing as pr
import time


# Area de Planeacion Colaborativa (APC)
# Libreria para el procesamiento de datos geograficos en Python
# ver. 2.7) y Qgis (2.18).

# Autores: Fidel Serrano,Victor Hernandez

# Objetivo: Facilitar la creacion de scripts en los procesos de información
# geográfica


def v_interseccion(vector_a, vector_b, path_s):
    '''
    v_interseccion(vector_a,vector_b,path_s)
    Esta funcion calcula la interseccion geometrica de las capas poligonales
    superpuestas es decir, vector_a y vector_b
    Parametros:
        vector_a =
        vector_b =
    '''
    pr.runalg("saga:intersect", vector_a, vector_b, 0, path_s)


def area_km2(path_vector, nombre_campo):
    """
    Esta funcion genera un campo nuevo y calcula el area de cada
    poligono en kilometros cuadrados.

    :param path_vector: ruta de la capa vectorial, debe estar en una proyeccion
                        cartografica que exrprese sun unidades lineales,
                        ej: UTM14N o CCL
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

    :param path_vector: ruta de la capa vectorial, debe estar en una
                        proyeccion cartografica que exrprese sun unidades
                       lineales, ej: UTM14N o CCL
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
    :param path_salida: ruta de donde sera almacenada la capa
    """
    vlayer = QgsVectorLayer(path_vector, "", "ogr")
    clonarv = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                      path_salida,
                                                      'utf-8',
                                                      vlayer.crs(),
                                                      "ESRI Shapefile")


def crear_campo(path_vector, nombre_campo, tipo):
    ''' Crear_campo(path_vector,nombre_campo,tipo)
    Esta funcion crea un campo segun el tipo especificado.
    Parametros:
        path_vector: La ruta del archivo shapefile al cual se le quiere
                      agregar el campo
        nombre_campo: Nombre del campo nuevo
        tipo: es el tipo de campo que se quiere crear:
        Int: para crear un campo tipo entero
        Double: para crear un campo tipo doble o flotante
        String: para crear un campo tipo texto
        Date: para crear un campo tipo fecha '''

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


def colonia_ageb(path_salida,
                 path_agebs,
                 path_colonias,
                 ageb_id,
                 col_id,
                 campos_resampling,
                 nombre_temp):
    '''
    Parametros:
    path_salida = Ruta de la salida de los datos
    path_agebs = ruta de la capa de agebs
    path_colonias =  ruta de la capa de colonias
    ageb_id = nombre del campo de id de los agebs
    col_id = nombre del campo de id de la colonia
    campos_resampling = nombre de los campos
    nombre_temp = nombre del archivo que se genera al intersectar la copia de
    colonias con la de agebs
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
    Esta funcion calcula la media de los valores de pixel
    contenidos en un raster sobreponiendo una capa vectorial de poligonos
    Parametros:
        path_vector = ruta de la capa que contendra los datos extraidos del archivo raster
        path_raster = ruta de la capa raster de la cual se extraera el valor
        nombre_campo = nombre del campo que se creara para agregar los valores de la capa
        raster a la capa vectorial
    '''
    vector=QgsVectorLayer(path_vector, "", "ogr")
    zoneStat = QgsZonalStatistics(vector, path_raster,
                                  nombre_campo, 1, QgsZonalStatistics.Mean)
    zoneStat.calculateStatistics(None)


def raster_poligono(path_tif, path_s_vector, nombre_campo, epsg):
    """
    Realiza el proceso de vectorizacion de una capa raster
    Parametros:
        path_tif= ruta de la capa raster
        path_s_vector= ruta de salida de la capa vectorial
        nombre_campo= nombre de un nuevo campo que contiene los valores de pixel
        epsg:
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
        Funcion para unir una base de datos csv a un archivo shapefile, por medio de un campo en comun.
        El resultado es una nueva capa vectorial con la union tabular.
        Parametros:
            path_csv = ruta del archivo csv, usar / en vez de '\'
            path_vector = ruta de la capa vectorial
            n_campo_comun = nombre del campo en comun
            path_salida = ruta de salida para la nueva capa vectorial que contiene la union
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
    Esta funcion permite cortar dos capas vectoriales
    Parametros:
        path_mask= capa vectorial que sirve como mascara de recorte.
        path_zona= capa vectorial de la capa a recortar.
        path_salida= ruta de la capa generada por el proceso.
    '''
    pr.runalg("saga:polygonclipping", path_mask, path_zona, path_salida)


def lista_shp(path_carpeta):
    '''
    Parametros:
        path_carpeta = ruta que contiene los archivos shape a procesar
    '''
    for root, dirs, files in os.walk(path_carpeta):
        lista = []
        for name in files:
            extension = os.path.splitext(name)
            if extension[1] == '.shp':
                lista.append(extension)
    return lista


def wgs84_a_utm(path_gws84, path_utm, zona_norte):

    vlayer = QgsVectorLayer(path_gws84,"","ogr")

    if zona_norte==11:
        crs = QgsCoordinateReferenceSystem("EPSG:32611")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm16n,
                                                           'utf-8',
                                                           crs,
                                                           "ESRI Shapefile")
    elif zona_norte==12:
        crs = QgsCoordinateReferenceSystem("EPSG:32612")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm16n,
                                                           'utf-8',
                                                           crs,
                                                           "ESRI Shapefile")
    elif zona_norte==13:
        crs = QgsCoordinateReferenceSystem("EPSG:32613")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm16n,
                                                           'utf-8',
                                                           crs,
                                                           "ESRI Shapefile")
    elif zona_norte==14:
        crs = QgsCoordinateReferenceSystem("EPSG:32614")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm16n,
                                                           'utf-8',
                                                           crs,
                                                           "ESRI Shapefile")
    elif zona_norte==15:
        crs = QgsCoordinateReferenceSystem("EPSG:32615")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm16n,
                                                           'utf-8',
                                                           crs,
                                                           "ESRI Shapefile")
    elif zona_norte==16:
        crs = QgsCoordinateReferenceSystem("EPSG:32616")
        proyecta = QgsVectorFileWriter.writeAsVectorFormat(vlayer,
                                                           path_utm16n,
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


def lista_archivos(lista_a, path, path_d, folders_check, tipo_ext):
    '''
    Esta funcion recursiva regresa una lista que contiene los
    archivos contenidos en un directorio segun el tipo de extension declarado.

    Parametros:
        lista_a=[]
        path= ruta de la carpeta (primer nivel) que contiene los archivos
        path_d= ruta de la carpeta (primer nivel) que contiene los archivos
        folders_check= []
        tipo_ext= se especifica la extension del archivo
        ejemplo:
        lista_shapes=apc.lista_archivos([],path_sig,path_sig,[],"shp")
    '''
    lista_tipo_ext = []
    if (path_d != path):
        folders_check.append(path_d)
    for f in os.listdir(path_d):
        d = path_d + f
        if os.path.isdir(d) and d not in folders_check:
            lista_archivos(lista_a,
                           path,
                           d + "/",
                           folders_check,
                           tipo_ext)
        else:
            if os.path.isfile(d):
                lista_a.append(path_d+f)
    for archivo in lista_a:
        if archivo.endswith(tipo_ext):
            lista_tipo_ext.append(archivo)
    return lista_tipo_ext


def nombre_archivo(ruta):
    '''
    Esta funcion extrae de la ruta el nombre del archivo shapefile
    Parametros:
        ruta = ruta de la capa shapefile
    '''
    nombre_cort = ruta.split("/")[-1:]
    nombre = nombre_cort[0].split(".")[0]
    return nombre


def validacion_prj(lista_paths):
    '''
    Parametros:

        lista_paths=ruta donde se encuentran los archivos shapefile
    '''
    sin_proj = []
    lista_shp = lista_archivos([], lista_paths, lista_paths, [], "shp")
    lista_prj = lista_archivos([], lista_paths, lista_paths, [], "prj")

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


def extension_capa(path_capa):
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

def borrar_shape(ruta_shape):
    path_dir = "/".join(ruta_shape.split("/")[:-1]) + "/"
    lista_archivos = os.listdir(path_dir)
    for archivo in lista_archivos:
        if archivo.split(".")[0] == nombre_archivo(ruta_shape):
            os.remove(path_dir+archivo)

def clean_var(nombre_var):
    gl=globals().copy()
    for var in gl:
        if var == nombre_var:
            del globals()[var]

def extension_vector(ruta_capa):
    ruta= extension_capa(ruta_capa)
    borrar_shape(ruta)

def campos_md(ruta_shape):
    layer = QgsVectorLayer(ruta_shape,"","ogr")
    nuevo_path = "/".join(ruta_shape.split("/")[:-1]) + "/"
    nombre="md_"+nombre_archivo(ruta_shape)+".md"
    archivo = open(nuevo_path+nombre,"w")

    archivo.write("Campo | Tipo | Descripción \n")
    archivo.write("--- | --- | --- |\n")

    campos = [field.name()+" | "+field.typeName() + " | " for field in layer.fields()]

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


            #print field.name()," | ",field.typeName()," | "," | ",min(lista),"-",max(lista),"\n"
            archivo.write(field.name()+" | "+field.typeName()+" | "+" | "+str(min(lista))+" - "+str(max(lista))+" | "+"\n")
        else:
            #print field.name()," | ",field.typeName()," | "," | "," ","\n"
            archivo.write(field.name()+" | "+field.typeName()+" | "+" | "+" |"+"\n")



    archivo.close()


    print ("metadatos creados")
    return ruta_temp

def crear_metadatos(ruta_shape):
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
