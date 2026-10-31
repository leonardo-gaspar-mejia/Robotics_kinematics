from derivadas import Derivador
from matriz import Matriz


def Jacobiano(funciones, variables):

    if funciones.columnas != 1:
        raise ValueError("Las funciones deben ser un vector columna")

    if variables.columnas != 1:
        raise ValueError("Las variables deben ser un vector columna")

    datos = []

    for i in range(funciones.filas):

        D = Derivador(funciones[i, 0])
        fila = []

        for j in range(variables.filas):
            fila.append(D.derivar(variables[j, 0]))

        datos.append(fila)

    return Matriz(datos)