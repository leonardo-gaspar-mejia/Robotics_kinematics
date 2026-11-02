# Registro de cambios / Changelog

Este archivo mantiene el historial de versiones en español e inglés. / This file keeps the version history in Spanish and English.

---

# Español

## [1.2] - 2026-10-31

Versión que amplía la toolbox desde las operaciones matriciales y transformaciones hacia derivación simbólica limitada y cálculo del Jacobiano. Las correcciones de mantenimiento y documentación que se preparan sobre esta versión no implican un incremento de versión.

### Añadido

- Módulo `derivadas.py` con la clase `Derivador` y reglas para constantes, variables, suma, resta, producto, seno, coseno y potencias con exponente constante.
- Regla de la cadena recursiva para las estructuras simbólicas soportadas por `Derivador`.
- Módulo `jacobiano.py` con `Jacobiano(funciones, variables)` para vectores columna.
- Construcción de transformaciones Denavit–Hartenberg con `Des.DH()` y composición mediante `Des.DH_table()`.
- Inversa de transformaciones rígidas homogéneas mediante `Des.H_inv()`.
- Comparación estructural de matrices y expresiones simbólicas.
- `Matriz.simplificar_m()`, que crea una matriz nueva sin modificar la original.
- Multiplicación por escalar mediante `Matriz.multiplicar_escalar()`.
- Pruebas manuales para la calculadora y pruebas automáticas para PC.

### Mejorado

- Determinantes para matrices cuadradas de orden N mediante expansión por cofactores, con casos directos para 1×1 y 2×2 y selección de fila o columna con más ceros explícitos.
- Simplificación de los resultados del determinante y soporte de expresiones simbólicas.
- Comparaciones algebraicas y trigonométricas basadas en la estructura de los objetos, reduciendo el uso de conversiones a texto como criterio de igualdad.
- Expansión distributiva limitada a 16 términos para evitar crecimiento excesivo de expresiones.
- Representación de potencias con paréntesis para conservar el significado de bases y exponentes compuestos.
- Cálculo de longitud de fila en los formatos de presentación, contando correctamente el separador `, `.
- Corrección del ejemplo `casio/ejemplo_uso.py`: se eliminó una llamada de instancia inválida a `Matriz.mostrar()` sin proporcionar una matriz.
- Pruebas de integración de un manipulador planar 2R.

### Pruebas

- 24 grupos de pruebas manuales en `testInCasio/`, cuya ejecución en la Casio fx-CG50 fue confirmada por el autor.
- 62 pruebas automáticas con `pytest` en PC; pasan en el árbol de trabajo revisado.
- Configuración de GitHub Actions para ejecutar la batería automática ante eventos `push` y `pull_request`.

### Compatibilidad y alcance

- La fx-CG50 continúa siendo la plataforma de ejecución principal.
- La derivación simbólica es deliberadamente limitada y no constituye un CAS general.
- El determinante admite orden N, pero la expansión por cofactores tiene crecimiento factorial en el peor caso y no es adecuada para matrices densas grandes en la calculadora.
- KhiCAS/Xcas permanece como exploración externa; el núcleo no depende de él.

## [1.2] - Mantenimiento

### Corregido

- Correcciones en `Des.Rot_lt()` y `Des.LT()`
  para mejorar la coherencia de las operaciones
  de construcción y extracción eje-ángulo.

- Correcciones en `Des.Rot_RPY()`, conservando
  la convención y el orden de parámetros de la
  toolbox de referencia del Dr. Chávez.

- Ajustes en el formato compacto de matrices
  para mejorar su presentación en la Casio fx-CG50.

### Eliminado

- Se eliminó `Des.camara()` de la API de la librería.

## [1.1] - 2026-09-26

Segunda versión orientada a mejorar la presentación de matrices simbólicas en la Casio fx-CG50, manteniendo el núcleo matemático de la versión 1.0.

### Añadido

