"""Pruebas de integracion de las funciones principales de robótica."""

import math

import pytest

from jacobiano import Jacobiano
from matriz import Matriz
from rot import Des
from syms import Potencia, Syms


def test_manipulador_planar_2r_cinematica_y_jacobiano(assert_matrix_close):
    q1 = Syms("q1")
    q2 = Syms("q2")
    l1 = Syms("l1")
    l2 = Syms("l2")

    tabla_dh = Matriz([
        [q1, 0, l1, 0],
        [q2, 0, l2, 0],
    ])
    transformacion = Des.DH_table(tabla_dh, False)

    posicion = Matriz([
        [transformacion[0, 3]],
        [transformacion[1, 3]],
    ])
    variables = Matriz([[q1], [q2]])
    jacobiano = Jacobiano(posicion, variables)

    valores = {
        "q1": math.pi / 2,
        "q2": 0,
        "l1": 2,
        "l2": 1,
    }

    assert_matrix_close(
        posicion.evaluar_numerico(valores),
        Matriz([[0], [3]]),
        abs_tol=1e-8,
    )
    assert_matrix_close(
        jacobiano.evaluar_numerico(valores),
        Matriz([[-3, -1], [0, 0]]),
        abs_tol=1e-8,
    )


def test_manipulador_2r_en_otra_configuracion(assert_matrix_close):
    q1 = Syms("q1")
    q2 = Syms("q2")
    l1 = Syms("l1")
    l2 = Syms("l2")

    tabla_dh = Matriz([
        [q1, 0, l1, 0],
        [q2, 0, l2, 0],
    ])
    transformacion = Des.DH_table(tabla_dh, False)

    valores = {
        "q1": 0,
        "q2": 0,
        "l1": 2,
        "l2": 1,
    }

    posicion = Matriz([
        [transformacion[0, 3]],
        [transformacion[1, 3]],
    ]).evaluar_numerico(valores)

    assert_matrix_close(posicion, Matriz([[3], [0]]), abs_tol=1e-8)
