from syms import (
    Syms, Expresion, Sin, Cos, Potencia,
    crear_suma, crear_resta,
    crear_negativo, crear_multiplicacion,
    crear_seno, crear_coseno,
    es_numero
)


class Derivador:

    def __init__(self, expresion):
        self.expresion = expresion

    def derivar(self, variable):
        if not isinstance(variable, Syms):
            raise TypeError("La variable debe ser un objeto Syms")

        return self._derivar(self.expresion, variable)

    def _derivar(self, expresion, variable):

        # Constantes numericas
        if es_numero(expresion):
            return 0

        # Variables simbolicas
        if isinstance(expresion, Syms):
            if expresion.nombre == variable.nombre:
                return 1
            return 0

        # Seno
        if isinstance(expresion, Sin):
            argumento = expresion.argumento

            derivada_argumento = self._derivar(
                argumento, variable
            )

            return crear_multiplicacion(
                crear_coseno(argumento),
                derivada_argumento
            )

        # Coseno
        if isinstance(expresion, Cos):
            argumento = expresion.argumento

            derivada_argumento = self._derivar(
                argumento, variable
            )

            resultado = crear_multiplicacion(
                crear_seno(argumento),
                derivada_argumento
            )

            return crear_negativo(resultado)

        # Potencias con exponente constante
        if isinstance(expresion, Potencia):
            base = expresion.base
            exponente = expresion.exponente

            if not es_numero(exponente):
                raise TypeError(
                    "Por ahora solo se admiten exponentes constantes"
                )

            if exponente == 0:
                return 0

            derivada_base = self._derivar(
                base, variable
            )

            if exponente == 1:
                return derivada_base

            nuevo_exponente = exponente - 1

            if nuevo_exponente == 0:
                nueva_base = 1
            elif nuevo_exponente == 1:
                nueva_base = base
            else:
                nueva_base = Potencia(
                    base, nuevo_exponente
                )

            resultado = crear_multiplicacion(
                exponente, nueva_base
            )

            return crear_multiplicacion(
                resultado, derivada_base
            )

        # Expresiones algebraicas
        if isinstance(expresion, Expresion):

            izquierda = expresion.izquierda

            # Negativo
            if expresion.operador == "neg":
                return crear_negativo(
                    self._derivar(izquierda, variable)
                )

            derecha = expresion.derecha

            derivada_izquierda = self._derivar(
                izquierda, variable
            )

            derivada_derecha = self._derivar(
                derecha, variable
            )

            # Suma
            if expresion.operador == "+":
                return crear_suma(
                    derivada_izquierda,
                    derivada_derecha
                )

            # Resta
            if expresion.operador == "-":
                return crear_resta(
                    derivada_izquierda,
                    derivada_derecha
                )

            # Producto
            if expresion.operador == "*":
                termino_1 = crear_multiplicacion(
                    derivada_izquierda,
                    derecha
                )

                termino_2 = crear_multiplicacion(
                    izquierda,
                    derivada_derecha
                )

                return crear_suma(
                    termino_1,
                    termino_2
                )

        raise TypeError(
            "Tipo de expresion no soportado: "
            + str(type(expresion))
        )