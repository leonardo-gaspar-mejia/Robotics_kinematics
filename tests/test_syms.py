"""Pruebas automaticas para el motor simbolico."""

import math

import pytest

from syms import (
    Expresion,
    Potencia,
    Syms,
    crear_coseno,
    crear_multiplicacion,
    crear_negativo,
    crear_resta,
    crear_seno,
    crear_suma,
    evaluar,
    n,
    producto,
    simplificar,
    suma,
)


def test_operaciones_numericas_basicas():
    assert crear_suma(2, 3) == 5
    assert crear_resta(7, 4) == 3
    assert crear_multiplicacion(3, 4) == 12
    assert crear_negativo(5) == -5


def test_identidades_basicas_con_variables_simbolicas():
    x = Syms("x")
    y = Syms("y")

    assert crear_suma(x, 0) is x
    assert crear_resta(x, x) == 0
    assert n(n(x)) is x
    assert str(x + y) == "x + y"


def test_simplificacion_de_terminos_semejantes():
    x = Syms("x")
    y = Syms("y")

    resultado = suma(
        producto(2, x, y),
        producto(3, y, x),
    )

    assert str(resultado) == "5 * x * y"


def test_identidad_pitagorica():
    x = Syms("x")
    expresion = crear_suma(
        Potencia(crear_seno(x), 2),
        Potencia(crear_coseno(Syms("x")), 2),
    )

    assert expresion == 1


def test_identidad_pitagorica_no_confunde_variables():
    x = Syms("x")
    y = Syms("y")

    expresion = crear_suma(
        Potencia(crear_seno(x), 2),
        Potencia(crear_coseno(y), 2),
    )

    assert expresion != 1


def test_identidades_de_suma_de_angulos():
    a = Syms("a")
    b = Syms("b")

    coseno = crear_suma(
        producto(crear_coseno(a), crear_coseno(b)),
        crear_negativo(producto(crear_seno(a), crear_seno(b))),
    )
    seno = crear_suma(
        producto(crear_seno(a), crear_coseno(b)),
        producto(crear_coseno(a), crear_seno(b)),
    )

    assert str(coseno) == "cos(a + b)"
    assert str(seno) == "sin(a + b)"


def test_evaluar_expresion_con_varias_variables():
    x = Syms("x")
    y = Syms("y")
    expresion = crear_suma(producto(2, x), crear_seno(y))

    resultado = evaluar(expresion, {"x": 3, "y": math.pi / 2})

    assert resultado == pytest.approx(7.0)


def test_evaluar_seno_y_coseno_usa_radianes():
    x = Syms("x")
    assert evaluar(crear_seno(x), {"x": math.pi / 2}) == pytest.approx(1.0)
    assert evaluar(crear_coseno(x), {"x": math.pi}) == pytest.approx(-1.0)


def test_evaluar_potencias_numericas():
    x = Syms("x")
    assert evaluar(Potencia(x, 3), {"x": 2}) == 8
    assert evaluar(Potencia(x, 2), {"x": -3}) == 9


def test_evaluar_rechaza_variables_sin_sustitucion():
    x = Syms("x")

    with pytest.raises(ValueError, match="Falta el valor"):
        evaluar(x, {})


def test_evaluar_rechaza_tipos_no_soportados():
    with pytest.raises(TypeError):
        evaluar(object(), {})


def test_simplificar_reduce_expresion_y_es_estable():
    x = Syms("x")
    expresion = Expresion("+", Expresion("+", x, 0), 0)

    primera = simplificar(expresion)
    segunda = simplificar(primera)

    assert str(primera) == "x"
    assert str(segunda) == "x"


def test_variables_con_mismo_nombre_interno_se_reconocen():
    a = Syms("q1", "theta1")
    b = Syms("q1", "q1")

    assert crear_resta(a, b) == 0