- Separación de la lógica de presentación simbólica en un módulo independiente `formato.py`.
- Funciones de formato compacto: `_nombre_compacto()`, `_agregar_nombre_simbolico()`, `_recoger_nombres_simbolicos()`, `crear_mapa_compacto()`, `_compacto_parentesis_suma()`, `_unir_productos_compactos()` y `texto_compacto()`.
- Selección automática entre dos niveles de presentación en `Matriz.mostrar()`.
- Nivel 0: representación simbólica completa.
- Nivel 1: representación simbólica compacta cuando una fila supera el umbral de presentación del Nivel 0.
- Compactación de funciones trigonométricas: `cos(x)` → `c(x)` y `sin(x)` → `s(x)`.
- Compactación de nombres simbólicos cuando la abreviación es inequívoca, por ejemplo `theta1` → `t1` y `alpha2` → `a2`.
- Protección contra abreviaciones ambiguas.
- Pruebas específicas para la selección entre Nivel 0 y Nivel 1.

### Mejorado

- Eliminación de espacios de relleno y alineación artificial entre columnas para reducir el ancho horizontal de la salida destinada a la calculadora.
- `syms.py` permanece dedicado al motor simbólico; `matriz.py` conserva las operaciones matriciales y decide el nivel de presentación; `formato.py` concentra la lógica de representación compacta.

### Evidencia experimental

- En una caracterización anterior, una fila de 509 caracteres se construyó e imprimió cuatro veces consecutivas sin errores observables.
- Una fila de 510 caracteres produjo un fallo en la representación utilizada en aquella prueba.
- La prueba se realizó con un formato que aún contenía espacios de relleno. El resultado 509/510 es evidencia histórica, no un límite físico universal de la fx-CG50.
- La caracterización anterior de `T06` registró elementos de hasta aproximadamente 180 caracteres y una fila de aproximadamente 589 caracteres.

La versión 1.1 mantiene dos niveles de presentación: expresión completa y expresión compacta. Un tercer nivel no está implementado.

## [1.0] - 2026-09-14

Primera versión funcional del núcleo de la Casio Robotics Toolbox.

### Añadido

- Motor simbólico ligero con `Syms`, `Expresion`, `Sin`, `Cos` y `Potencia`.
- Suma, resta y multiplicación simbólicas.
- Simplificación algebraica básica y simplificaciones trigonométricas especializadas.
- Evaluación numérica de expresiones.
- Clase `Matriz` con suma, resta, multiplicación por escalar, multiplicación matricial y transposición.
- Determinantes hasta 3×3.
- Evaluación numérica de matrices y composición mediante `Matriz.p_m()`.
- Rotaciones homogéneas Rx, Ry y Rz; rotaciones 3×3 y traslaciones homogéneas.
- Composición RPY `Rz(phi) · Ry(theta) · Rx(psi)`.
- Convención angular en radianes y conversión explícita mediante `grados()`.
- Presentación matricial sin utilizar `str.rjust()`.

### Compatibilidad y exploración

- Adaptaciones específicas para las limitaciones observadas en la fx-CG50.
- Funciones auxiliares para reducir la dependencia del despacho automático de operadores.
- Pruebas iniciales independientes con KhiCAS MicroPython 1.12 y acceso experimental a Xcas mediante `cas.caseval()`. Esta exploración permaneció fuera del núcleo estable.

---

# English

## [1.2] - 2026-10-31

This version extends the toolbox from matrix operations and transformations to limited symbolic differentiation and Jacobian calculation. Maintenance and documentation work prepared on top of this version does not imply a version increment.

### Added

- `derivadas.py` module with the `Derivador` class and rules for constants, variables, addition, subtraction, products, sine, cosine, and powers with constant exponents.
- Recursive chain-rule support for the symbolic structures supported by `Derivador`.
- `jacobiano.py` module with `Jacobiano(funciones, variables)` for column vectors.
- Denavit–Hartenberg transformation construction through `Des.DH()` and composition through `Des.DH_table()`.
- Inversion of rigid homogeneous transformations through `Des.H_inv()`.
- Structural comparison of matrices and symbolic expressions.
- `Matriz.simplificar_m()`, which creates a new matrix without modifying the original.
- Scalar multiplication through `Matriz.multiplicar_escalar()`.
- Manual tests for the calculator and automated tests for desktop Python.

### Improved

- Determinants for square matrices of order N through cofactor expansion, with direct cases for 1×1 and 2×2 matrices and selection of a row or column containing the largest number of explicit zeros.
- Simplification of determinant results and support for symbolic expressions.
- Algebraic and trigonometric comparisons based on object structure, reducing reliance on text conversion as an equality criterion.
- Distributive expansion limited to 16 terms to prevent excessive expression growth.
- Power representation with parentheses to preserve the meaning of composite bases and exponents.
- Row-length calculation in presentation formats, correctly counting the `, ` separator.
- `casio/ejemplo_uso.py` example correction: an invalid instance call to `Matriz.mostrar()` without a matrix instance was removed.
- Integration tests for a planar 2R manipulator.

