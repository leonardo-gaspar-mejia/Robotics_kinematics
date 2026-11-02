"""Pruebas automaticas para rotaciones y transformaciones."""

import math

import pytest

from matriz import Matriz
from rot import Des
from syms import Syms, grados


def _identidad_3():
    return Matriz([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


def _identidad_4():
    return Matriz([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])


def test_rotaciones_de_90_grados(assert_matrix_close):
    angulo = math.pi / 2

    assert_matrix_close(
        Des.rotx3(angulo),
        Matriz([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    )
    assert_matrix_close(
        Des.roty3(angulo),
        Matriz([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    )
    assert_matrix_close(
        Des.rotz3(angulo),
        Matriz([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    )


def test_rotaciones_son_ortogonales(assert_matrix_close):
    for rotacion in (
        Des.rotx3(0.31),
        Des.roty3(-0.72),
        Des.rotz3(1.13),
    ):
        producto = Matriz.p_m(rotacion, rotacion.traspuesta())
        assert_matrix_close(producto, _identidad_3(), abs_tol=1e-8)


def test_rotaciones_homogeneas_tienen_dimensiones_4x4():
    assert (Des.rotx(0.2).filas, Des.rotx(0.2).columnas) == (4, 4)
    assert (Des.roty(0.2).filas, Des.roty(0.2).columnas) == (4, 4)
    assert (Des.rotz(0.2).filas, Des.rotz(0.2).columnas) == (4, 4)


def test_composicion_rpy_y_recuperacion(assert_matrix_close):
    phi = grados(30)
    theta = grados(20)
    psi = grados(40)

    original = Des.Rot_RPY(phi, theta, psi)
    recuperados = Des.RPY(original, False)
    reconstruida = Des.Rot_RPY(*recuperados)

    assert_matrix_close(original, reconstruida, abs_tol=1e-8)


def test_rpy_en_bloqueo_de_gimbal(assert_matrix_close):
    phi = grados(30)
    psi = grados(40)

    for theta in (math.pi / 2, -math.pi / 2):
        original = Des.Rot_RPY(phi, theta, psi)
        recuperados = Des.RPY(original, False)
        reconstruida = Des.Rot_RPY(*recuperados)
        assert_matrix_close(original, reconstruida, abs_tol=1e-7)


def test_rotacion_eje_angulo_reconstruye_rotacion(assert_matrix_close):
    norma = math.sqrt(14.0)
    eje = (1 / norma, -2 / norma, 3 / norma)
    angulo = 0.73

    original = Des.Rot_lt(eje[0], eje[1], eje[2], angulo)
    eje_recuperado = Des.LT(original, False)
    reconstruida = Des.Rot_lt(*eje_recuperado[:3], eje_recuperado[3])

    assert eje_recuperado[3] == pytest.approx(angulo)
    assert_matrix_close(original, reconstruida, abs_tol=1e-7)


def test_rotacion_eje_angulo_identidad():
    eje = Des.LT(_identidad_3(), False)
    assert eje == (0.0, 0.0, 0.0, 0.0)


def test_rotacion_eje_angulo_180_grados(assert_matrix_close):
    norma = math.sqrt(14.0)
    original = Des.Rot_lt(1 / norma, -2 / norma, 3 / norma, math.pi)

    recuperado = Des.LT(original, False)
    reconstruida = Des.Rot_lt(*recuperado[:3], recuperado[3])

    assert recuperado[3] == pytest.approx(math.pi, abs=1e-7)
    assert_matrix_close(original, reconstruida, abs_tol=1e-7)


def test_rotacion_eje_angulo_acepta_angulos_simbolicos():
    theta = Syms("theta")
    resultado = Des.Rot_lt(1, 0, 0, theta)

    assert resultado.filas == 3
    assert resultado.columnas == 3


def test_transformacion_dh_basica(assert_matrix_close):
    resultado = Des.DH(0, 3, 2, 0)
    esperado = Matriz([
        [1, 0, 0, 2],
        [0, 1, 0, 0],
        [0, 0, 1, 3],
        [0, 0, 0, 1],
    ])

    assert_matrix_close(resultado, esperado)


def test_tabla_dh_compone_dos_traslaciones(assert_matrix_close):
    tabla = Matriz([[0, 0, 2, 0], [0, 0, 3, 0]])

    resultado = Des.DH_table(tabla, False)
    esperado = Matriz([
        [1, 0, 0, 5],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    assert_matrix_close(resultado, esperado)


def test_tabla_dh_rechaza_filas_con_numero_incorrecto_de_columnas():
    with pytest.raises(ValueError):
        Des.DH_table(Matriz([[0, 0, 1]]), False)


def test_inversa_homogenea_por_izquierda_y_derecha(assert_matrix_close):
    transformacion = Des.DH(
        grados(30),
        2,
        3,
        grados(-20),
    )
    inversa = Des.H_inv(transformacion)

    assert_matrix_close(
        Matriz.p_m(transformacion, inversa),
        _identidad_4(),
        abs_tol=1e-8,
    )
    assert_matrix_close(
        Matriz.p_m(inversa, transformacion),
        _identidad_4(),
        abs_tol=1e-8,
    )

def test_rpy_grados_conserva_orden_original_de_toolbox():
    original = Des.Rot_RPY_grados(30, 20, 40)

    recuperados = Des.RPY_grados(original)

    assert recuperados == pytest.approx(
        (30.0, 20.0, 40.0),
        abs=1e-8
    )
