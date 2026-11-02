"""Configuracion compartida de las pruebas automaticas."""

from pathlib import Path
import sys

import pytest


# Los modulos de la calculadora usan imports directos (por ejemplo,
# `from syms import ...`). Agregamos la carpeta de la libreria al path
# solamente durante las pruebas; no modificamos el codigo de produccion.
ROOT_DIR = Path(__file__).resolve().parents[1]
CASIO_DIR = ROOT_DIR / "casio"

casio_path = str(CASIO_DIR)
if casio_path not in sys.path:
    sys.path.insert(0, casio_path)


@pytest.fixture
def assert_matrix_close():
    """Compara dos Matriz elemento por elemento con tolerancia numerica."""

    def _assert_matrix_close(actual, expected, abs_tol=1e-9):
        assert actual.filas == expected.filas
        assert actual.columnas == expected.columnas

        for i in range(actual.filas):
            for j in range(actual.columnas):
                assert actual[i, j] == pytest.approx(
                    expected[i, j], abs=abs_tol
                ), "Diferencia en elemento [{}, {}]".format(i, j)

    return _assert_matrix_close
