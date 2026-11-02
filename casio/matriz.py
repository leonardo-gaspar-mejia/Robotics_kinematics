from syms import suma, resta, producto, es_cero, es_uno, evaluar, simplificar as simplificar_expresion, ExpresionSimbolica, _mismo_termino
from formato import texto_compacto, crear_mapa_compacto


MAX_FILA_NIVEL0 = 509


def es_matriz_identidad(m):

    if m.filas != m.columnas:
        return False

    for i in range(m.filas):
        for j in range(m.columnas):
            valor = m[i, j]

            if i == j:
                if not es_uno(valor):
                    return False
            else:
                if not es_cero(valor):
                    return False

    return True


def es_matriz_cero(m):

    for i in range(m.filas):
        for j in range(m.columnas):
            if not es_cero(m[i, j]):
                return False

    return True


def _matriz_cero(filas, columnas):

    datos = []

    for _ in range(filas):
        fila = []

        for _ in range(columnas):
            fila.append(0)

        datos.append(fila)

    return Matriz(datos)


def crear_multiplicacion_matriz(a, b):

    if a.columnas != b.filas:
        raise ValueError("Dimensiones incompatibles para multiplicacion")

    if es_matriz_identidad(a):
        return b

    if es_matriz_identidad(b):
        return a

    if es_matriz_cero(a) or es_matriz_cero(b):
        return _matriz_cero(a.filas, b.columnas)

    resultado = []

    for i in range(a.filas):

        fila = []

        for j in range(b.columnas):

            valor = 0

            for k in range(a.columnas):

                termino = producto(
                    a[i, k],
                    b[k, j]
                )

                valor = suma(
                    valor,
                    termino
                )

            fila.append(valor)

        resultado.append(fila)

    return Matriz(resultado)


