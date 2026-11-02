"""Pruebas automaticas para derivacion simbolica."""

import math

import pytest

from derivadas import Derivador
from syms import Potencia, Syms, crear_coseno, crear_seno, crear_suma, evaluar, producto


def test_derivada_de_constante_y_variable():
    x = Syms("x")
    y = Syms("y")

    assert Derivador(5).derivar(x) == 0
    assert Derivador(x).derivar(x) == 1
    assert Derivador(y).derivar(x) == 0


def test_derivada_de_potencia():
    x = Syms("x")
    derivada = Derivador(Potencia(x, 3)).derivar(x)

    assert evaluar(derivada, {"x": 2}) == pytest.approx(12)


def test_derivada_de_suma():
    x = Syms("x")
    derivada = Derivador(crear_suma(Potencia(x, 2), x)).derivar(x)

    assert evaluar(derivada, {"x": 2}) == pytest.approx(5)


def test_derivada_de_producto():
    x = Syms("x")
    expresion = producto(x, crear_seno(x))
    derivada = Derivador(expresion).derivar(x)

    valor = 0.4
    esperado = math.sin(valor) + valor * math.cos(valor)
    assert evaluar(derivada, {"x": valor}) == pytest.approx(esperado)


def test_derivadas_de_seno_y_coseno():
    x = Syms("x")
    valor = 0.7

    d_seno = Derivador(crear_seno(x)).derivar(x)
    d_coseno = Derivador(crear_coseno(x)).derivar(x)

    assert evaluar(d_seno, {"x": valor}) == pytest.approx(math.cos(valor))
    assert evaluar(d_coseno, {"x": valor}) == pytest.approx(-math.sin(valor))


def test_regla_de_la_cadena():
    x = Syms("x")
    expresion = crear_seno(Potencia(x, 2))
    derivada = Derivador(expresion).derivar(x)

    valor = 0.4
    esperado = 2 * valor * math.cos(valor ** 2)
    assert evaluar(derivada, {"x": valor}) == pytest.approx(esperado)


def test_derivador_rechaza_exponente_simbolico():
    x = Syms("x")
    y = Syms("y")

    with pytest.raises(TypeError, match="exponentes constantes"):
        Derivador(Potencia(x, y)).derivar(x)


def test_derivador_rechaza_variable_que_no_es_syms():
    with pytest.raises(TypeError, match="objeto Syms"):
        Derivador(Syms("x")).derivar("x")
