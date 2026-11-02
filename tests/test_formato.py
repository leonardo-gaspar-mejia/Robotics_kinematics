"""Pruebas automaticas basicas de formato y presentacion."""

from formato import texto_compacto
from matriz import Matriz
from syms import Potencia, Syms, crear_coseno, producto


def test_formato_compacto_de_productos_y_trigonometria():
    l1 = Syms("l1")
    l2 = Syms("l2")
    theta1 = Syms("theta1")
    theta2 = Syms("theta2")

    assert texto_compacto(producto(l1, l2)) == "l1*l2"
    assert texto_compacto(producto(theta1, crear_coseno(theta2))) == "t1*c(t2)"


def test_formato_compacto_asigna_nombres_consistentes():
    theta1 = Syms("theta1")
    theta2 = Syms("theta2")
    matriz = Matriz([[theta1, theta2], [theta2, theta1]])

    textos = matriz._textos_compactos()

    assert textos[0][0] == textos[1][1]
    assert textos[0][1] == textos[1][0]


def test_mostrar_matriz_imprime_contenido(capsys):
    matriz = Matriz([[1, 2], [3, 4]])
    matriz.mostrar()

    salida = capsys.readouterr().out

    assert "[1, 2]" in salida
    assert "[3, 4]" in salida
