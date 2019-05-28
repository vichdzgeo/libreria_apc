Estilo de código en python
==========================



Dos buenas razones para romper una regla en particular:

    * Cuando el aplicar la regla, haga el código menos legible o confuso, incluso para alguien que está acostumbrado a leer códigos bajo este estilo.
    * Para ser consistente en código que también la rompe (tal vez por razones históricas) - aunque esto podría ser una oportunidad para limpiar el "desastre" de otra persona.


Identación
-----------
  * Usar espacios en lugar de tabulaciones

  * Se recomienda alinear verticalmente con el carácter que se ha utilizado (paréntesis, llaves, corchetes)

Si


::

  #Alineado con el paréntesis que abre la función
  foo = nombre_variable(var_uno,
                       var_dos,
                       var_tres,
                       var_cuatro)

No


::

 #Argumentos en la primera línea cuando no se esta haciendo uso de la alineacion vertical
 foo = nombre_variable(var_uno, var_dos,
     var_tres,var_cuatro)

Longitud de líneas
------------------

 * Limita todas las líneas de código a un máximo de 79 caracteres.
 * En el caso de largos bloques de texto ("docstrings" o comentarios), es recomendado limitarlo a 72 caracteres


Importaciones
-------------
Las importaciones siempre se colocan al comienzo del archivo,
simplemente luego de cualquier comentario o documentación del módulo,
y antes de las variables globales y constantes
Las importaciones deben estar en líneas separadas, por ejemplo:

::

  Sí: import os
      import sys
  No: import sys, os

Sin embargo es correcto decir:

::

  from subprocess import Popen, PIPE

Espacios en expresiones y sentencias
-----------------------------------------------

Evitar usar espacios en blanco extraños en las siguientes situaciones:

  * Inmediatamente dentro del paréntesis, corchetes o llaves:
    ::

      Sí: spam(ham[1], {eggs: 2})
      No: spam ham[ 1 ], { eggs: 2 } )

  * Antes de una coma, un punto y coma o dos puntos:

  * Antes del paréntesis o corchete
  * Más de un espacio alrededor de un operador de asignación.

  Si.

    ::

      x = 1
      y = 2
      variable_larga = 3

  No

    ::

      x              = 1
      y              = 2
      variable_larga = 3

  * No utilizar espacios alrededor del = (igual) cuando es utilizado para indicar un argumento en una función.

  Sí

    ::

      def complex(real, img=0.0):
        return magin(r=real, i= imag)

  No

    ::

      def complex(real, imag = 0.0):
        return magic(r = real, i = imag)


Comentarios
-----------

.. note::

  Siempre tener en prioridad mantener los comentarios al día cuando el
  código cambie

Comentarios que contradigan el código es peor que no colocar comentarios.




  * Los comentarios deben ser oraciones completas.
  * La primera palabra debe comenzar con mayúscula
  * Si un comentario es corto, el punto final puede omitirse
  * Usar dos espacios luego de una oración que termine con un punto.
  * Usar comentarios en línea escasamente y deberan ser separados por al menos dos espacios de la sentencia
    * Deben empezar con un # (numeral) seguido de un espacio


Docstrings
^^^^^^^^^^

Tambien llamadas cadenas de documentación.

Escribir "docstrings" para todos los módulos, funciones, clases y métodos
públicos.

Ejemplo
::


  def v_interseccion(vector_a, vector_b, path_s):
    '''
    Esta funcion calcula la interseccion  de las capas vectoriales
    superpuestas es decir, vector_a y vector_b

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
