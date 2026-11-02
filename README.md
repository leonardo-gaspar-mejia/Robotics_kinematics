# Casio Robotics Toolbox

**Versión 1.2**  
**Plataforma objetivo: Casio fx-CG50**

[Español](#español) | [English](#english)

---

## Español

**Versión 1.2**  
**Plataforma objetivo: Casio fx-CG50**

[Documentación técnica en español](docs/README.md) | [Technical documentation in English](docs/en/README.md) | [Historial de cambios / Changelog](CHANGELOG.md)

Toolbox ligera de matemáticas y robótica desarrollada para la **Casio fx-CG50**, inspirada en la toolbox utilizada en la enseñanza de robótica por el Dr. César Chávez.

Su propósito es reunir operaciones matemáticas y herramientas de cálculo utilizadas en el estudio de manipuladores robóticos, manteniendo una implementación modular y adecuada a los recursos y particularidades del entorno Python de la calculadora.

> **Nota de compatibilidad:** el desarrollo y la validación funcional de esta toolbox están enfocados en la **Casio fx-CG50**. Una función se considera comprobada en la calculadora únicamente cuando se ha ejecutado en el hardware real. Las pruebas automáticas realizadas en PC ayudan a detectar errores y regresiones, pero no sustituyen las pruebas en la fx-CG50 ni garantizan compatibilidad con otras calculadoras, implementaciones de MicroPython o versiones de Python.

## Contacto

Correo para sugerencia, dudas, bugs, etc.
**Email**: leogasmejob@gmail.com

## Objetivo

Proporcionar una herramienta compacta para realizar operaciones matemáticas utilizadas en robótica, especialmente:

- álgebra matricial numérica y simbólica;
- representación y manipulación de expresiones simbólicas;
- derivación simbólica especializada;
- construcción de Jacobianos;
- rotaciones y traslaciones espaciales;
- transformaciones homogéneas;
- parámetros y tablas de Denavit-Hartenberg (DH);
- representaciones RPY y eje-ángulo;
- evaluación numérica de expresiones y matrices;
- presentación de resultados adaptada a la pantalla de la calculadora.

La toolbox está especializada en las operaciones necesarias para estudiar y trabajar con manipuladores robóticos. **No pretende ser un sistema de álgebra computacional (CAS) general.**

## Funcionalidades de la versión 1.2

### Motor simbólico

El módulo `syms.py` proporciona una estructura ligera para representar y operar con expresiones simbólicas.

Incluye:

- variables simbólicas mediante `Syms`;
- expresiones algebraicas mediante `Expresion`;
- funciones trigonométricas simbólicas `Sin` y `Cos`;
- potencias mediante `Potencia`;
- suma, resta, multiplicación y negación;
- simplificaciones algebraicas y trigonométricas especializadas;
- evaluación numérica mediante sustitución de variables;
- conversión entre grados y radianes.

Las funciones auxiliares `suma()`, `resta()` y `producto()` permiten controlar las operaciones entre objetos numéricos, simbólicos y matriciales. En particular, se recomienda utilizar `producto()` para las multiplicaciones por escalares en la fx-CG50, en lugar de depender directamente de la sobrecarga del operador `*`.

### Álgebra matricial

El módulo `matriz.py` implementa la clase `Matriz`, que permite trabajar con matrices numéricas y simbólicas.

Incluye:

- construcción y validación de matrices;
- acceso a elementos;
- suma y resta;
- multiplicación por escalares;
- multiplicación matricial;
- composición de productos mediante `Matriz.p_m()`;
- transposición;
- cálculo de determinantes de matrices cuadradas de orden N mediante expansión recursiva por cofactores;
- simplificación de matrices simbólicas mediante `simplificar_m()`;
- evaluación numérica mediante `evaluar_numerico()`;
- presentación de matrices mediante `mostrar()`.

El método de determinantes es general para matrices cuadradas, pero la expansión por cofactores puede crecer rápidamente en matrices grandes. Su disponibilidad no implica que sea conveniente calcular determinantes de orden elevado en la calculadora.

### Transformaciones y cinemática

El módulo `rot.py`, mediante la clase `Des`, reúne funciones para construir y manipular transformaciones espaciales.

Incluye:

- rotaciones alrededor de X, Y y Z en matrices homogéneas 4×4;
- matrices de rotación 3×3;
- traslaciones homogéneas;
- composición Roll-Pitch-Yaw (RPY);
- representación eje-ángulo;
- extracción de eje-ángulo a partir de una transformación;
- extracción de ángulos RPY;
- construcción de matrices de Denavit-Hartenberg mediante `Des.DH()`;
- composición de tablas DH mediante `Des.DH_table()`;
- cálculo de la inversa de una transformación homogénea mediante `Des.H_inv()`.

La convención RPY implementada es:

\[
R_{RPY}(\phi,\theta,\psi)=R_z(\phi)R_y(\theta)R_x(\psi)
\]

El orden de composición forma parte de la definición de la función y no debe intercambiarse.

### Derivación simbólica y Jacobiano

El módulo `derivadas.py` contiene la clase `Derivador`, que implementa reglas de derivación para las expresiones soportadas por el motor simbólico.

Actualmente contempla:

- constantes y variables;
- suma y resta;
- producto;
- seno y coseno;
- potencias con exponente constante;
- regla de la cadena para las funciones trigonométricas soportadas.

No es un derivador simbólico general: por ejemplo, las potencias con exponentes simbólicos no están admitidas por la implementación actual.

El módulo `jacobiano.py` proporciona `Jacobiano(funciones, variables)`, que construye la matriz Jacobiana a partir de un vector columna de funciones y un vector columna de variables.

### Presentación de matrices

El módulo `formato.py` separa la representación compacta del motor simbólico y permite que `Matriz.mostrar()` seleccione entre dos niveles de presentación:

- **Nivel 0:** expresión simbólica completa.
- **Nivel 1:** expresión compacta, con abreviaciones para funciones trigonométricas y nombres simbólicos cuando corresponde.

La presentación está orientada a aprovechar el espacio horizontal de la pantalla de la fx-CG50 y evita la alineación artificial de columnas mediante espacios de relleno.

## Convención angular

Los ángulos se interpretan en **radianes** por defecto. Esto aplica a las funciones trigonométricas y a las funciones de rotación que reciben ángulos.

Para convertir grados a radianes:

```python
from syms import grados

angulo = grados(45)
```

También se dispone de funciones para convertir de radianes a grados y para utilizar las variantes que reciben grados, cuando están implementadas.

## Ejemplo de uso

Los módulos de la toolbox se encuentran dentro de `casio/`. Para ejecutar el ejemplo en la fx-CG50, copia los módulos necesarios al entorno de la calculadora y conserva las importaciones relativas a esa ubicación.

Ejemplo básico de construcción de una rotación y una transformación DH:

```python
from syms import Syms, grados
from rot import Des

# Variable articular simbólica
theta = Syms("theta")

# Rotación alrededor del eje Z (3x3)
Rz = Des.rotz3(theta)
Rz.mostrar()

# Transformación DH con theta = 45 grados,
# d = 0, a = 2 y alpha = 0
T = Des.DH(grados(45), 0, 2, 0)
T.mostrar()
```

Para consultar un ejemplo más amplio que utiliza tablas DH, transformaciones homogéneas, inversas y Jacobianos, revisa `casio/ejemplo_uso.py`.

## Plataforma y compatibilidad

La plataforma objetivo es la **Casio fx-CG50**, utilizando el entorno Python proporcionado por la calculadora. Durante el desarrollo se trabajó con el entorno basado en MicroPython 1.9.4.

La implementación de Python de la calculadora tiene diferencias y limitaciones respecto a una instalación convencional de Python. Por ello, el código evita depender de algunas características que no se comportan de la misma manera en la fx-CG50 y utiliza funciones auxiliares para ciertas operaciones simbólicas y matriciales.

El proyecto también incluye pruebas automáticas que pueden ejecutarse en una computadora con Python y `pytest`. Estas pruebas son útiles para revisar el comportamiento del código y detectar regresiones durante el desarrollo; sin embargo, **una prueba aprobada en PC no demuestra por sí sola que el mismo comportamiento esté validado en la calculadora**.

Los detalles del entorno, las limitaciones identificadas y el alcance de las comprobaciones se describen en `docs/02_plataforma.md`. Las traducciones al inglés están disponibles en `docs/en/`.

## Pruebas

El repositorio separa las pruebas destinadas a la calculadora de las pruebas automáticas para PC.

### Pruebas en la Casio fx-CG50

La carpeta `testInCasio/` contiene los scripts destinados a ejecutarse directamente en la calculadora. `pruebasInCasio.py` reúne la batería de regresión y `pruebas_presentacion.py` contiene herramientas de diagnóstico manual. No requieren `pytest` ni bibliotecas externas. Copia los módulos de `casio/` junto con el script que vayas a ejecutar y utiliza el entorno Python de la fx-CG50.

### Pruebas automáticas en PC

La carpeta `tests/` contiene las pruebas automatizadas con `pytest`. Desde la raíz del repositorio, instala las dependencias de desarrollo y ejecuta:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

La guía de `tests/README.md` contiene instrucciones adicionales para ejecutar pruebas específicas y ampliar la suite. Su traducción está disponible en `tests/README_EN.md`. El script `testInCasio/pruebas_presentacion.py` es una herramienta de diagnóstico manual; no forma parte de las pruebas automatizadas de `pytest`.

## Estructura del proyecto

```text
Robotics_Toolbox_Casio/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── casio/
│   ├── derivadas.py
│   ├── ejemplo_uso.py
│   ├── formato.py
│   ├── jacobiano.py
│   ├── matriz.py
│   ├── rot.py
│   └── syms.py
│
├── docs/
│   ├── README.md
│   ├── 01_objetivos.md
│   ├── 02_plataforma.md
│   ├── 03_arquitectura.md
│   ├── 04_pruebas_presentacion.md
│   ├── VERSION.md
│   └── en/
│       ├── 01_objectives_and_scope.md
│       ├── 02_platform_and_compatibility.md
│       ├── 03_library_architecture.md
│       ├── 04_presentation_tests_and_observed_limits.md
│       ├── README.md
│       └── VERSION.md
│
├── testInCasio/
│   ├── pruebasInCasio.py
│   └── pruebas_presentacion.py
│
├── tests/
│   ├── README.md
│   ├── README_EN.md
│   ├── conftest.py
│   ├── test_derivadas.py
│   ├── test_formato.py
│   ├── test_integracion.py
│   ├── test_jacobiano.py
│   ├── test_matriz.py
│   ├── test_rot.py
│   └── test_syms.py
│
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── pytest.ini
├── README.md
└── requirements-dev.txt
```

La carpeta `.git/` no se incluye en el árbol porque contiene metadatos locales del repositorio y Git la administra automáticamente.

## KhiCAS

Durante el desarrollo se realizaron pruebas independientes con **KhiCAS para fx-CG50**. Su entorno MicroPython 1.12 proporciona acceso al motor Xcas mediante el módulo `cas` y la función `cas.caseval()`.

Esta exploración se mantiene separada del núcleo de la toolbox. La versión actual no depende de KhiCAS para sus operaciones y no debe considerarse que existe una integración estable entre ambos motores. La posible utilización de Xcas como backend simbólico avanzado queda como una línea de trabajo experimental.

## Filosofía del proyecto

La toolbox busca ser:

- ligera y adecuada a los recursos de la calculadora;
- clara y comprensible;
- modular;
- especializada en matemáticas aplicadas a robótica;
- verificable mediante pruebas en el hardware objetivo;
- extensible sin convertir el núcleo en un CAS general.

Se priorizan las operaciones necesarias para el estudio de manipuladores robóticos y se evita incorporar complejidad cuando una solución específica y ligera es suficiente.

## Documentación adicional

- `docs/01_objetivos.md`: objetivos y alcance del proyecto.
- `docs/02_plataforma.md`: plataforma objetivo, compatibilidad y limitaciones observadas.
- `docs/03_arquitectura.md`: organización interna y responsabilidades de los módulos.
- `docs/04_pruebas_presentacion.md`: pruebas y criterios de presentación matricial.
- `docs/VERSION.md`: información de la versión documentada.
- `CHANGELOG.md`: historial de cambios entre versiones.

## Estado del proyecto

**Versión 1.2 — núcleo de robótica en desarrollo y validación sobre Casio fx-CG50.**

La versión 1.2 amplía el núcleo inicial con herramientas de derivación simbólica, construcción de Jacobianos y operaciones de cinemática mediante transformaciones DH. La evolución del proyecto continuará guiándose por las necesidades de uso en robótica y por las pruebas realizadas en la calculadora.

---

## English

**Version 1.2**  
**Target platform: Casio fx-CG50**

[Technical documentation in English](docs/en/README.md) | [Spanish technical documentation](docs/README.md) | [Changelog](CHANGELOG.md)

A lightweight mathematics and robotics toolbox developed for the **Casio fx-CG50**, inspired by the robotics toolbox used in teaching by Dr. César Chávez.

Its purpose is to bring together mathematical operations and calculation tools used in the study of robotic manipulators, with a modular implementation designed around the resources and characteristics of the calculator's Python environment.

> **Compatibility notice:** Development and functional validation are focused on the **Casio fx-CG50**. A feature is considered validated on the calculator only after it has been executed on the actual hardware. Automated tests on a PC help detect errors and regressions, but they do not replace tests on the fx-CG50 or guarantee compatibility with other calculators, MicroPython implementations, or Python versions.

## Contact

For questions, suggestions, or bug reports:  
**Email:** leogasmejob@gmail.com

## Project goal

Provide a compact tool for mathematical operations used in robotics, especially:

- numerical and symbolic matrix algebra;
- representation and manipulation of symbolic expressions;
- specialized symbolic differentiation;
- Jacobian construction;
- spatial rotations and translations;
- homogeneous transformations;
- Denavit–Hartenberg (DH) parameters and tables;
- RPY and axis-angle representations;
- numerical evaluation of expressions and matrices;
- result formatting adapted to the calculator's display.

The toolbox focuses on operations needed to study and work with robotic manipulators. **It is not intended to be a general-purpose computer algebra system (CAS).**

## Features in version 1.2

### Symbolic engine

The `syms.py` module provides a lightweight structure for representing and operating on symbolic expressions.

It includes:

- symbolic variables through `Syms`;
- algebraic expressions through `Expresion`;
- symbolic trigonometric functions `Sin` and `Cos`;
- powers through `Potencia`;
- addition, subtraction, multiplication, and negation;
- specialized algebraic and trigonometric simplifications;
- numerical evaluation by substituting variable values;
- degree/radian conversion helpers.

The helper functions `suma()`, `resta()`, and `producto()` provide explicit operations for numeric, symbolic, and matrix objects. In particular, `producto()` is recommended for scalar multiplication on the fx-CG50 instead of relying directly on the `*` operator overload.

### Matrix algebra

The `matriz.py` module implements the `Matriz` class for numerical and symbolic matrices.

It provides:

- matrix construction and validation;
- element access;
- addition and subtraction;
- scalar multiplication;
- matrix multiplication;
- product composition through `Matriz.p_m()`;
- transposition;
- determinants of square matrices of order N using recursive cofactor expansion;
- symbolic matrix simplification through `simplificar_m()`;
- numerical evaluation through `evaluar_numerico()`;
- matrix display through `mostrar()`.

The determinant implementation supports square matrices of arbitrary order in principle, but cofactor expansion can become expensive as matrix size increases. Its availability does not mean that high-order determinants are practical to calculate on the calculator.

### Transformations and kinematics

The `rot.py` module groups spatial transformation functions under the `Des` class.

It includes:

- rotations about X, Y, and Z using 4×4 homogeneous matrices;
- 3×3 rotation matrices;
- homogeneous translations;
- Roll-Pitch-Yaw (RPY) composition;
- axis-angle representation;
- axis-angle extraction from a transformation;
- RPY angle extraction;
- Denavit–Hartenberg matrix construction through `Des.DH()`;
- DH table composition through `Des.DH_table()`;
- rigid homogeneous transformation inversion through `Des.H_inv()`.

The implemented RPY composition is:

\[
R_{RPY}(\phi,\theta,\psi)=R_z(\phi)R_y(\theta)R_x(\psi)
\]

The parameter order, naming, and extraction convention follow the reference toolbox used by Dr. César Chávez. They are intentionally preserved; do not reorder or reinterpret the returned angles according to a different RPY convention.

### Symbolic differentiation and Jacobian

The `derivadas.py` module contains the `Derivador` class, which implements differentiation rules for expression types supported by the symbolic engine.

Currently supported cases include:

- constants and variables;
- addition and subtraction;
- products;
- sine and cosine;
- powers with constant exponents;
- the chain rule for supported trigonometric expressions.

This is not a general symbolic differentiator. For example, powers with symbolic exponents are not supported by the current implementation.

The `jacobiano.py` module provides `Jacobiano(funciones, variables)`, which builds a Jacobian matrix from a column vector of functions and a column vector of variables.

### Matrix presentation

The `formato.py` module separates compact expression formatting from the symbolic engine. `Matriz.mostrar()` selects between two presentation levels:

- **Level 0:** full symbolic expression.
- **Level 1:** compact expression, using abbreviations for trigonometric functions and symbolic names when appropriate.

The presentation is designed to make efficient use of the fx-CG50 display width and avoids artificial column alignment using padding spaces.

## Angular convention

Angles are interpreted in **radians** by default. This applies to trigonometric functions and rotation functions that receive angles.

To convert degrees to radians:

```python
from syms import grados

angle = grados(45)
```

The library also provides helpers to convert radians to degrees and degree-based variants where implemented.

## Basic usage

The toolbox modules are located in `casio/`. To run the example on the fx-CG50, copy the required modules to the calculator's Python environment and keep them together so that the existing imports can be resolved.

The following example creates a rotation and a DH transformation:

```python
from syms import Syms, grados
from rot import Des

# Symbolic joint variable
theta = Syms("theta")

# Rotation about the Z axis (3x3)
Rz = Des.rotz3(theta)
Rz.mostrar()

# DH transformation: theta = 45 degrees,
# d = 0, a = 2, alpha = 0
T = Des.DH(grados(45), 0, 2, 0)
T.mostrar()
```

For a more complete example using DH tables, homogeneous transformations, inverses, and Jacobians, see `casio/ejemplo_uso.py`.

## Platform and compatibility

The target platform is the **Casio fx-CG50**, using the Python environment provided by the calculator. Development used the environment identified as based on MicroPython 1.9.4.

The calculator's Python implementation differs from a conventional Python installation. Some features, methods, and operator-dispatch mechanisms may behave differently. For this reason, the code avoids relying on certain features that are not handled consistently on the fx-CG50 and uses helper functions for selected symbolic and matrix operations.

The project also includes automated tests that can be run on a computer using Python and `pytest`. These tests help review code behavior and detect regressions during development. However, **a passing PC test does not by itself demonstrate that the same behavior has been validated on the calculator**.

For environment details, identified limitations, and validation scope, see `docs/02_plataforma.md` (Spanish) and `docs/en/02_platform_and_compatibility.md` (English).

## Tests

The repository separates calculator tests from automated PC tests.

### Tests on the Casio fx-CG50

The `testInCasio/` directory contains scripts intended to run directly on the calculator. `pruebasInCasio.py` contains the regression test suite, while `pruebas_presentacion.py` provides manual diagnostic tools. They do not require `pytest` or external libraries. Copy the `casio/` modules together with the script you intend to run, then execute it in the calculator's Python environment.

### Automated tests on a PC

The `tests/` directory contains automated tests using `pytest`. From the repository root, install the development dependencies and run:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

The guide in `tests/README.md` (Spanish) and `tests/README_EN.md` (English) contains further instructions for running selected tests and extending the suite. `testInCasio/pruebas_presentacion.py` is a manual diagnostic tool and is not part of the automated `pytest` suite.

## Project structure

```text
Robotics_Toolbox_Casio/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── casio/
│   ├── derivadas.py
│   ├── ejemplo_uso.py
│   ├── formato.py
│   ├── jacobiano.py
│   ├── matriz.py
│   ├── rot.py
│   └── syms.py
│
├── docs/
│   ├── README.md
│   ├── 01_objetivos.md
│   ├── 02_plataforma.md
│   ├── 03_arquitectura.md
│   ├── 04_pruebas_presentacion.md
│   ├── VERSION.md
│   └── en/
│       ├── 01_objectives_and_scope.md
│       ├── 02_platform_and_compatibility.md
│       ├── 03_library_architecture.md
│       ├── 04_presentation_tests_and_observed_limits.md
│       ├── README.md
│       └── VERSION.md
│
├── testInCasio/
│   ├── pruebasInCasio.py
│   └── pruebas_presentacion.py
│
├── tests/
│   ├── README.md
│   ├── README_EN.md
│   ├── conftest.py
│   ├── test_derivadas.py
│   ├── test_formato.py
│   ├── test_integracion.py
│   ├── test_jacobiano.py
│   ├── test_matriz.py
│   ├── test_rot.py
│   └── test_syms.py
│
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── pytest.ini
├── README.md
└── requirements-dev.txt
```

The `.git/` directory is not shown because it contains local Git metadata and is managed by Git.

## KhiCAS / Xcas

Independent experiments were carried out with **KhiCAS for the fx-CG50**. Its MicroPython 1.12 environment provides access to the Xcas engine through the `cas` module and the `cas.caseval()` function.

This exploration is kept separate from the toolbox core. Version 1.2 does not depend on KhiCAS for its operations, and no stable integration between the two engines is claimed. Using Xcas as an advanced symbolic backend remains an experimental direction.

## Additional documentation

- `docs/en/01_objectives_and_scope.md`: project objectives and scope.
- `docs/en/02_platform_and_compatibility.md`: target platform, compatibility, and known limitations.
- `docs/en/03_library_architecture.md`: internal organization and module responsibilities.
- `docs/en/04_presentation_tests_and_observed_limits.md`: presentation tests and observed limits.
- `docs/en/VERSION.md`: documented project version.
- `CHANGELOG.md`: version history in Spanish and English.

## Project philosophy

The toolbox aims to be:

- lightweight and suitable for the calculator's resources;
- clear and easy to understand;
- modular;
- specialized in mathematics applied to robotics;
- verifiable through tests on the target hardware;
- extensible without turning the core into a general-purpose CAS.

The project prioritizes operations needed for studying robotic manipulators and avoids adding complexity when a focused, lightweight solution is sufficient.
