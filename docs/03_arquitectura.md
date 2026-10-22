# 3. Arquitectura

## 3.1 Visión general

La versión 1.1 se divide en cuatro componentes principales:

    Toolbox
    │
    ├── Motor simbólico
    │     ├── Syms
    │     ├── Expresion
    │     ├── Sin
    │     ├── Cos
    │     └── Potencia
    │
    ├── Núcleo matricial
    │     └── Matriz
    │
    ├── Transformaciones
    │     ├── Rx
    │     ├── Ry
    │     ├── Rz
    │     ├── RPY
    │     └── Traslación
    │
    └── Presentación
          └── formato.py

Cada componente tiene una responsabilidad específica.

## 3.2 Motor simbólico

El motor simbólico utiliza objetos que representan expresiones matemáticas en lugar de almacenar únicamente texto.

Los elementos principales son:

### `Syms`

Representa una variable simbólica.

Ejemplo:

    theta = Syms("theta")

### `Expresion`

Representa operaciones entre elementos simbólicos.

Los operadores principales son:

    +
    -
    *

También existe una representación interna para la negación.

### `Sin` y `Cos`

Representan funciones trigonométricas simbólicas:

    sin(x)
    cos(x)

Las funciones constructoras `crear_seno()` y `crear_coseno()` evalúan directamente los argumentos numéricos y crean objetos simbólicos cuando el argumento no es numérico.

### `Potencia`

Representa expresiones de la forma:

    base^exponente

Se utiliza, entre otras cosas, para representar productos como:

    sin(x) * sin(x)

como:

    sin(x)^2

## 3.3 Construcción inteligente de expresiones

Las operaciones simbólicas pasan por constructores como:

    crear_suma()
    crear_resta()
    crear_multiplicacion()
    crear_negativo()

Estos constructores realizan simplificaciones inmediatas cuando la estructura de la expresión lo permite.

Ejemplos:

    x + 0  → x
    0 + x  → x
    x - 0  → x
    x - x  → 0

    x * 0  → 0
    0 * x  → 0
    x * 1  → x
    1 * x  → x

También se realizan algunas simplificaciones trigonométricas especializadas.

## 3.4 Evaluación numérica

La función:

    evaluar(expresion, valores)

permite sustituir variables simbólicas por valores numéricos y reducir la expresión.

La clase `Matriz` utiliza esta función mediante:

    evaluar_numerico()

para producir una nueva matriz numérica a partir de una matriz simbólica.

## 3.5 Funciones auxiliares de operación

Debido a las particularidades del intérprete de la fx-CG50, se utilizan funciones auxiliares para realizar operaciones entre expresiones:

    suma()
    resta()
    producto()

La función interna `_combinar()` selecciona explícitamente el método apropiado cuando intervienen objetos simbólicos.

Esto permite reducir la dependencia del despacho automático de operadores.

## 3.6 Núcleo matricial

La clase `Matriz` almacena los datos como una lista de listas.

Ejemplo:

    Matriz([
        [1, 2],
        [3, 4]
    ])

Durante la construcción se comprueba que:

- los datos sean una lista;
- exista al menos una fila;
- cada fila sea una lista;
- exista al menos una columna;
- todas las filas tengan la misma longitud.

## 3.7 Operaciones matriciales

La clase `Matriz` implementa:

- suma;
- resta;
- multiplicación por escalar;
- multiplicación matricial;
- evaluación numérica;
- transposición;
- determinante hasta 3x3;
- presentación mediante `mostrar()`.

La multiplicación matricial se encuentra separada en:

    crear_multiplicacion_matriz()

Esto permite mantener el algoritmo matricial independiente de la lógica de expresiones simbólicas.

## 3.8 Multiplicación de matrices

El producto matricial utiliza la definición convencional:

    C[i,j] = Σ A[i,k] B[k,j]

Cada producto entre elementos se delega en `producto()` y cada suma acumulada en `suma()`.

