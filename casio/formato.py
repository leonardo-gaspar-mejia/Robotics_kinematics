from syms import (Syms,Sin,Cos,Potencia,Expresion,es_numero,radianes_a_grados,_redondear)

def _nombre_compacto(nombre):

    if len(nombre) == 0:
        return nombre

    indice = 0

    while indice < len(nombre):
        c = nombre[indice]

        es_letra = (
            ('a' <= c <= 'z')
            or ('A' <= c <= 'Z')
        )

        if not es_letra:
            break

        indice = indice + 1

    prefijo = nombre[:indice]
    resto = nombre[indice:]

    if len(prefijo) == 0:
        return nombre

    resto_limpio = ""

    for i in range(len(resto)):
        c = resto[i]

        if c != "_":
            resto_limpio = resto_limpio + c

    return prefijo[0] + resto_limpio


def _agregar_nombre_simbolico(lista, nombre):

    for i in range(len(lista)):
        if lista[i] == nombre:
            return

    lista.append(nombre)


def _recoger_nombres_simbolicos(expresion, nombres):

    if isinstance(expresion, Syms):
        _agregar_nombre_simbolico(
            nombres,
            expresion.nombre
        )
        return

    if isinstance(expresion, Sin) or isinstance(expresion, Cos):
        _recoger_nombres_simbolicos(
            expresion.argumento,
            nombres
        )
        return

    if isinstance(expresion, Potencia):
        _recoger_nombres_simbolicos(
            expresion.base,
            nombres
        )
        _recoger_nombres_simbolicos(
            expresion.exponente,
            nombres
        )
        return

    if isinstance(expresion, Expresion):
        _recoger_nombres_simbolicos(
            expresion.izquierda,
            nombres
        )

        if expresion.derecha is not None:
            _recoger_nombres_simbolicos(
                expresion.derecha,
                nombres
            )


def crear_mapa_compacto(elementos):

    nombres = []

    for elemento in elementos:
        _recoger_nombres_simbolicos(
            elemento,
            nombres
        )

    candidatos = {}

    for nombre in nombres:
        candidato = _nombre_compacto(nombre)

        if candidato in candidatos:

            if candidatos[candidato] != nombre:
                candidatos[candidato] = None

        else:
            candidatos[candidato] = nombre

    mapa = {}

    for nombre in nombres:

        candidato = _nombre_compacto(nombre)

        if candidatos[candidato] is None:
            mapa[nombre] = nombre

        else:
            mapa[nombre] = candidato

    return mapa


def _formatear_numero(valor, decimales=4):

    texto = str(valor)

    if "e" in texto or "E" in texto:
        separador = "e" if "e" in texto else "E"
        mantisa, exponente = texto.split(separador, 1)

        if "." in mantisa:
            entero, decimal = mantisa.split(".", 1)
            decimal = decimal[:decimales].rstrip("0")

            if decimal:
                mantisa = entero + "." + decimal
            else:
                mantisa = entero

        return mantisa + separador + exponente

    if "." not in texto:
        return texto

    entero, decimal = texto.split(".", 1)
    decimal = decimal[:decimales].rstrip("0")

    if not decimal:
        if entero == "-0" or entero == "0":
            return "0"
        return entero

    return entero + "." + decimal


def _formatear_angulo(valor, compacto=False):

    valor_grados = _redondear(
        radianes_a_grados(valor)
    )

    texto = _formatear_numero(valor_grados)

    if compacto:
        return texto + "deg"

    return texto + " deg"


def _es_suma_resta(expresion):

    return (
        isinstance(expresion, Expresion)
        and expresion.operador in ("+", "-")
    )


def _unir_productos_compactos(izquierda, derecha):

    if len(izquierda) == 0:
        return derecha

    if len(derecha) == 0:
        return izquierda

    ultimo = izquierda[-1]
    primero = derecha[0]

    es_letra_ultimo = (
        ("a" <= ultimo <= "z")
        or ("A" <= ultimo <= "Z")
    )

    es_letra_primero = (
        ("a" <= primero <= "z")
        or ("A" <= primero <= "Z")
    )

    es_digito_ultimo = "0" <= ultimo <= "9"
    es_digito_primero = "0" <= primero <= "9"

    if (
        (es_letra_ultimo or es_digito_ultimo)
        and (es_letra_primero or es_digito_primero)
    ):
        return izquierda + "*" + derecha

    if primero == "-":
        return izquierda + "*" + derecha

    if ultimo == ")" and primero == "(":
        return izquierda + "*" + derecha

    return izquierda + derecha


