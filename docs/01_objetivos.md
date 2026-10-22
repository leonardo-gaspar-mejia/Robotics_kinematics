# 1. Objetivos del proyecto

## 1.1 Objetivo general

Desarrollar una toolbox ligera de matemáticas y robótica para la calculadora Casio fx-CG50, orientada principalmente al álgebra matricial, las transformaciones espaciales y la representación simbólica necesaria en problemas de robótica.

La versión 1.1 mantiene una implementación pequeña, clara y compatible con las limitaciones reales de la plataforma, evitando convertir el proyecto en un sistema CAS general.

## 1.2 Objetivos específicos

### Álgebra matricial

Implementar una estructura `Matriz` capaz de almacenar matrices numéricas y matrices cuyos elementos sean expresiones simbólicas.

La versión 1.1 mantiene como base:

- creación y validación de matrices;
- acceso a elementos;
- suma y resta;
- multiplicación por escalar;
- multiplicación matricial;
- transposición;
- determinante para matrices hasta 3x3;
- evaluación numérica de matrices simbólicas;
- composición de múltiples productos mediante `p_m()`.

### Transformaciones

Implementar rotaciones alrededor de los ejes X, Y y Z, tanto en representación homogénea 4x4 como en representación rotacional 3x3.

También se incluye la traslación homogénea en X, Y y Z.

### Transformaciones homogéneas

Permitir la construcción y composición de transformaciones homogéneas mediante objetos `Matriz`.

### Representación RPY

Implementar la representación Roll-Pitch-Yaw utilizada por la toolbox de referencia.

La convención adoptada es:

    R_RPY(phi, theta, psi) = Rz(phi) · Ry(theta) · Rx(psi)

Esta convención forma parte de la especificación del proyecto y no debe modificarse al ampliar o optimizar la implementación.

### Operaciones simbólicas

Desarrollar un motor simbólico ligero especializado en las expresiones que aparecen en robótica.

La versión 1.1 permite trabajar con:

- variables simbólicas;
- expresiones aritméticas;
- suma;
- resta;
- multiplicación;
- seno y coseno;
- potencias;
- negación;
- simplificación algebraica y trigonométrica básica;
- evaluación numérica mediante sustitución de valores.

## 1.3 Convención angular

La toolbox utiliza **radianes como unidad angular predeterminada**.

Cuando sea necesario introducir un ángulo expresado en grados puede utilizarse:

    grados(valor)

Por ejemplo:

    grados(45)

convierte 45 grados a radianes.

La función `radianes_a_grados()` permite realizar la conversión inversa y `mostrar_deg()` permite mostrar un valor numérico expresado en radianes como grados.

## 1.4 Principios de diseño

La versión 1.1 mantiene:

- bajo consumo de recursos;
- compatibilidad con la fx-CG50;
- código comprensible;
- modularidad;
- reutilización del núcleo matemático;
- comportamiento determinista;
- separación entre expresiones simbólicas, matrices y transformaciones;
- evitar dependencias innecesarias.

## 1.5 Fuera del alcance de la versión 1.1

La toolbox no pretende ser un CAS general. Quedan fuera del alcance de esta versión:

- integración simbólica general;
- derivación simbólica general;
- resolución general de ecuaciones;
- factorización general;
- expansión algebraica general;
- límites simbólicos;
- optimización simbólica avanzada;
- un sistema general de álgebra computacional.

Estas capacidades podrían delegarse o estudiarse posteriormente mediante un motor externo como Xcas/KhiCAS, pero **no forman parte del núcleo de la versión 1.0**.

## 1.6 Alcance de la versión 1.1

La versión 1.1 parte del núcleo funcional de la versión 1.0 y comprende:

- motor simbólico ligero;
- operaciones simbólicas básicas;
- funciones trigonométricas `sin` y `cos`;
- evaluación numérica;
- matrices;
- determinante hasta 3x3;
- rotaciones Rx, Ry y Rz;
- rotaciones 3x3;
- traslaciones homogéneas;
- transformaciones homogéneas;
- composición de transformaciones;
- RPY con la convención `Rz(phi) · Ry(theta) · Rx(psi)`;
- presentación adaptativa de matrices mediante dos niveles de representación, orientada a las limitaciones observadas en la fx-CG50.

La integración con KhiCAS se mantiene como **línea experimental independiente** y no modifica el núcleo de esta versión.


## 1.7 Cambios principales de la versión 1.1

La versión 1.1 mantiene el motor matemático de la versión anterior y concentra los cambios principales en la presentación de expresiones simbólicas en la Casio fx-CG50.

Los cambios de esta versión son:

- separación de la lógica de formato en el módulo `formato.py`;
- presentación de matrices sin espacios de relleno ni alineación artificial de columnas en la versión Casio;
- selección automática entre dos niveles de representación;
- Nivel 0: expresión simbólica completa;
- Nivel 1: representación compacta de la expresión;
- uso de abreviaciones autocontenidas como `c(x)` y `s(x)` en lugar de variables auxiliares externas;
- caracterización experimental del límite de longitud de fila y registro de la frontera 509/510 como referencia experimental.

La versión 1.1 no incorpora un tercer nivel de compactación. Su desarrollo se mantendrá guiado por pruebas reales en la calculadora y por las necesidades de uso en robótica.