### Tests

- 24 groups of manual tests in `testInCasio/`, whose execution on the Casio fx-CG50 was confirmed by the author.
- 62 automated `pytest` tests on desktop Python; they pass in the reviewed working tree.
- GitHub Actions configuration to run the automated suite on `push` and `pull_request` events.

### Compatibility and scope

- The fx-CG50 remains the primary execution platform.
- Symbolic differentiation is deliberately limited and is not a general-purpose CAS.
- Determinants support order N, but cofactor expansion has factorial worst-case growth and is not suitable for large dense matrices on the calculator.
- KhiCAS/Xcas remains an external exploration; the core does not depend on it.

## [1.2] - Maintenance

### Fixed

- Corrections to `Des.Rot_lt()` and `Des.LT()`
  to improve consistency in axis-angle rotation
  construction and extraction.

- Corrections to `Des.Rot_RPY()`, preserving
  the convention and parameter order of the
  reference toolbox by Dr. Chávez.

- Adjustments to compact matrix formatting
  to improve presentation on the Casio fx-CG50.

### Removed

- Removed `Des.camara()` from the library API.

## [1.1] - 2026-09-26

The second version focused on improving symbolic matrix presentation on the Casio fx-CG50 while retaining the mathematical core of version 1.0.

### Added

- Separation of symbolic presentation logic into the independent `formato.py` module.
- Compact-format functions: `_nombre_compacto()`, `_agregar_nombre_simbolico()`, `_recoger_nombres_simbolicos()`, `crear_mapa_compacto()`, `_compacto_parentesis_suma()`, `_unir_productos_compactos()`, and `texto_compacto()`.
- Automatic selection between two presentation levels in `Matriz.mostrar()`.
- Level 0: full symbolic representation.
- Level 1: compact symbolic representation when a row exceeds the Level 0 presentation threshold.
- Trigonometric compaction: `cos(x)` → `c(x)` and `sin(x)` → `s(x)`.
- Symbolic-name compaction when an abbreviation is unambiguous, for example `theta1` → `t1` and `alpha2` → `a2`.
- Protection against ambiguous abbreviations.
- Specific tests for selection between Level 0 and Level 1.

### Improved

- Removal of padding spaces and artificial column alignment to reduce the horizontal width of calculator output.
- `syms.py` remains dedicated to the symbolic engine; `matriz.py` retains matrix operations and selects the presentation level; `formato.py` contains compact-format logic.

### Experimental evidence

- In an earlier characterization, a 509-character row was built and printed four consecutive times without observable errors.
- A 510-character row caused a failure in the representation used in that test.
- The test used a format that still included padding spaces. The 509/510 result is historical evidence, not a universal physical limit of the fx-CG50.
- Earlier `T06` characterization recorded elements up to approximately 180 characters and a row of approximately 589 characters.

Version 1.1 maintains two presentation levels: full expression and compact expression. A third level is not implemented.

## [1.0] - 2026-09-14

First functional version of the Casio Robotics Toolbox core.

### Added

- Lightweight symbolic engine with `Syms`, `Expresion`, `Sin`, `Cos`, and `Potencia`.
- Symbolic addition, subtraction, and multiplication.
- Basic algebraic and specialized trigonometric simplification.
- Numerical evaluation of expressions.
- `Matriz` class with matrix addition, subtraction, scalar multiplication, matrix multiplication, and transposition.
- Determinants up to 3×3.
- Numerical matrix evaluation and product composition through `Matriz.p_m()`.
- Homogeneous rotations Rx, Ry, and Rz; 3×3 rotations; and homogeneous translations.
- RPY composition `Rz(phi) · Ry(theta) · Rx(psi)`.
- Radian angular convention and explicit degree conversion through `grados()`.
- Matrix presentation without using `str.rjust()`.

### Compatibility and exploration

- Adaptations for limitations observed on the fx-CG50.
- Helper functions to reduce reliance on automatic operator dispatch.
- Independent initial experiments with KhiCAS MicroPython 1.12 and experimental Xcas access through `cas.caseval()`. This exploration remained outside the stable core.
