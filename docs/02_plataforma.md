# 2. Plataforma objetivo

## 2.1 Hardware

La plataforma objetivo de la versión 1.1 es la calculadora **Casio fx-CG50**.

La implementación está diseñada para ejecutarse en el entorno Python disponible en la calculadora.

## 2.2 Entorno Python

El desarrollo principal de esta versión se realizó considerando la implementación de MicroPython proporcionada por la fx-CG50.

En el entorno Casio utilizado para el desarrollo se identificó **MicroPython 1.9.4**. La implementación de la calculadora no debe considerarse equivalente a una instalación completa de MicroPython: algunas funciones, métodos y comportamientos de Python pueden estar limitados o modificados.

Por esta razón, una característica se considera compatible con la toolbox únicamente después de comprobar su funcionamiento en la calculadora.

## 2.3 Compatibilidad observada

Durante el desarrollo se comprobaron, entre otras, las siguientes capacidades:

| Característica | Estado |
|---|---|
| `math` | Confirmada |
| Funciones definidas por el usuario | Confirmada |
| Clases | Confirmada |
| Listas | Confirmada |
| Listas anidadas | Confirmada |
| Cadenas de texto | Confirmada |
| Operaciones aritméticas básicas | Confirmada |
| Uso de objetos simbólicos propios | Confirmada |
| Matrices mediante listas de listas | Confirmada |

La toolbox evita depender de características que hayan mostrado incompatibilidad con la plataforma.

## 2.4 Limitaciones de operadores

Durante las pruebas se observó que la sobrecarga de determinados operadores sobre clases propias no siempre se comporta como en Python de PC.

En particular, la multiplicación mediante `*` presentó problemas de despacho automático para objetos propios, aunque la implementación de `__mul__()` puede ejecutarse mediante invocación directa.

Por ello, el núcleo utiliza funciones auxiliares como:

    suma()
    resta()
    producto()
    Matriz.p_m()

Estas funciones reducen la dependencia del despacho automático del intérprete.

La negación unaria también presentó limitaciones. Por ello se utiliza:

    n(expresion)

en lugar de depender exclusivamente de:

    -expresion

## 2.5 Representación de símbolos

La representación simbólica utiliza nombres ASCII, por ejemplo:

    x
    phi
    theta
    psi
    L1

Se evita depender de caracteres griegos directamente en el código debido a las limitaciones de representación observadas en la calculadora.

## 2.6 Ángulos

La convención interna de la toolbox es **radianes**.

Las funciones trigonométricas numéricas utilizan radianes y la función auxiliar `grados()` permite convertir explícitamente desde grados.

## 2.7 Presentación de matrices

En la versión 1.1, `Matriz.mostrar()` utiliza una presentación orientada a la pantalla de la fx-CG50 y evita la alineación artificial de columnas.

La versión Casio no agrega espacios de relleno para que columnas de distinta longitud tengan el mismo ancho. Esto evita consumir espacio horizontal únicamente por cuestiones estéticas y reduce desplazamientos innecesarios al consultar matrices grandes.

La implementación tampoco utiliza `str.rjust()`, ya que este método presentó incompatibilidad con el entorno de la fx-CG50.

## 2.8 Almacenamiento

Durante las pruebas se observó aproximadamente:

**16,264 KB de espacio libre**

Este valor corresponde al estado observado durante el desarrollo y puede variar según los archivos almacenados en la calculadora.

El tamaño de almacenamiento no constituye actualmente la principal limitación del proyecto. El rendimiento y la memoria utilizada durante la ejecución son consideraciones más importantes.

## 2.9 KhiCAS

Durante el desarrollo de la versión 1.0 también se probó la versión completa de KhiCAS para fx-CG50.

KhiCAS proporciona un entorno adicional con **MicroPython 1.12** y acceso al motor simbólico de Xcas mediante el módulo `cas`.

Se comprobó que:

    import cas

funciona en el entorno de MicroPython 1.12 de KhiCAS y que:

    cas.caseval(...)

permite enviar expresiones al motor Xcas.

También se comprobó la evaluación de matrices numéricas y simbólicas mediante este mecanismo.

Sin embargo, esta integración se mantiene experimental y separada del núcleo de la versión 1.0. El funcionamiento del toolbox principal no depende de KhiCAS.

## 2.10 Principio de compatibilidad

La plataforma real de referencia es la fx-CG50. El entorno de PC se utiliza principalmente para edición, organización y validación del código.

No se asumirá que una función disponible en Python de PC presenta exactamente el mismo comportamiento en la calculadora.

## 2.11 Pruebas de tamaño de salida

Se realizaron pruebas específicas sobre matrices simbólicas grandes para estudiar las limitaciones de presentación de la fx-CG50.

En una prueba con `T06` se observaron:

- elementos de hasta 180 caracteres;
- una fila de aproximadamente 589 caracteres que pudo ser construida en la representación utilizada durante esa prueba.

Posteriormente se realizó una prueba de frontera con filas de tamaño controlado:

- 509 caracteres: funcionó correctamente;
- la misma prueba de 509 caracteres se ejecutó cuatro veces consecutivas sin errores observables;
- 510 caracteres: produjo un fallo.

Esta frontera de 509/510 se considera evidencia experimental de la operación de construcción e impresión evaluada y no una medición directa de la memoria RAM total disponible.

En la versión 1.1 se modificó además el formato Casio para eliminar espacios de relleno. Por este cambio de representación, el valor de 509 caracteres se conserva como **referencia de diseño inicial** y deberá revalidarse como umbral de la nueva salida sin alineación antes de tratarlo como límite operativo definitivo.
