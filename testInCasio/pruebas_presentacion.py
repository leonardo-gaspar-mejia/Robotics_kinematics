# Pruebas de presentación para ejecutar en la Casio fx-CG50.
# Requiere que T06 exista antes de llamar a estas funciones.
# No utiliza gc ni depende de funciones que hayan mostrado incompatibilidad.


def medir_elementos(M):
    print("")
    print("===== MEDICION ELEMENTOS =====")

    for i in range(M.filas):
        for j in range(M.columnas):
            try:
                texto = str(M[i,j])
                print("")
                print("Elemento [" + str(i) + "," + str(j) + "]")
                print("Caracteres:", len(texto))
                texto = None
            except MemoryError:
                print("")
                print("Elemento [" + str(i) + "," + str(j) + "]")
                print("MEMORY ERROR")


def medir_filas(M):
    print("")
    print("===== MEDICION FILAS =====")

    for i in range(M.filas):
        try:
            fila = "["

            for j in range(M.columnas):
                fila = fila + " " + str(M[i,j])
                if j < M.columnas - 1:
                    fila = fila + " ,"

            fila = fila + " ]"

            print("")
            print("Fila:", i)
            print("Caracteres:", len(fila))
            fila = None

        except MemoryError:
            print("")
            print("Fila:", i)
            print("MEMORY ERROR")


def probar_longitud(n, imprimir=True):
    try:
        texto = ""

        for i in range(n):
            texto = texto + "x"

        print("OK:", n)

        if imprimir:
            print(texto)

        texto = None

    except MemoryError:
        print("ERROR:", n)


# Ejemplo de uso con la matriz simbólica T06:
# medir_elementos(T06)
# medir_filas(T06)
# probar_longitud(500)
# probar_longitud(600)
# probar_longitud(700)
# probar_longitud(800)
# probar_longitud(900)
# probar_longitud(1000)
