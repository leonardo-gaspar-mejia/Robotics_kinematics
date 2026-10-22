# 4. Pruebas de presentación y límites observados

## 4.1 Objetivo

Estas pruebas buscan caracterizar el comportamiento real de la Casio fx-CG50 al convertir expresiones simbólicas a texto y al construir filas completas de una matriz.

La finalidad es obtener evidencia experimental que permita diseñar la presentación adaptativa de `Matriz.mostrar()` sin asumir que la longitud de una cadena equivale directamente a la memoria RAM disponible.

---

## 4.2 Criterio experimental

La plataforma no ofrece en el entorno utilizado una medición directa de memoria disponible mediante `gc`, por lo que no se utiliza `gc.mem_free()` como parte del sistema de decisión.

La caracterización se realiza mediante:

- cantidad de caracteres de cada elemento;
- cantidad de caracteres de una fila;
- capacidad de `str()` para convertir el elemento en texto;
- capacidad de construir la fila completa;
- repetición de la prueba;
- detección de `MemoryError` cuando aparece.

Una longitud determinada de texto no debe interpretarse automáticamente como un número de bytes de memoria.

---

## 4.3 Evidencia inicial con `T06`

Durante una prueba con la transformación homogénea simbólica `T06` se obtuvieron los siguientes valores destacados:

| Medición | Valor observado |
|---|---:|
| Elemento de mayor longitud observado | 180 caracteres |
| Elementos destacados | `T06[0,3]` y `T06[1,3]` |
| Fila de mayor longitud observada | 589 caracteres |
| Fila destacada | fila 2 de 4 |

Estas expresiones pudieron ser convertidas a texto y la fila correspondiente pudo ser construida sin producir `MemoryError` en esa prueba.

Estos datos corresponden a la representación utilizada durante la prueba inicial y constituyen evidencia de funcionamiento, no un límite absoluto.

---

## 4.4 Prueba de elementos

El siguiente código permite medir la longitud de cada elemento y detectar un posible `MemoryError` durante `str()`.

```python
def medir_elementos(M):
    print("")
    print("===== MEDICION ELEMENTOS =====")

    for i in range(M.filas):
        for j in range(M.columnas):
            try:
                texto = str(M[i,j])
                print("")
                print("Elemento [" + str(i) + "," + str(j) + "]")
                print("Caracteres:", len(texto))
                texto = None
            except MemoryError:
                print("")
                print("Elemento [" + str(i) + "," + str(j) + "]")
                print("MEMORY ERROR")
```

---

## 4.5 Prueba de filas

La siguiente prueba reproduce el problema de construir una fila completa antes de imprimirla.

```python
def medir_filas(M):
    print("")
    print("===== MEDICION FILAS =====")

    for i in range(M.filas):
        try:
            fila = "["

            for j in range(M.columnas):
                fila = fila + " " + str(M[i,j])

                if j < M.columnas - 1:
                    fila = fila + " ,"

            fila = fila + " ]"

            print("")
            print("Fila:", i)
            print("Caracteres:", len(fila))
            fila = None

        except MemoryError:
            print("")
            print("Fila:", i)
            print("MEMORY ERROR")
```

Esta prueba conserva el formato utilizado durante la caracterización inicial. No debe confundirse con el formato final sin espacios de la versión 1.1.

---

## 4.6 Prueba de crecimiento de cadenas

Para separar el comportamiento de las expresiones simbólicas del tamaño bruto de una cadena, se puede utilizar:

```python
def probar_longitud(n, imprimir=True):
    try:
        texto = ""

        for i in range(n):
            texto = texto + "x"

        print("OK:", n)

        if imprimir:
            print(texto)

        texto = None

    except MemoryError:
        print("ERROR:", n)
```

El objetivo es observar empíricamente el comportamiento al aumentar progresivamente el número de caracteres.

---

## 4.7 Frontera experimental de 509/510 caracteres

Se realizó posteriormente una prueba de frontera con una fila de longitud controlada.

Los resultados fueron:

| Longitud de fila | Resultado |
|---:|---|
| 509 | Funcionó |
| 509, repetido 4 veces | Funcionó sin errores observables |
| 510 | Se produjo un fallo |

