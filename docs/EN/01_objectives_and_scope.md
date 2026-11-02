# 1. Objectives and scope

## 1.1 General objective

Develop a lightweight mathematics and robotics toolbox for the Casio fx-CG50, focused on matrix algebra, spatial transformations, and the symbolic operations needed to study robotic manipulators.

Version 1.2 extends the core with limited symbolic differentiation, Jacobian construction, and Denavit–Hartenberg transformation tools, while keeping calculator compatibility as the main priority.

## 1.2 Specific objectives

### Matrix algebra

Implement `Matriz` to store numerical data and symbolic expressions. The class provides:

- matrix construction and validation;
- addition and subtraction;
- matrix multiplication and product composition;
- scalar multiplication;
- transposition;
- structural comparison;
- simplification into a new matrix;
- numerical evaluation;
- determinants of square matrices of order N.

The determinant is computed through recursive cofactor expansion. Direct cases are used for 1×1 and 2×2 matrices, and the algorithm selects a row or column containing the largest number of explicit zeros. The algorithm can become expensive for large dense matrices.

### Symbolic engine

Represent expressions as objects rather than only as text strings. The core supports variables, addition, subtraction, multiplication, negation, sine, cosine, and powers, together with specialized algebraic and trigonometric simplifications.

Distributive expansion is limited to 16 terms to control expression growth. Recursive simplification is limited to a maximum of six passes.

### Symbolic differentiation

The `Derivador` class implements rules for:

- constants and variables;
- addition and subtraction;
- products;
- sine and cosine;
- powers with constant exponents.

Differentiation is recursive and applies the chain rule when an expression is composed of supported structures. It does not implement quotients, variable exponents, or a general set of mathematical functions.

### Jacobian

`Jacobiano(funciones, variables)` builds a matrix of partial derivatives. Both arguments must be `Matriz` column vectors. If there are `m` functions and `n` variables, the result has dimensions `m × n`.

### Kinematics and transformations

Provide rotations, translations, and homogeneous transformations; matrix composition; RPY representation; Denavit–Hartenberg matrices; DH table composition; and inversion of rigid homogeneous transformations.

## 1.3 Angular convention

The default angular unit is radians. `grados(value)` converts degrees to radians, while `radianes_a_grados(value)` performs the reverse conversion. Numerical trigonometric functions use radians.

The adopted RPY composition is:

```text
R_RPY(phi, theta, psi) = Rz(phi) · Ry(theta) · Rx(psi)
```

The parameter order, names, and extraction convention are preserved from the reference toolbox used by Dr. César Chávez. They must not be reinterpreted or reordered according to a different RPY convention.

## 1.4 Design principles

- Prioritize compatibility with the fx-CG50.
- Keep the core small and specialized in robotics.
- Separate the symbolic engine, matrices, transformations, and presentation.
- Avoid external dependencies in code copied to the calculator.
- Use tests that can run on the calculator and automated tests on a PC.
- Document performance limitations and the scope of symbolic rules.

## 1.5 Out of scope

Version 1.2 is not intended to be a general-purpose CAS. It does not include, among other capabilities:

- general symbolic integration;
- general equation or system solving;
- general polynomial factorization;
- symbolic limits;
- differentiation of arbitrary mathematical functions;
- general inversion of matrices of any size;
- advanced symbolic optimization.

KhiCAS/Xcas has been explored as a possible external engine, but it is not part of the dependencies or core workflow in version 1.2.

## 1.6 Validation

The `testInCasio/` suite contains 24 groups of manual checks that the author confirmed on the fx-CG50. The `tests/` directory contains 62 automated tests run on desktop Python using `pytest`. These suites have different purposes, and neither replaces the other.