def _renderizar_argumento_trig(
    expresion,
    mapa,
    compacto,
    grados
):
    """
    Formatea el argumento de Sin/Cos.

    En modo grados convierte únicamente las constantes
    que aparecen como términos aditivos.

    Los coeficientes de productos permanecen en su
    representación numérica original.
    """

    if not grados:
        return _renderizar(
            expresion,
            mapa,
            compacto,
            False
        )

    if es_numero(expresion):
        return _formatear_angulo(
            expresion,
            compacto
        )

    if isinstance(expresion, Expresion):

        operador = expresion.operador

        if operador == "+":

            izquierda = _renderizar_argumento_trig(
                expresion.izquierda,
                mapa,
                compacto,
                grados
            )

            derecha = _renderizar_argumento_trig(
                expresion.derecha,
                mapa,
                compacto,
                grados
            )

            separador = "+" if compacto else " + "

            return izquierda + separador + derecha

        if operador == "-":

            izquierda = _renderizar_argumento_trig(
                expresion.izquierda,
                mapa,
                compacto,
                grados
            )

            derecha = _renderizar_argumento_trig(
                expresion.derecha,
                mapa,
                compacto,
                grados
            )

            if _es_suma_resta(expresion.derecha):
                derecha = "(" + derecha + ")"

            separador = "-" if compacto else " - "

            return izquierda + separador + derecha

        if operador == "neg":

            izquierda = expresion.izquierda

            if es_numero(izquierda):
                return _formatear_angulo(
                    -izquierda,
                    compacto
                )

            texto = _renderizar_argumento_trig(
                izquierda,
                mapa,
                compacto,
                grados
            )

            if _es_suma_resta(izquierda):
                return "-(" + texto + ")"

            return "-" + texto

    # Los productos, coeficientes y potencias se
    # representan normalmente.
    return _renderizar(
        expresion,
        mapa,
        compacto,
        grados
    )


def _nombre_simbolico(expresion, mapa, compacto):

    if compacto:

        if expresion.nombre in mapa:
            return mapa[expresion.nombre]

        return expresion.nombre

    return str(expresion)


def _renderizar(
    expresion,
    mapa=None,
    compacto=False,
    grados=False
):

    if es_numero(expresion):
        return _formatear_numero(expresion)

    if isinstance(expresion, Syms):

        return _nombre_simbolico(
            expresion,
            mapa,
            compacto
        )

    if isinstance(expresion, Sin):

        argumento = _renderizar_argumento_trig(
            expresion.argumento,
            mapa,
            compacto,
            grados
        )

        nombre = "s" if compacto else "sin"

        return nombre + "(" + argumento + ")"

    if isinstance(expresion, Cos):

        argumento = _renderizar_argumento_trig(
            expresion.argumento,
            mapa,
            compacto,
            grados
        )

        nombre = "c" if compacto else "cos"

        return nombre + "(" + argumento + ")"

    if isinstance(expresion, Potencia):

        base = _renderizar(
            expresion.base,
            mapa,
            compacto,
            grados
        )

        exponente = _renderizar(
            expresion.exponente,
            mapa,
            compacto,
            grados
        )

        if isinstance(expresion.base, (Expresion, Potencia)):
            base = "(" + base + ")"

        elif es_numero(expresion.base) and expresion.base < 0:
            base = "(" + base + ")"

        if isinstance(expresion.exponente, (Expresion, Potencia)):
            exponente = "(" + exponente + ")"

        return base + "^" + exponente

    if isinstance(expresion, Expresion):

        operador = expresion.operador

        if operador == "neg":

            izquierda = expresion.izquierda

            texto = _renderizar(
                izquierda,
                mapa,
                compacto,
                grados
            )

            if _es_suma_resta(izquierda):
                return "-(" + texto + ")"

            return "-" + texto

        if operador == "*":

            izquierda = _renderizar(
                expresion.izquierda,
                mapa,
                compacto,
                grados
            )

            derecha = _renderizar(
                expresion.derecha,
                mapa,
                compacto,
                grados
            )

            if _es_suma_resta(expresion.izquierda):
                izquierda = "(" + izquierda + ")"

            if _es_suma_resta(expresion.derecha):
                derecha = "(" + derecha + ")"

            if compacto:
                return _unir_productos_compactos(
                    izquierda,
                    derecha
                )

            return izquierda + " * " + derecha

        izquierda = _renderizar(
            expresion.izquierda,
            mapa,
            compacto,
            grados
        )

        derecha = _renderizar(
            expresion.derecha,
            mapa,
            compacto,
            grados
        )

        if operador == "+":

            separador = "+" if compacto else " + "

            return izquierda + separador + derecha

        if operador == "-":

            if _es_suma_resta(expresion.derecha):
                derecha = "(" + derecha + ")"

            separador = "-" if compacto else " - "

            return izquierda + separador + derecha

    return str(expresion)


def texto_compacto(expresion, mapa=None, grados=False):

    if mapa is None:
        mapa = crear_mapa_compacto([expresion])

    return _renderizar(
        expresion,
        mapa,
        True,
        grados
    )


def texto_completo(expresion, grados=False):

    return _renderizar(
        expresion,
        None,
        False,
        grados
    )