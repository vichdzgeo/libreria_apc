import os
import pandas as pd
import numpy as np


def nombre_archivo(ruta):
    '''
    Esta funcion extrae de la ruta el nombre del archivo shapefile
    Parametros:
        ruta = ruta de la capa shapefile
    '''
    nombre_cort = ruta.split("/")[-1:]
    nombre = nombre_cort[0].split(".")[0]
    return nombre

def lista_archivos(ruta,ext):
    lista=[]
    for root, dirs, files in os.walk(ruta, topdown=False):
       for name in files:
           if name.endswith(ext):
               #print(os.path.join(root, name))
               liga=root+"/"+name
               lista.append(liga)
    return lista

def df_empty(columns, dtypes, index=None):
   df = pd.DataFrame(index=index)
   for c,d in zip(columns, dtypes):
       df[c] = pd.Series(dtype=d)
   return df

path_esc=("C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/\
dataframe_prec_esc/insumos/experimentos/")

agebs_swat = pd.read_csv("C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/procesamiento/encharcamientos_escorrentias/swat_agebs.csv")
lista_esc=lista_archivos(path_esc,"csv")

for path in lista_esc:
    escorrentias_85_85 = pd.read_csv(path)

    el_dataframe = df_empty(['year', 'ageb_id', 'prec', 'runoff'],dtypes=[np.int, np.int, np.float64, np.float64])

    print (path)
    for year in range(1993,2014):
        prec_df = pd.read_csv("C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/\
procesamiento/precipitacion_hist_esc/salida/csv/\
tp_agebs_prec_hist_esc_"+str(year)+".csv")
        for index, row in agebs_swat.iterrows():
            ageb_id = row['ageb_id']
            sus_swat = str(row['sus_swat']).split(";")

            escorrentia = 0
            esc_field = "esc_"+ str(year)
            if 'nan' not in sus_swat:
                for swat in sus_swat:

                    el_renglon = escorrentias_85_85.query('swat_id=='+swat)
                    for index, row in el_renglon.iterrows():
                        escorrentia += row[esc_field]

            el_renglon_prec = prec_df.query('ageb_id=='+str(ageb_id))
            prec = 0
            for index, row in el_renglon_prec.iterrows():

                if "ff45" in nombre_archivo(path):
                    prec = row['he_85_85']

                elif "nf45" in nombre_archivo(path):
                    prec = row['he_45_55']

                elif "nf85" in nombre_archivo(path):
                    prec = row['he_85_55']

                elif "ff85" in nombre_archivo(path):
                    prec = row['he_85_85']

            dicc = {'year' : year, 'ageb_id' : ageb_id, 'prec' : prec,'runoff' : escorrentia}
            el_dataframe = el_dataframe.append(dicc, ignore_index = True)
            print (year, ageb_id, prec, escorrentia)

    el_dataframe.to_csv("C:/Dropbox (LANCIS)/SIG/desarrollo/sig_megadapt/\
procesamiento/dataframe_prec_esc/salida/df_prec_"+nombre_archivo(path)+".csv")