Además, los cálculos de las matrices utilizadas para generar la fila se realizaron correctamente.

Por ello:

**509 caracteres por fila = límite experimental comprobado para la representación evaluada en esa prueba.**

**510 caracteres por fila = primer punto de fallo observado en esa prueba.**

Este resultado no debe interpretarse como el límite absoluto de memoria RAM de la Casio fx-CG50.

---

## 4.8 Cambio de representación en la versión 1.1

Después de la caracterización anterior se modificó la representación de matrices para la versión Casio.

La salida dejó de utilizar espacios de relleno para alinear columnas de diferente longitud.

Antes:

```text
[ expresion_larga , expresion_corta        , expresion ]
[ expresion       , otra_expresion_larga   , x         ]
```

En la versión 1.1:

```text
[expresion_larga,expresion_corta,expresion]
[expresion,otra_expresion_larga,x]
```

El objetivo es reducir el ancho horizontal y evitar desplazamientos innecesarios provocados únicamente por alineación estética.

### Consecuencia

El límite de 509 caracteres se conserva en la documentación como **referencia experimental de la caracterización anterior**.

Debido al cambio de representación, la frontera 509/510 debe volver a comprobarse directamente con el formato final de la versión 1.1 antes de considerarla el umbral operativo definitivo de `Matriz.mostrar()`.

---

## 4.9 Arquitectura de presentación de la versión 1.1

La versión 1.1 utiliza dos niveles:

### Nivel 0 — representación completa

Se mantiene la expresión matemática completa.

Ejemplo:

```text
cos(theta4 + theta5)
```

Este es el formato preferido siempre que resulte viable.

### Nivel 1 — representación compacta

Se reduce la longitud textual sin introducir definiciones externas.

Ejemplos:

```text
cos(x) -> c(x)
sin(x) -> s(x)
```

y:

```text
cos(theta1 + theta5) * sin(theta5)
```

puede representarse como:

```text
c(t1+t5)s(t5)
```

La expresión sigue siendo autocontenida.

---

## 4.10 Separación del formato

La lógica para compactar expresiones se mueve fuera de `syms.py` y se concentra en:

```text
formato.py
```

Las funciones de formato son:

```text
_nombre_compacto()
_agregar_nombre_simbolico()
_recoger_nombres_simbolicos()
crear_mapa_compacto()
_compacto_parentesis_suma()
_unir_productos_compactos()
texto_compacto()
```

`syms.py` conserva el motor simbólico y no decide cómo se presenta una expresión en pantalla.

`matriz.py` decide qué nivel utilizar.

---

## 4.11 Criterio de selección

La estrategia de presentación es:

```text
Matriz.mostrar()
      |
      v
Construir representación Nivel 0
      |
      v
Medir cada fila
      |
      +---- dentro del umbral ----> Nivel 0
      |
      +---- supera el umbral -----> Nivel 1
```

El Nivel 1 no introduce variables auxiliares como `c45` y `s45`.

Se prefieren formas autocontenidas como:

```text
c(t4+t5)
s(t4+t5)
```

La compactación debe evitar abreviaciones ambiguas.

---

## 4.12 Estado actual

La versión 1.1 establece como decisiones de arquitectura:

- presentación separada del motor simbólico;
- ausencia de espacios de relleno en la salida Casio;
- dos niveles de presentación;
- compactación mediante `c(...)` y `s(...)`;
- mantenimiento de la información dentro de la propia expresión;
- selección automática entre Nivel 0 y Nivel 1;
- ausencia de un Nivel 2.

El valor de 509 caracteres se mantiene como referencia experimental hasta repetir la prueba con el formato sin alineación.

---

## 4.13 Conclusión de la etapa

La principal dificultad técnica de presentación identificada durante el desarrollo fue aislada del motor simbólico y trasladada a una capa específica de formato.

Esto permite que:

```text
syms.py
```

se concentre en la representación y simplificación matemática,

mientras que:

```text
formato.py
```

se concentre en la representación textual,

y:

```text
matriz.py
```

decida qué nivel de presentación utilizar.

Esta separación constituye uno de los cambios principales de la versión 1.1.
