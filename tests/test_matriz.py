"""Pruebas automaticas para las operaciones de Matriz."""

import random

import pytest

from matriz import Matriz
from syms import Expresion, Syms, evaluar


def _determinante_gauss(datos):
    """Calcula un determinante numerico por eliminacion gaussiana.

    Se usa como referencia independiente para contrastar Matriz.determinante().
    """
    a = [list(map(float, fila)) for fila in datos]
    n = len(a)
    resultado = 1.0

    for columna in range(n):
        pivote = max(range(columna, n), key=lambda fila: abs(a[fila][columna]))

        if abs(a[pivote][columna]) < 1e-12:
            return 0.0

        if pivote != columna:
            a[columna], a[pivote] = a[pivote], a[columna]
            resultado *= -1.0

        valor_pivote = a[columna][columna]
        resultado *= valor_pivote

        for fila in range(columna + 1, n):
            factor = a[fila][columna] / valor_pivote
            for j in range(columna + 1, n):
                a[fila][j] -= factor * a[columna][j]
            a[fila][columna] = 0.0

    return resultado


def test_constructor_acepta_matriz_rectangular():
    matriz = Matriz([[1, 2, 3], [4, 5, 6]])

    assert matriz.filas == 2
    assert matriz.columnas == 3
    assert matriz[1, 2] == 6


def test_constructor_copia_las_filas_de_entrada():
    datos = [[1, 2], [3, 4]]
    matriz = Matriz(datos)
    datos[0][0] = 99

    assert matriz[0, 0] == 1


def test_constructor_rechaza_entradas_invalidas():
    with pytest.raises(TypeError):
        Matriz("no es una matriz")

    with pytest.raises(TypeError):
        Matriz([1, 2, 3])

    with pytest.raises(ValueError):
        Matriz([])

    with pytest.raises(ValueError):
        Matriz([[]])

    with pytest.raises(ValueError):
        Matriz([[1, 2], [3]])


def test_suma_y_resta_de_matrices(assert_matrix_close):
    a = Matriz([[1, 2, 3], [4, 5, 6]])
    b = Matriz([[6, 5, 4], [3, 2, 1]])

    assert_matrix_close(a + b, Matriz([[7, 7, 7], [7, 7, 7]]))
    assert_matrix_close(a - b, Matriz([[-5, -3, -1], [1, 3, 5]]))


def test_suma_y_resta_rechazan_dimensiones_incompatibles():
    a = Matriz([[1, 2], [3, 4]])
    b = Matriz([[1, 2, 3]])

    with pytest.raises(ValueError):
        _ = a + b

    with pytest.raises(ValueError):
        _ = a - b


def test_producto_matricial_rectangular(assert_matrix_close):
    a = Matriz([[1, 2, 3], [4, 5, 6]])
    b = Matriz([[1, 2], [3, 4], [5, 6]])

    resultado = Matriz.p_m(a, b)
    esperado = Matriz([[22, 28], [49, 64]])

    assert_matrix_close(resultado, esperado)


def test_producto_matricial_rechaza_dimensiones_incompatibles():
    a = Matriz([[1, 2, 3], [4, 5, 6]])
    b = Matriz([[1, 2], [3, 4]])

    with pytest.raises(ValueError):
        Matriz.p_m(a, b)


def test_producto_por_identidad_y_matriz_cero(assert_matrix_close):
    a = Matriz([[1, 2], [3, 4]])
    identidad = Matriz([[1, 0], [0, 1]])
    cero = Matriz([[0, 0], [0, 0]])

    assert_matrix_close(Matriz.p_m(a, identidad), a)
    assert_matrix_close(Matriz.p_m(identidad, a), a)
    assert_matrix_close(
        Matriz.p_m(a, cero),
        Matriz([[0, 0], [0, 0]])
    )


def test_producto_de_multiples_matrices(assert_matrix_close):
    a = Matriz([[1, 2], [0, 1]])
    b = Matriz([[2, 0], [1, 2]])
    c = Matriz([[1], [3]])

    resultado = Matriz.p_m(a, b, c)
    esperado = Matriz([[16], [7]])

    assert_matrix_close(resultado, esperado)


def test_traspuesta_de_matriz_rectangular(assert_matrix_close):
    matriz = Matriz([[1, 2, 3], [4, 5, 6]])

    assert_matrix_close(
        matriz.traspuesta(),
        Matriz([[1, 4], [2, 5], [3, 6]])
    )


def test_determinantes_basicos():
    assert Matriz([[7]]).determinante() == 7
    assert Matriz([[1, 2], [3, 4]]).determinante() == -2
    assert Matriz([
        [6, 1, 1],
        [4, -2, 5],
        [2, 8, 7],
    ]).determinante() == -306


def test_determinante_de_matriz_triangular():
    matriz = Matriz([
        [2, 1, 0, 0],
        [0, 3, 0, 0],
        [0, 0, 4, 1],
        [0, 0, 0, 5],
    ])

    assert matriz.determinante() == 120


def test_determinante_de_matriz_singular():
    matriz = Matriz([
        [1, 2, 3],
        [1, 2, 3],
        [4, 5, 6],
    ])

    assert matriz.determinante() == 0


def test_determinante_simbolico_se_puede_evaluar():
    x = Syms("x")
    matriz = Matriz([[x, 1], [2, 3]])

    determinante = matriz.determinante()

    assert evaluar(determinante, {"x": 4}) == 10
    assert evaluar(determinante, {"x": 0}) == -2


def test_determinante_rechaza_matrices_no_cuadradas():
    with pytest.raises(ValueError):
        Matriz([[1, 2, 3], [4, 5, 6]]).determinante()


def test_determinantes_con_matrices_deterministas_hasta_5x5():
    generador = random.Random(20261101)

    for orden in range(2, 6):
        for _ in range(2):
            datos = [
                [generador.randint(-4, 4) for _ in range(orden)]
                for _ in range(orden)
            ]

            esperado = _determinante_gauss(datos)
            obtenido = Matriz(datos).determinante()

            assert obtenido == pytest.approx(esperado, abs=1e-8)


def test_matriz_simbolica_se_evalua_completa(assert_matrix_close):
    x = Syms("x")
    y = Syms("y")
    matriz = Matriz([[x, y], [x + y, x * y]])

    resultado = matriz.evaluar_numerico({"x": 2, "y": 3})

    assert_matrix_close(resultado, Matriz([[2, 3], [5, 6]]))


def test_simplificar_m_devuelve_otra_matriz():
    x = Syms("x")
    original = Matriz([[Expresion("+", x, 0), 2], [3, 4]])

    resultado = original.simplificar_m()

    assert resultado is not original
    assert str(resultado[0, 0]) == "x"
    assert str(original[0, 0]) == "x + 0"
