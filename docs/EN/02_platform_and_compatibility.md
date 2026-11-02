# 2. Platform and compatibility

## 2.1 Target platform

The primary execution platform is the **Casio fx-CG50** calculator. The modules in `casio/` are intended to be copied together into the calculator's Python folder.

## 2.2 Python environment

During development, the fx-CG50 Python environment was identified as an implementation based on **MicroPython 1.9.4**. It should not be assumed to behave exactly like a full desktop Python or MicroPython installation. Some functions, methods, and operator mechanisms may differ.

Compatibility is considered confirmed only after the operation has been tested directly on the calculator.

## 2.3 Operator behavior

During development, differences were observed in automatic operator dispatch for user-defined classes. For this reason, the project recommends using its explicit helper functions for matrix and symbolic operations:

```python
suma(a, b)
resta(a, b)
producto(a, b)
Matriz.p_m(A, B, C)
```

The `n(expression)` helper is available for symbolic negation. This interface reduces dependence on operator overloading in the calculator's interpreter.

## 2.4 Symbols and text

Symbolic names preferably use ASCII characters, for example `theta1`, `alpha2`, `q1`, and `L1`. The `formato.py` module can abbreviate names in a controlled way in compact display mode.

## 2.5 Angular convention

The internal angular convention is radians. Numerical trigonometric functions use radians. Use `grados()` to explicitly convert a value in degrees before passing it to a function that expects radians.

## 2.6 Matrix presentation

`Matriz.mostrar()` uses two presentation levels:

- **Level 0:** full symbolic text.
- **Level 1:** compact text with self-contained abbreviations.

The `MAX_FILA_NIVEL0` constant currently has a value of 509. If any Level 0 row exceeds this threshold, `mostrar()` builds the compact representation and displays the matrix at Level 1. This value is an internal selection threshold, not a universal guarantee of maximum string length or available memory.

## 2.7 Experimental characterization

In earlier tests, a 509-character row was built and printed four times without observable errors, while a 510-character row caused a failure in the representation used for that test. A symbolic `T06` matrix was also recorded with elements up to approximately 180 characters and a row of approximately 589 characters.

These results describe specific tests; they do not establish the calculator's absolute memory limit. The representation was later changed to remove padding spaces and automatically select compact mode. Therefore, the historical 509/510 observation must not be treated as a universal hardware specification.

## 2.8 KhiCAS/Xcas

KhiCAS for the fx-CG50 was explored independently. Its environment includes MicroPython 1.12 and the `cas` module for communicating with Xcas. This exploration is not integrated into the version 1.2 core. The library works without importing `cas` or depending on KhiCAS.

## 2.9 Tests by platform

- `testInCasio/`: contains `pruebasInCasio.py`, the calculator regression suite, and `pruebas_presentacion.py`, a manual diagnostic tool. They run alongside the modules from `casio/` and do not require `pytest`.
- `tests/`: desktop tests that use `pytest` with conventional Python.
- `pytest.ini` and `requirements-dev.txt`: configure test discovery and development dependencies.
- `.github/workflows/tests.yml`: runs the PC test suite on each `push`, `pull_request`, and manual launch from GitHub Actions.

A passing PC test does not, by itself, demonstrate compatibility with the fx-CG50. This is why the manual calculator test suite is retained.
