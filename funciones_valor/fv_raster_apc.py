import math
import StringIO
import numpy
from os import listdir
import json


def leer_json(path):
    data = json.load(path)
path = "C:\Dropbox (LANCIS)\CARPETAS_TRABAJO\vhernandez\codigos_github\libreria_apc\funciones_valor\concava_dec.json"

data = json.load(path)
print data 


def normalize100(x, xmax, xmin):
    return (100.0 * (x - xmin)/(xmax - xmin))


def logistic(x, k, center, xmax, xmin):
    return 1 / (1.0
                + math.exp(-k * (
                    (100 * (x - xmin) / (xmax - xmin))
                    - (100 * (center - xmin) / (xmax - xmin)))))


def logistica_invertida(x, k, center, xmax, xmin):
    return 1.0 - logistic(x, k, center, xmax, xmin)


def gaussian(x, a, center, xmax, xmin):
    return math.exp(0.0 - ((
        (normalize100(x, xmax, xmin)
         - normalize100(center, xmax, xmin)) / (a))**2))


def campana_invertida(x, a, center, xmax, xmin):
    return 1.0 - gaussian(x, a, center, xmax, xmin)


def bojorquezSerrano(fp, categories=5, maximum=1.0, minimum=0.0):
    the_sum = 0
    for i in range(categories):
        the_sum += ((fp) ** i)

    bit = (maximum - minimum) / the_sum
    cuts = []
    cuts.append(minimum)
    for i in range(categories):
        prev = cuts[i]
        cut = prev + fp ** i * bit
        cuts.append(cut)

    return cuts


def concava_decreciente(x, gama, xmax, xmin):
    return ((math.exp(gama * (
        100.0 - (100.0*(x - xmin)
                 / (xmax - xmin))))) - 1) / (math.exp(gama * 100) - 1)


def concava_creciente(x, gama, xmax, xmin):
    return ((math.exp(
        gama * (100
                *
                (x - xmin)
                /
                (xmax - xmin)))) - 1) / (math.exp(gama * 100) - 1)


def convexa_decreciente(x, gama, xmax, xmin):
    return 1.0 - concava_creciente(x, gama, xmax, xmin)


def convexa_creciente(x, gama, xmax, xmin):
    return 1.0 - concava_decreciente(x, gama, xmax, xmin)


def linear(x, m, b):
    return (m * x) + b


def lineal_decreciente(x, m, b):
    return (m * x) + b


def normalize_max_min(y, maxy, miny):
    return (y - miny)/(maxy - miny)


def normalize01(y):
    maxy = max(y)
    miny = min(y)
    y_prima = [normalize_max_min(t, maxy, miny) for t in y]
    return y_prima