Esto permite que la misma rutina funcione tanto con números como con expresiones simbólicas.

Se incluyen además optimizaciones simples para:

- matrices identidad;
- matrices cero.

## 3.9 Composición de productos

La función:

    Matriz.p_m(A, B, C, ...)

permite encadenar varios productos matriciales.

Conceptualmente:

    p_m(A, B, C)

representa:

    (A · B) · C

La multiplicación continúa siendo no conmutativa; el orden de las matrices es parte del resultado.

## 3.10 Transformaciones

El módulo `rot.py` utiliza `Matriz` y las funciones trigonométricas simbólicas del motor.

Las funciones implementadas son:

    Des.rotx(t)
    Des.rotx3(t)
    Des.roty(t)
    Des.roty3(t)
    Des.rotz(t)
    Des.rotz3(t)
    Des.trans(x, y, z)
    Des.Rot_RPY(phi, theta, psi)

Las funciones 4x4 representan transformaciones homogéneas. Las funciones 3x3 representan únicamente la parte rotacional.

## 3.11 Convención RPY

La función `Rot_RPY()` conserva exactamente la convención:

    R_RPY(phi, theta, psi) = Rz(phi) · Ry(theta) · Rx(psi)

La implementación realiza la composición mediante:

    Matriz.p_m(
        Des.rotz3(phi),
        Des.roty3(theta),
        Des.rotx3(psi)
    )

No debe intercambiarse el orden de estas matrices.

## 3.12 Presentación

En la versión 1.1 la presentación se separa del motor simbólico mediante el módulo:

    formato.py

Este módulo contiene únicamente la lógica necesaria para generar la representación compacta de las expresiones para la Casio.

Las funciones de formato son:

    _nombre_compacto()
    _agregar_nombre_simbolico()
    _recoger_nombres_simbolicos()
    crear_mapa_compacto()
    _compacto_parentesis_suma()
    _unir_productos_compactos()
    texto_compacto()

`syms.py` conserva la responsabilidad de representar y simplificar expresiones; no debe encargarse de decidir cómo se muestran en pantalla.

En la versión Casio se elimina el relleno utilizado para alinear columnas de diferente longitud. Una matriz se presenta con el menor espacio horizontal razonable, por ejemplo:

    [a,b,c]
    [d,e,f]

en lugar de agregar espacios para justificar las columnas.

La implementación evita `rjust()` para conservar compatibilidad con la fx-CG50.

## 3.13 Separación del experimento KhiCAS

El directorio:

    casio/Pruebas KhiCAS/

contiene pruebas experimentales independientes del núcleo.

Estas pruebas utilizan:

    import cas

para acceder al motor Xcas desde MicroPython 1.12 de KhiCAS.

La arquitectura de la versión 1.0 **no depende de esta integración**. Su finalidad es evaluar posteriormente si Xcas puede actuar como motor simbólico avanzado sin reemplazar necesariamente el núcleo propio.

## 3.14 Principio general de diseño

El núcleo debe permanecer pequeño y especializado en robótica.

Las funciones generales de un CAS no se implementarán únicamente por aumentar la cantidad de características. Una nueva función deberá justificar su utilidad dentro de la toolbox y mantener la compatibilidad con la plataforma.

## 3.15 Presentación adaptativa

La presentación de matrices se tratará como una capa independiente del motor simbólico. El formato completo (`nivel 0`) se conservará como primera opción porque mantiene la expresión matemática original.

Se ha definido provisionalmente un segundo formato (`nivel 1`) orientado a compactar la representación textual, principalmente mediante abreviaciones como:

    cos(x) -> c(x)
    sin(x) -> s(x)

La representación compacta no debe introducir variables auxiliares cuyo significado deba definirse fuera de la expresión.

La selección automática entre niveles todavía no tiene umbrales fijos. Antes de establecerlos se realizarán pruebas adicionales de crecimiento de cadenas y casos simbólicos. La evidencia experimental se documenta en `04_pruebas_presentacion.md`.
