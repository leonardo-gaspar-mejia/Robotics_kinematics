from syms import (
    Syms,
    Sin,
    Cos,
    Potencia,
    Expresion,
    es_numero
)

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


def _compacto_parentesis_suma(expresion, mapa):

    if isinstance(expresion, Expresion):

        if (
            expresion.operador == "+"
            or expresion.operador == "-"
        ):
            return (
                "("
                + texto_compacto(expresion, mapa)
                + ")"
            )

    return texto_compacto(
        expresion,
        mapa
    )


def _unir_productos_compactos(izquierda, derecha):

    if len(izquierda) == 0:
        return derecha

    if len(derecha) == 0:
        return izquierda

    ultimo = izquierda[-1]
    primero = derecha[0]

    es_letra_ultimo = (('a' <= ultimo <= 'z') or ('A' <= ultimo <= 'Z'))
    es_letra_primero = (('a' <= primero <= 'z') or ('A' <= primero <= 'Z'))

    es_digito_ultimo = '0' <= ultimo <= '9'
    es_digito_primero = '0' <= primero <= '9'


    if ((es_letra_ultimo or es_digito_ultimo) and (es_letra_primero or es_digito_primero)):
        return izquierda + "*" + derecha

    if primero == "-":
        return izquierda + "*" + derecha

    if ultimo == ")" and primero == "(":
        return izquierda + "*" + derecha

    return izquierda + derecha


def texto_compacto(expresion, mapa=None):

    if mapa is None:
        mapa = crear_mapa_compacto(
            [expresion]
        )

    if es_numero(expresion):
        return str(expresion)

    if isinstance(expresion, Syms):

        if expresion.nombre in mapa:
            return mapa[expresion.nombre]

        return expresion.nombre

    if isinstance(expresion, Sin):

        return (
            "s("
            + texto_compacto(
                expresion.argumento,
                mapa
            )
            + ")"
        )

    if isinstance(expresion, Cos):

        return (
            "c("
            + texto_compacto(
                expresion.argumento,
                mapa
            )
            + ")"
        )

    if isinstance(expresion, Potencia):

        base_texto = _compacto_base_potencia(
            expresion.base,
            mapa
        )

        exponente_texto = _compacto_exponente_potencia(
            expresion.exponente,
            mapa
        )

        return base_texto + "^" + exponente_texto

    if isinstance(expresion, Expresion):

        if expresion.operador == "neg":

            izquierda = expresion.izquierda

            if isinstance(izquierda, Expresion):

                if (
                    izquierda.operador == "+"
                    or izquierda.operador == "-"
                ):

                    return (
                        "-("
                        + texto_compacto(
                            izquierda,
                            mapa
                        )
                        + ")"
                    )

            return (
                "-"
                + texto_compacto(
                    izquierda,
                    mapa
                )
            )

        if expresion.operador == "*":

            izquierda = _compacto_parentesis_suma(
                expresion.izquierda,
                mapa
            )

            derecha = _compacto_parentesis_suma(
                expresion.derecha,
                mapa
            )

            return _unir_productos_compactos(
                izquierda,
                derecha
            )

        if expresion.operador == "+":

            return (
                texto_compacto(
                    expresion.izquierda,
                    mapa
                )
                + "+"
                + texto_compacto(
                    expresion.derecha,
                    mapa
                )
            )

        if expresion.operador == "-":

            izquierda = texto_compacto(
                expresion.izquierda,
                mapa
            )

            derecha = texto_compacto(
                expresion.derecha,
                mapa
            )

            if isinstance(
                expresion.derecha,
                Expresion
            ):

                if (
                    expresion.derecha.operador == "+"
                    or expresion.derecha.operador == "-"
                ):

                    derecha = (
                        "("
                        + derecha
                        + ")"
                    )

            return (
                izquierda
                + "-"
                + derecha
            )

    return str(expresion)

def _compacto_base_potencia(expresion, mapa):

    texto = texto_compacto(expresion, mapa)

    if isinstance(expresion, (Expresion, Potencia)):
        return "(" + texto + ")"

    if es_numero(expresion) and expresion < 0:
        return "(" + texto + ")"

    return texto


def _compacto_exponente_potencia(expresion, mapa):

    texto = texto_compacto(expresion, mapa)

    if isinstance(expresion, (Expresion, Potencia)):
        return "(" + texto + ")"

    return texto