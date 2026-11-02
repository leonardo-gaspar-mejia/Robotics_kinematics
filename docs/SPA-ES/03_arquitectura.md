# 3. Arquitectura de la librería

## 3.1 Organización por módulos

La carpeta `casio/` contiene únicamente los módulos que forman la toolbox y el ejemplo de uso.

| Archivo | Responsabilidad | Elementos principales |
|---|---|---|
| `syms.py` | Árboles de expresiones, operaciones y simplificación simbólica | `Syms`, `Expresion`, `Sin`, `Cos`, `Potencia`, `evaluar()`, `simplificar()`, `suma()`, `resta()`, `producto()`, `n()` |
| `matriz.py` | Matrices numéricas/simbólicas y presentación coordinada | `Matriz`, `determinante()`, `p_m()`, `traspuesta()`, `simplificar_m()`, `evaluar_numerico()` |
| `formato.py` | Conversión de expresiones a texto compacto | `crear_mapa_compacto()`, `texto_compacto()` |
| `rot.py` | Rotaciones, transformaciones y extracción de parámetros | `Des.rotx*()`, `Des.roty*()`, `Des.rotz*()`, `Des.trans()`, `Des.Rot_RPY()`, `Des.Rot_lt()`, `Des.LT()`, `Des.RPY()`, `Des.DH()`, `Des.DH_table()`, `Des.H_inv()` |
| `derivadas.py` | Diferenciación simbólica mediante reglas seleccionadas | `Derivador` |
| `jacobiano.py` | Construcción del Jacobiano a partir de vectores columna | `Jacobiano()` |
| `ejemplo_uso.py` | Ejemplo de composición DH, transformación homogénea y Jacobiano | Script demostrativo |

Los imports entre módulos son directos (`from syms import ...`). Por ese motivo, los archivos `.py` de `casio/` deben permanecer juntos al copiarlos a la calculadora.

## 3.2 Motor simbólico

`syms.py` representa las expresiones como objetos, no como cadenas. `Syms` almacena el nombre interno de la variable y su representación visible. `Expresion` representa operaciones aritméticas y `Sin`, `Cos` y `Potencia` representan funciones y potencias.

Los constructores `crear_suma()`, `crear_resta()` y `crear_multiplicacion()` aplican simplificaciones inmediatas. La función `simplificar()` realiza un recorrido recursivo y repite el proceso hasta estabilizarse o alcanzar seis pasadas.

Las comparaciones de términos utilizan `_mismo_termino()` y recorren la estructura simbólica. Así, la igualdad matemática estructural no depende únicamente de que dos objetos produzcan la misma cadena al convertirse a texto.

La expansión distributiva está limitada por `MAX_TERMINOS_EXPANSION = 16`. Si expandir una multiplicación excedería ese límite, el producto se conserva sin distribuir.

## 3.3 Evaluación numérica

`evaluar(expresion, valores)` sustituye variables simbólicas usando un diccionario cuyas claves son los nombres internos de `Syms`. Los argumentos de seno y coseno se interpretan en radianes.

`Matriz.evaluar_numerico(valores)` aplica esa evaluación a los elementos y devuelve una matriz numérica nueva.

## 3.4 Núcleo matricial

`Matriz` almacena sus datos como una lista de listas. El constructor valida que haya al menos una fila y una columna y que todas las filas tengan la misma longitud.

Las operaciones disponibles incluyen suma, resta, producto matricial, multiplicación por escalar, igualdad estructural, trasposición y simplificación en una matriz nueva. `Matriz.p_m(A, B, C, ...)` compone productos respetando el orden de los factores.

### Determinante

`Matriz.determinante()` exige una matriz cuadrada no vacía. Utiliza resultados directos para 1×1 y 2×2 y expansión recursiva por cofactores para órdenes mayores. Antes de expandir, busca entre filas y columnas una línea con más ceros exactos.

Este método admite matrices cuadradas de orden N, pero su coste puede crecer factorialmente para matrices densas. La búsqueda de ceros es exacta: expresiones simbólicas que equivalgan a cero pero no estén simplificadas podrían no contarse como ceros.

## 3.5 Derivación simbólica

`Derivador(expresion).derivar(variable)` admite una variable `Syms`. Las reglas implementadas son:

- constantes y variables;
- suma y resta;
- producto;
- seno y coseno;
- potencia con exponente numérico constante;
- negación.

La recursividad aplica la regla de la cadena a argumentos compuestos formados por esos tipos. No están implementadas reglas de cociente, potencias de exponente simbólico ni funciones como logaritmo, exponencial o tangente.

## 3.6 Jacobiano

`Jacobiano(funciones, variables)` requiere dos objetos `Matriz` que representen vectores columna. Para `m` funciones y `n` variables devuelve una matriz de `m × n`; cada elemento corresponde a la derivada parcial de una función respecto a una variable.

## 3.7 Transformaciones

`rot.py` agrupa las operaciones geométricas dentro de `Des`:

- `rotx`, `roty`, `rotz`: rotaciones homogéneas 4×4.
- `rotx3`, `roty3`, `rotz3`: rotaciones 3×3.
- `trans(x, y, z)`: traslación homogénea.
- `Rot_RPY(phi, theta, psi)`: composición `Rz(phi) · Ry(theta) · Rx(psi)`, conservando la convención y el orden de parámetros de la toolbox de referencia del Dr. César Chávez.
- `Rot_lt(lx, ly, lz, theta)`: matriz de rotación mediante eje y ángulo.
- `LT(H)`: extracción numérica de eje y ángulo de una transformación/rotación.
- `RPY(H)`: extracción numérica que devuelve la terna `(Roll, Pitch, Yaw)` según la nomenclatura y el orden de la toolbox de referencia, incluyendo un caso especial de bloqueo de cardán.
- `RPY_grados(H)`: la misma extracción, con los tres valores convertidos a grados; también devuelve la terna.
- `DH(theta, d, a, alpha)`: transformación Denavit–Hartenberg.
- `DH_table(tabla)`: composición de filas DH; la tabla debe tener cuatro columnas.
- `H_inv(H)`: inversa de una transformación rígida homogénea.
- `nsad()`: plantilla simbólica para una matriz homogénea con los vectores n, s, a y d.

`H_inv()` utiliza la transpuesta de la submatriz rotacional y `-Rᵀd`; presupone una transformación rígida con rotación ortonormal. No es una inversa general de cualquier matriz 4×4.

## 3.8 Presentación

`formato.py` está separado del motor simbólico. `texto_compacto()` genera una salida más corta mediante abreviaciones de seno/coseno y nombres simbólicos, protegiendo las abreviaciones ambiguas. También conserva paréntesis cuando una base o exponente compuesto de una potencia lo requiere.

`Matriz.mostrar()` mide cada fila de la salida completa. Si alguna supera `MAX_FILA_NIVEL0`, genera la representación compacta y presenta el Nivel 1. El umbral es un parámetro de presentación, no una garantía de que cualquier expresión pueda mostrarse sin error.

## 3.9 Separación de pruebas y exploraciones

- `testInCasio/` contiene scripts que se copian a la calculadora para validar las operaciones esenciales.
- `tests/` contiene pruebas automáticas para PC con `pytest`.
- `.github/workflows/tests.yml` automatiza la ejecución de las pruebas de PC.

KhiCAS/Xcas se ha estudiado como posible motor externo, pero no existe un backend integrado en esta versión. La toolbox no importa el módulo `cas`.
