# 4. Presentation tests and observed limits

## 4.1 Objective

This document records the characterization of symbolic-expression output on the fx-CG50 and explains the adaptive presentation mechanism used by `Matriz.mostrar()`.

String length is used as a practical signal for deciding when to switch to compact output. It is not directly equivalent to RAM consumption and does not establish the calculator's total memory limit.

## 4.2 Two presentation levels

The current version maintains two formats:

- **Level 0:** full symbolic representation, with `, ` separators between columns and no padding spaces for column alignment.
- **Level 1:** compact representation; for example, `sin(x)` becomes `s(x)`, `cos(x)` becomes `c(x)`, and some names such as `theta1` may be abbreviated to `t1` when the abbreviation is unambiguous.

Abbreviations remain within the expression itself; no separately defined helper variables are required.

## 4.3 Configured threshold

The following constant is defined in `casio/matriz.py`:

```python
MAX_FILA_NIVEL0 = 509
```

`Matriz.mostrar()` builds the full text and measures the length of each row. If any row exceeds 509 characters, the compact matrix representation is generated and Level 1 is printed. If no row exceeds the threshold, Level 0 is printed.

This value is a representation-selection threshold. It is not a guarantee of free memory or a universal limit on the size of every expression.

## 4.4 Earlier experimental characterization

During an earlier test, a 509-character row was built and printed four consecutive times without observable errors, while a 510-character row caused a failure. A symbolic `T06` matrix was also recorded with elements up to approximately 180 characters and a row of approximately 589 characters.

The test used a representation that still contained padding spaces. The format was later changed to remove that alignment. For this reason, the 509/510 observation is retained as historical experimental evidence and not as an absolute physical limit.

## 4.5 Current level-switching test

The `testInCasio/pruebasInCasio.py` script contains a group that builds a row of 70 `theta` variables and checks that:

- the full row exceeds the Level 0 threshold;
- the compact row is below the threshold;
- the matrix can be displayed in compact format.

The author confirmed that the 24 test groups ran on the fx-CG50. This test checks a representative reduction case; it does not guarantee that every possible compact expression will fit on the display.

## 4.6 Reproducing the analysis

The `testInCasio/pruebas_presentacion.py` file contains diagnostic functions for measuring the length of elements and rows and experimenting with strings of controlled length. The functions require a matrix to have been created beforehand; for example, the symbolic `T06` transformation.

These functions are manual diagnostic tools and are not part of the automated `pytest` suite.

## 4.7 Module responsibilities

- `syms.py`: builds, compares, and simplifies symbolic objects.
- `formato.py`: produces the compact representation.
- `matriz.py`: chooses the presentation level and displays the matrix.

This separation makes it possible to adjust calculator output without mixing presentation decisions into the algebra engine.
