# 1. Objetivos y alcance

## 1.1 Objetivo general

Desarrollar una toolbox ligera de matemáticas y robótica para la Casio fx-CG50, orientada al álgebra matricial, las transformaciones espaciales y las operaciones simbólicas necesarias para estudiar manipuladores robóticos.

La versión 1.2 amplía el núcleo con derivación simbólica limitada, construcción del Jacobiano y herramientas para transformaciones Denavit–Hartenberg, conservando como prioridad la compatibilidad con la calculadora.

## 1.2 Objetivos específicos

### Álgebra matricial

Implementar `Matriz` para almacenar datos numéricos y expresiones simbólicas. La clase proporciona:

- construcción y validación de matrices;
- suma y resta;
- producto matricial y composición de productos;
- multiplicación por escalar;
- transposición;
- comparación estructural;
- simplificación en una matriz nueva;
- evaluación numérica;
- determinante de matrices cuadradas de orden N.

El determinante se calcula mediante expansión recursiva por cofactores. Se utilizan casos directos para 1×1 y 2×2 y se selecciona una fila o columna que contenga el mayor número de ceros explícitos. El algoritmo puede resultar costoso en matrices densas grandes.

### Motor simbólico

Representar expresiones mediante objetos y no únicamente mediante cadenas de texto. El núcleo contempla variables, suma, resta, multiplicación, negación, seno, coseno y potencias, además de simplificaciones algebraicas y trigonométricas especializadas.

La expansión distributiva tiene un límite de 16 términos para contener el crecimiento de las expresiones. La simplificación recursiva está limitada a seis pasadas como máximo.

### Derivación simbólica

La clase `Derivador` implementa reglas para:

- constantes y variables;
- suma y resta;
- producto;
- seno y coseno;
- potencias cuyo exponente sea constante.

La derivación es recursiva, por lo que aplica la regla de la cadena cuando la expresión está formada por las estructuras soportadas. No implementa cocientes, exponentes variables ni un conjunto general de funciones matemáticas.

### Jacobiano

La función `Jacobiano(funciones, variables)` construye la matriz de derivadas parciales. Ambos argumentos deben ser vectores columna `Matriz`. Si hay `m` funciones y `n` variables, el resultado tiene dimensiones `m × n`.

### Cinemática y transformaciones

Proporcionar rotaciones, traslaciones y transformaciones homogéneas; composición de matrices; representación RPY; construcción de matrices Denavit–Hartenberg; composición de una tabla DH e inversa de una transformación rígida homogénea.

## 1.3 Convención angular

La unidad angular predeterminada es el radián. `grados(valor)` convierte grados a radianes; `radianes_a_grados(valor)` realiza la conversión inversa. Las funciones trigonométricas numéricas utilizan radianes.

La convención RPY adoptada es:

    R_RPY(phi, theta, psi) = Rz(phi) · Ry(theta) · Rx(psi)

Se conserva la convención, la nomenclatura y el orden de parámetros de la toolbox de referencia del Dr. César Chávez. La pareja de funciones `Rot_RPY()` y `RPY()` mantiene su correspondencia original; no se intercambian ni reinterpretan los nombres de los ángulos.

## 1.4 Principios de diseño

- Priorizar compatibilidad real con la fx-CG50.
- Mantener el núcleo pequeño y especializado en robótica.
- Separar motor simbólico, matrices, transformaciones y presentación.
- Evitar dependencias externas en el código que se copia a la calculadora.
- Utilizar pruebas ejecutables en la calculadora y pruebas automáticas en PC.
- Documentar las limitaciones de rendimiento y de las reglas simbólicas.

## 1.5 Fuera del alcance

La versión 1.2 no pretende ofrecer un CAS general. No incluye, entre otras capacidades:

- integración simbólica general;
- solución general de ecuaciones o sistemas;
- factorización polinómica general;
- límites simbólicos;
- derivación de cualquier función matemática;
- inversión general de matrices de cualquier tamaño;
- optimización simbólica avanzada.

KhiCAS/Xcas se ha explorado como posible motor externo, pero no forma parte de las dependencias ni del flujo del núcleo 1.2.

## 1.6 Validación

La batería `testInCasio/` contiene 24 grupos de comprobaciones manuales que el autor confirmó en la fx-CG50. La carpeta `tests/` contiene 62 pruebas automáticas ejecutadas en Python de PC mediante `pytest`. Estas dos baterías tienen objetivos distintos y ninguna sustituye a la otra.
