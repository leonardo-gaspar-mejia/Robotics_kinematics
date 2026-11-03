"""Pruebas automaticas basicas de formato y presentacion."""

from formato import texto_compacto, texto_completo
from matriz import Matriz
from syms import Potencia, Syms, crear_coseno, producto, suma, grados, n


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

def test_truncamiento_numerico():

    assert texto_completo(1.234567) == "1.2345"
    assert texto_completo(2.500000) == "2.5"


def test_constante_angular_en_grados():

    theta = Syms("theta1")

    expresion = crear_coseno(
        suma(theta, n(grados(90)))
    )

    assert texto_completo(
        expresion,
        grados=True
    ) == "cos(theta1 - 90 deg)"


def test_constante_angular_en_radianes():

    theta = Syms("theta1")

    expresion = crear_coseno(
        suma(theta, n(grados(90)))
    )

    assert texto_completo(
        expresion
    ) == "cos(theta1 - 1.5707)"


def test_coeficiente_no_se_convierte_a_grados():

    theta = Syms("theta1")

    expresion = crear_coseno(
        suma(
            producto(0.5, theta),
            grados(45)
        )
    )

    resultado = texto_completo(
        expresion,
        grados=True
    )

    assert resultado == "cos(0.5 * theta1 + 45 deg)"


def test_formateo_no_modifica_expresion():

    theta = Syms("theta1")

    expresion = crear_coseno(
        suma(theta, n(grados(90)))
    )

    original = str(expresion)

    texto_completo(expresion, grados=True)

    assert str(expresion) == original


def test_mostrar_matriz_en_grados(capsys):

    theta = Syms("theta1")

    expresion = crear_coseno(
        suma(theta, n(grados(90)))
    )

    matriz = Matriz([[expresion]])

    matriz.mostrar(True)

    salida = capsys.readouterr().out

    assert "90 deg" in salida