class Matriz:

    _es_matriz = True

    def __init__(self, data):

        if not isinstance(data, list):
            raise TypeError("Los datos deben ser una lista")

        if len(data) == 0:
            raise ValueError("La matriz no puede estar vacia")

        if not isinstance(data[0], list):
            raise TypeError(
                "La matriz debe ser una lista de listas"
            )

        columnas = len(data[0])

        if columnas == 0:
            raise ValueError(
                "La matriz no puede tener cero columnas"
            )

        for fila in data:

            if not isinstance(fila, list):
                raise TypeError(
                    "Todas las filas deben ser listas"
                )

            if len(fila) != columnas:
                raise ValueError(
                    "Todas las filas deben tener la misma longitud"
                )

        self.data = []

        for fila in data:
            self.data.append(fila[:])

        self.filas = len(self.data)
        self.columnas = columnas


    def __getitem__(self, indice):

        fila, columna = indice

        return self.data[fila][columna]


    def __str__(self):

        return str(self.data)


    def __add__(self, otra):

        if (
            self.filas != otra.filas
            or self.columnas != otra.columnas
        ):
            raise ValueError(
                "Las matrices deben tener las mismas dimensiones"
            )

        resultado = []

        for i in range(self.filas):

            fila = []

            for j in range(self.columnas):

                fila.append(
                    suma(
                        self[i, j],
                        otra[i, j]
                    )
                )

            resultado.append(fila)

        return Matriz(resultado)


    def __sub__(self, otra):

        if (
            self.filas != otra.filas
            or self.columnas != otra.columnas
        ):
            raise ValueError(
                "Las matrices deben tener las mismas dimensiones"
            )

        resultado = []

        for i in range(self.filas):

            fila = []

            for j in range(self.columnas):

                fila.append(
                    resta(
                        self[i, j],
                        otra[i, j]
                    )
                )

            resultado.append(fila)

        return Matriz(resultado)


    def __mul__(self, otra):

        if isinstance(otra, Matriz):
            return crear_multiplicacion_matriz(self, otra)

        return self.multiplicar_escalar(otra)


    def __rmul__(self, otra):

        return self.multiplicar_escalar(otra, izquierda=True)

    def __eq__(self, otra):

        if not isinstance(otra, Matriz):
            return False

        if self.filas != otra.filas or self.columnas != otra.columnas:
            return False

        for i in range(self.filas):
            for j in range(self.columnas):

                a = self[i, j]
                b = otra[i, j]

                if isinstance(a, (int, float)) and isinstance(b, (int, float)):

                    if a != b:
                        return False

                elif not _mismo_termino(a, b):
                    return False

        return True


    def evaluar_numerico(self, valores=None):
        """
        Devuelve una nueva matriz con cada entrada
        reducida a un numero.
        """

        resultado = []

        for i in range(self.filas):

            fila = []

            for j in range(self.columnas):

                fila.append(
                    evaluar(
                        self[i, j],
                        valores
                    )
                )

            resultado.append(fila)

        return Matriz(resultado)


    # =========================================================
    # REPRESENTACION NIVEL 0
    # =========================================================

    def _textos_completos(self):

        textos = []

        for i in range(self.filas):

            fila = []

            for j in range(self.columnas):

                fila.append(
                    str(self[i, j])
                )

            textos.append(fila)

        return textos


    def _longitud_fila_nivel0(
        self,
        textos,
        fila
    ):

        longitud = 2

        for j in range(self.columnas):

            longitud = (
                longitud
                + len(textos[fila][j])
            )

            if j < self.columnas - 1:
                longitud = longitud + 2

        return longitud


    def _fila_nivel0(
        self,
        textos,
        fila
    ):

        linea = "["

        for j in range(self.columnas):

            linea = (
                linea
                + textos[fila][j]
            )

            if j < self.columnas - 1:
                linea = linea + ", "

        linea = linea + "]"

        return linea


    def _mostrar_nivel0(
        self,
        textos
    ):
        print("")
        for i in range(self.filas):

            print(
                self._fila_nivel0(
                    textos,
                    i
                )
            )


    # =========================================================
    # REPRESENTACION NIVEL 1
    # =========================================================

    def _elementos_matriz(self):

        elementos = []

        for i in range(self.filas):

            for j in range(self.columnas):

                elementos.append(
                    self[i, j]
                )

        return elementos


    def _textos_compactos(self):

        elementos = self._elementos_matriz()

        mapa = crear_mapa_compacto(
            elementos
        )

        textos = []

        indice = 0

        for i in range(self.filas):

            fila = []

            for j in range(self.columnas):

                fila.append(
                    texto_compacto(
                        elementos[indice],
                        mapa
                    )
                )

                indice = indice + 1

            textos.append(fila)

        return textos


    def _longitud_fila_compacta(
        self,
        textos,
        fila
    ):

        longitud = 2

        for j in range(self.columnas):

            longitud = (
                longitud
                + len(textos[fila][j])
            )

            if j < self.columnas - 1:
                longitud = longitud + 2

        return longitud


    def _fila_compacta(
        self,
        textos,
        fila
    ):

        linea = "["

        for j in range(self.columnas):

            linea = (
                linea
                + textos[fila][j]
            )

            if j < self.columnas - 1:
                linea = linea + ", "

        linea = linea + "]"

        return linea


    def _mostrar_nivel1(
        self,
        textos
    ):
        print("")
        for i in range(self.filas):

            print(
                self._fila_compacta(
                    textos,
                    i
                )
            )


    # =========================================================
    # MOSTRAR AUTOMATICO
    # =========================================================

    def mostrar(self):

        textos = self._textos_completos()

        for i in range(self.filas):

            longitud = (
                self._longitud_fila_nivel0(
                    textos,
                    i
                )
            )

            if longitud > MAX_FILA_NIVEL0:

                # -------------------------------------------------
                # NIVEL 1
                # -------------------------------------------------

                textos_compactos = (
                    self._textos_compactos()
                )

                self._mostrar_nivel1(
                    textos_compactos
                )
                return

        # -------------------------------------------------
        # NIVEL 0
        # -------------------------------------------------

        self._mostrar_nivel0(
            textos
        )


    # =========================================================
    # OPERACIONES MATRICIALES
    # =========================================================

    def determinante(self):

        if self.filas != self.columnas:
            raise ValueError("La matriz debe ser cuadrada")

        # Casos base
        if self.filas == 1:
            return simplificar_expresion(self[0, 0])

        if self.filas == 2:
            diagonal_principal = producto(
                self[0, 0],
                self[1, 1]
            )

            diagonal_secundaria = producto(
                self[0, 1],
                self[1, 0]
            )

            return simplificar_expresion(
                resta(diagonal_principal, diagonal_secundaria)
            )

        # Buscar la fila o columna con más ceros.
        tipo_expansion = "fila"
        indice_expansion = 0
        max_ceros = -1

        for i in range(self.filas):

            ceros = 0

            for j in range(self.columnas):
                if es_cero(self[i, j]):
                    ceros += 1

            if ceros > max_ceros:
                max_ceros = ceros
                tipo_expansion = "fila"
                indice_expansion = i

        for j in range(self.columnas):

            ceros = 0

            for i in range(self.filas):
                if es_cero(self[i, j]):
                    ceros += 1

            if ceros > max_ceros:
                max_ceros = ceros
                tipo_expansion = "columna"
                indice_expansion = j

        # Si la mejor línea contiene únicamente ceros.
        if max_ceros == self.filas:
            return 0

        terminos = []

        if tipo_expansion == "fila":
            posiciones = [
                (indice_expansion, j)
                for j in range(self.columnas)
            ]
        else:
            posiciones = [
                (i, indice_expansion)
                for i in range(self.filas)
            ]

        # Desarrollo por cofactores.
        for fila_elemento, columna_elemento in posiciones:

            elemento = self[fila_elemento, columna_elemento]

            if es_cero(elemento):
                continue

            datos = []

            for i in range(self.filas):

                if i == fila_elemento:
                    continue

                fila = []

                for j in range(self.columnas):

                    if j != columna_elemento:
                        fila.append(self[i, j])

                datos.append(fila)

            menor = Matriz(datos)

            termino = producto(
                elemento,
                menor.determinante()
            )

            if (fila_elemento + columna_elemento) % 2 != 0:
                termino = resta(0, termino)

            terminos.append(termino)

        if len(terminos) == 0:
            return 0

        return simplificar_expresion(suma(*terminos))


    def p_m(*matrices):

        if len(matrices) == 0:
            return None

        resultado = matrices[0]

        for matriz in matrices[1:]:

            resultado = Matriz.__mul__(
                resultado,
                matriz
            )

        return resultado

    def traspuesta(self):

        datos = []

        for j in range(self.columnas):
            fila = []

            for i in range(self.filas):
                fila.append(self[i, j])

            datos.append(fila)

        return Matriz(datos)

    def simplificar_m(self):

        resultado = []

        for i in range(self.filas):

            fila = []

            for j in range(self.columnas):
                fila.append(
                    simplificar_expresion(self[i, j])
                )

            resultado.append(fila)

        return Matriz(resultado)

    def multiplicar_escalar(self, escalar, izquierda=False):

        if not isinstance(escalar, (int, float, ExpresionSimbolica)):
            raise TypeError("El escalar debe ser numerico o simbolico")

        resultado = []

        for i in range(self.filas):

            fila = []

            for j in range(self.columnas):

                if izquierda:
                    valor = producto(escalar, self[i, j])
                else:
                    valor = producto(self[i, j], escalar)

                fila.append(valor)

            resultado.append(fila)

        return Matriz(resultado)