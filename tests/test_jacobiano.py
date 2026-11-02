"""Pruebas automaticas para la construccion del Jacobiano."""

import pytest

from jacobiano import Jacobiano
from matriz import Matriz
from syms import Potencia, Syms, crear_suma


def test_jacobiano_de_dos_funciones_y_dos_variables(assert_matrix_close):
    x = Syms("x")
    y = Syms("y")

    funciones = Matriz([
        [crear_suma(Potencia(x, 2), y)],
        [x * y],
    ])
    variables = Matriz([[x], [y]])

    resultado = Jacobiano(funciones, variables)
    numerico = resultado.evaluar_numerico({"x": 2, "y": 3})

    assert_matrix_close(numerico, Matriz([[4, 1], [3, 2]]))


def test_jacobiano_rectangular_con_tres_funciones(assert_matrix_close):
    x = Syms("x")
    y = Syms("y")

    funciones = Matriz([
        [x + y],
        [x * y],
        [Potencia(x, 2)],
    ])
    variables = Matriz([[x], [y]])

    resultado = Jacobiano(funciones, variables)
    numerico = resultado.evaluar_numerico({"x": 2, "y": 3})

    assert numerico.filas == 3
    assert numerico.columnas == 2
    assert_matrix_close(numerico, Matriz([[1, 1], [3, 2], [4, 0]]))


def test_jacobiano_exige_vectores_columna():
    x = Syms("x")
    y = Syms("y")

    with pytest.raises(ValueError, match="funciones.*vector columna"):
        Jacobiano(Matriz([[x, y]]), Matriz([[x], [y]]))

    with pytest.raises(ValueError, match="variables.*vector columna"):
        Jacobiano(Matriz([[x], [y]]), Matriz([[x, y]]))


def test_jacobiano_conserva_error_de_derivacion():
    x = Syms("x")
    y = Syms("y")

    with pytest.raises(TypeError, match="exponentes constantes"):
        Jacobiano(
            Matriz([[Potencia(x, y)]]),
            Matriz([[x]])
        )
