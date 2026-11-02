# 3. Library architecture

## 3.1 Module organization

The `casio/` directory contains only the toolbox modules and the usage example.

| File | Responsibility | Main elements |
|---|---|---|
| `syms.py` | Expression trees, operations, and symbolic simplification | `Syms`, `Expresion`, `Sin`, `Cos`, `Potencia`, `evaluar()`, `simplificar()`, `suma()`, `resta()`, `producto()`, `n()` |
| `matriz.py` | Numerical/symbolic matrices and coordinated presentation | `Matriz`, `determinante()`, `p_m()`, `traspuesta()`, `simplificar_m()`, `evaluar_numerico()` |
| `formato.py` | Conversion of expressions to compact text | `crear_mapa_compacto()`, `texto_compacto()` |
| `rot.py` | Rotations, transformations, and parameter extraction | `Des.rotx*()`, `Des.roty*()`, `Des.rotz*()`, `Des.trans()`, `Des.Rot_RPY()`, `Des.Rot_lt()`, `Des.LT()`, `Des.RPY()`, `Des.DH()`, `Des.DH_table()`, `Des.H_inv()` |
| `derivadas.py` | Symbolic differentiation using selected rules | `Derivador` |
| `jacobiano.py` | Jacobian construction from column vectors | `Jacobiano()` |
| `ejemplo_uso.py` | DH composition, homogeneous transformation, and Jacobian example | Demonstration script |

Imports between modules are direct (for example, `from syms import ...`). For this reason, the `.py` files in `casio/` must remain together when copied to the calculator.

## 3.2 Symbolic engine

`syms.py` represents expressions as objects rather than strings. `Syms` stores the internal variable name and its visible representation. `Expresion` represents arithmetic operations, while `Sin`, `Cos`, and `Potencia` represent functions and powers.

The `crear_suma()`, `crear_resta()`, and `crear_multiplicacion()` constructors apply immediate simplifications. The `simplificar()` function traverses the expression recursively and repeats the process until it stabilizes or reaches six passes.

Term comparisons use `_mismo_termino()` and traverse the symbolic structure. Therefore, structural mathematical equality does not depend only on whether two objects produce the same text string.

Distributive expansion is limited by `MAX_TERMINOS_EXPANSION = 16`. If expanding a multiplication would exceed this limit, the product is preserved without distribution.

## 3.3 Numerical evaluation

`evaluar(expression, values)` substitutes symbolic variables using a dictionary whose keys are the internal names of `Syms` objects. Sine and cosine arguments are interpreted in radians.

`Matriz.evaluar_numerico(values)` applies this evaluation to matrix elements and returns a new numerical matrix.

## 3.4 Matrix core

`Matriz` stores its data as a list of lists. The constructor validates that there is at least one row and one column and that every row has the same length.

Available operations include addition, subtraction, matrix multiplication, scalar multiplication, structural equality, transposition, and simplification into a new matrix. `Matriz.p_m(A, B, C, ...)` composes products while preserving factor order.

### Determinant

`Matriz.determinante()` requires a non-empty square matrix. It uses direct results for 1×1 and 2×2 matrices and recursive cofactor expansion for higher orders. Before expanding, it searches rows and columns for a line containing the largest number of exact zeros.

This method supports square matrices of order N, but its cost can grow factorially for dense matrices. Zero detection is exact: symbolic expressions that are mathematically equivalent to zero but have not been simplified may not be counted as zeros.

## 3.5 Symbolic differentiation

`Derivador(expression).derivar(variable)` accepts a `Syms` variable. Implemented rules include:

- constants and variables;
- addition and subtraction;
- products;
- sine and cosine;
- powers with constant numerical exponents;
- negation.

Recursion applies the chain rule to composite arguments built from these supported types. Quotient rules, symbolic exponents, and functions such as logarithm, exponential, or tangent are not implemented.

## 3.6 Jacobian

`Jacobiano(funciones, variables)` requires two `Matriz` objects representing column vectors. For `m` functions and `n` variables, it returns an `m × n` matrix; each element is the partial derivative of one function with respect to one variable.

## 3.7 Transformations

`rot.py` groups geometric operations under `Des`:

- `rotx`, `roty`, `rotz`: 4×4 homogeneous rotations.
- `rotx3`, `roty3`, `rotz3`: 3×3 rotations.
- `trans(x, y, z)`: homogeneous translation.
- `Rot_RPY(phi, theta, psi)`: composition `Rz(phi) · Ry(theta) · Rx(psi)`.
- `Rot_lt(lx, ly, lz, theta)`: rotation matrix from an axis and angle.
- `LT(H)`: numerical extraction of axis and angle from a transformation/rotation.
- `RPY(H)`: numerical extraction of RPY angles, including a special gimbal-lock case.
- `DH(theta, d, a, alpha)`: Denavit–Hartenberg transformation.
- `DH_table(table)`: composition of DH rows; the table must have four columns.
- `H_inv(H)`: inverse of a rigid homogeneous transformation.
- `nsad()`: symbolic template for a homogeneous matrix with the n, s, a, and d vectors.

The RPY implementation follows the parameter names, order, and extraction convention of the reference toolbox used by Dr. César Chávez. This convention is intentionally preserved.

`H_inv()` uses the transpose of the rotational submatrix and `-Rᵀd`; it assumes a rigid transformation with an orthonormal rotation matrix. It is not a general inverse for every 4×4 matrix.

## 3.8 Presentation

`formato.py` is separated from the symbolic engine. `texto_compacto()` generates shorter output through sine/cosine abbreviations and symbolic-name abbreviations while protecting ambiguous cases. It also preserves parentheses when a power has a composite base or exponent.

`Matriz.mostrar()` measures each row of the full representation. If any row exceeds `MAX_FILA_NIVEL0`, it generates the compact representation and displays Level 1. The threshold is a presentation parameter, not a guarantee that every expression can be displayed without error.

## 3.9 Test separation and experiments

- `testInCasio/` contains scripts copied to the calculator to validate essential operations.
- `tests/` contains automated PC tests using `pytest`.
- `.github/workflows/tests.yml` automates execution of the PC tests.

KhiCAS/Xcas has been studied as a possible external engine, but no backend is integrated in this version. The toolbox does not import the `cas` module.
