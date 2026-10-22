import math

pi = math.pi

class ExpresionSimbolica:

    def __add__(self, otra):
        return crear_suma(self, otra)

    def __radd__(self, otra):
        return crear_suma(otra, self)

    def __sub__(self, otra):
        return crear_resta(self, otra)

    def __rsub__(self, otra):
        return crear_resta(otra, self)

    def __mul__(self, otra):
        return crear_multiplicacion(self, otra)

    def __rmul__(self, otra):
        return crear_multiplicacion(otra, self)


def negativo(expresion):
    return crear_negativo(expresion)


class Syms(ExpresionSimbolica):

    def __init__(self, nombre, simbolo=None):
        self.nombre = nombre
        self.simbolo = simbolo if simbolo is not None else nombre

    def __str__(self):
        return self.simbolo


def _con_parentesis_si_es_suma(expresion):
    """
    Texto de 'expresion', entre parentesis si es un '+' o un '-' (una
    suma no puede meterse tal cual dentro de una negacion o de un
    producto sin parentesis: perderia su agrupacion y el texto
    impreso significaria otra cosa distinta de lo que realmente vale).
    """

    if isinstance(expresion, Expresion) and expresion.operador in ("+", "-"):
        return "(" + str(expresion) + ")"

    return str(expresion)


class Expresion(ExpresionSimbolica):

    def __init__(self, operador, izquierda, derecha=None):
        self.operador = operador
        self.izquierda = izquierda
        self.derecha = derecha

    def __str__(self):
        if self.operador == "neg":
            return "-" + _con_parentesis_si_es_suma(self.izquierda)

        if self.operador == "*":
            return (
                _con_parentesis_si_es_suma(self.izquierda)
                + " * "
                + _con_parentesis_si_es_suma(self.derecha)
            )

        if self.operador == "-":
            # a - (b + c) y a - (b - c) necesitan parentesis: sin ellos
            # "a - b + c" y "a - b - c" quieren decir otra cosa.
            return (
                str(self.izquierda)
                + " - "
                + _con_parentesis_si_es_suma(self.derecha)
            )

        # "+"
        return str(self.izquierda) + " + " + str(self.derecha)

def grados(valor_en_grados):
    
    return valor_en_grados * math.pi / 180


def radianes_a_grados(valor_en_radianes):
    return valor_en_radianes * 180 / math.pi


def mostrar_deg(valor_en_radianes):

    print(str(_redondear(radianes_a_grados(valor_en_radianes))) + " grados")


def _redondear(valor):

    redondeado = round(valor, 10)

    if redondeado == int(redondeado):
        return int(redondeado)

    return redondeado

def crear_seno(argumento):
    """Sin(x) toma el argumento numerico en RADIANES (convencion estandar)."""

    if es_numero(argumento):
        return _redondear(math.sin(argumento))

    return Sin(argumento)

def crear_coseno(argumento):
    """Version coseno de crear_seno(). Ver ese docstring."""

    if es_numero(argumento):
        return _redondear(math.cos(argumento))

    return Cos(argumento)


class Sin(ExpresionSimbolica):

    def __init__(self, argumento):
        self.argumento = argumento

    def __str__(self):
        return "sin(" + str(self.argumento) + ")"


class Cos(ExpresionSimbolica):

    def __init__(self, argumento):
        self.argumento = argumento

    def __str__(self):
        return "cos(" + str(self.argumento) + ")"


class Potencia(ExpresionSimbolica):


    def __init__(self, base, exponente):
        self.base = base
        self.exponente = exponente

    def __str__(self):
        return str(self.base) + "^" + str(self.exponente)


def evaluar(expresion, valores=None):
    """
    Sustituye cada Syms por un numero y reduce toda la expresion a un
    unico numero ('valores' es un diccionario {nombre: numero}, en
    grados para los angulos que entren a Sin/Cos). Sirve tanto para
    obtener un resultado final en la calculadora como para verificar
    con casos concretos que una identidad simbolica es correcta.
    """

    if valores is None:
        valores = {}

    if es_numero(expresion):
        return expresion

    if isinstance(expresion, Syms):
        if expresion.nombre in valores:
            return valores[expresion.nombre]
        raise ValueError("Falta el valor de '" + expresion.nombre + "'")

    if isinstance(expresion, Potencia):
        base = evaluar(expresion.base, valores)
        return base ** expresion.exponente

    if isinstance(expresion, Sin):
        return crear_seno(evaluar(expresion.argumento, valores))

    if isinstance(expresion, Cos):
        return crear_coseno(evaluar(expresion.argumento, valores))

    if isinstance(expresion, Expresion):
        if expresion.operador == "neg":
            return -evaluar(expresion.izquierda, valores)

        izquierda = evaluar(expresion.izquierda, valores)
        derecha = evaluar(expresion.derecha, valores)

        if expresion.operador == "+":
            return izquierda + derecha
        if expresion.operador == "-":
            return izquierda - derecha
        if expresion.operador == "*":
            return izquierda * derecha

    raise TypeError("No se pudo evaluar: " + str(expresion))


def es_numero(valor):
    return isinstance(valor, (int, float))


def es_cero(valor):
    return isinstance(valor, (int, float)) and valor == 0


def es_uno(valor):
    return isinstance(valor, (int, float)) and valor == 1



def crear_negativo(expresion):

    if es_numero(expresion):
        return -expresion

    if isinstance(expresion, Expresion):

        if expresion.operador == "neg":
            return expresion.izquierda

        # -(A + B) = -A - B ; -(A - B) = B - A
        # Repartir el signo aqui evita que mas adelante un '*' o una
        # nueva negacion tengan que cargar con una suma completa sin
        # parentesis.
        if expresion.operador == "+":
            return crear_resta(
                crear_negativo(expresion.izquierda),
                expresion.derecha
            )

        if expresion.operador == "-":
            return crear_resta(
                expresion.derecha,
                expresion.izquierda
            )

    return Expresion("neg", expresion)


def _extraer_signo(expresion):
    """
    Devuelve (signo, expresion_sin_signo) con signo en {1, -1}.

    Tanto un '-' simbolico (neg) como un numero negativo cuentan como
    signo -1: para el signo de un termino da lo mismo que el -1 venga
    envuelto en un nodo 'neg' o sea, por ejemplo, el -1 que produce
    sin(-90 grados).
    """

    if isinstance(expresion, Expresion) and expresion.operador == "neg":
        return (-1, expresion.izquierda)

    if es_numero(expresion) and expresion < 0:
        return (-1, -expresion)

    return (1, expresion)

def _descomponer_producto(valor):
    """
    Separa un termino en:
    signo, coeficiente numerico y factores.

    El orden de los factores no importa al comparar productos.
    """

    # -x
    if isinstance(valor, Expresion) and valor.operador == "neg":
        signo, coeficiente, factores = _descomponer_producto(
            valor.izquierda
        )

        return -signo, coeficiente, factores

    # x * y
    if isinstance(valor, Expresion) and valor.operador == "*":
        signo1, coef1, factores1 = _descomponer_producto(
            valor.izquierda
        )

        signo2, coef2, factores2 = _descomponer_producto(
            valor.derecha
        )

        return (
            signo1 * signo2,
            coef1 * coef2,
            factores1 + factores2
        )

    # Numero
    if es_numero(valor):

        if valor < 0:
            return -1, -valor, []

        return 1, valor, []

    # Factor simbolico
    return 1, 1, [valor]


def _claves_factores(factores):

    claves = []

    for factor in factores:
        claves.append(str(factor))

    claves.sort()

    return claves


def _terminos_equivalentes(a, b):

    signo_a, coef_a, factores_a = _descomponer_producto(a)
    signo_b, coef_b, factores_b = _descomponer_producto(b)

    return (
        signo_a == signo_b
        and coef_a == coef_b
        and _claves_factores(factores_a)
            == _claves_factores(factores_b)
    )


def _terminos_opuestos(a, b):

    signo_a, coef_a, factores_a = _descomponer_producto(a)
    signo_b, coef_b, factores_b = _descomponer_producto(b)

    return (
        signo_a == -signo_b
        and coef_a == coef_b
        and _claves_factores(factores_a)
            == _claves_factores(factores_b)
    )


def _extraer_cuadrado_trig(factores):

    for i in range(len(factores)):

        factor = factores[i]

        if (
            isinstance(factor, Potencia)
            and factor.exponente == 2
            and isinstance(factor.base, (Sin, Cos))
        ):

            restantes = factores[:i] + factores[i + 1:]

            return (
                type(factor.base),
                factor.base.argumento,
                restantes
            )

    for i in range(len(factores)):

        primero = factores[i]

        if not isinstance(primero, (Sin, Cos)):
            continue

        for j in range(i + 1, len(factores)):

            segundo = factores[j]

            if (
                type(primero) == type(segundo)
                and str(primero.argumento)
                == str(segundo.argumento)
            ):

                restantes = []

                for k in range(len(factores)):

                    if k != i and k != j:
                        restantes.append(factores[k])

                return (
                    type(primero),
                    primero.argumento,
                    restantes
                )

    return None


def _identidad_pitagoras_factorizada(a, b):


    signo_a, coef_a, factores_a = _descomponer_producto(a)
    signo_b, coef_b, factores_b = _descomponer_producto(b)

    if signo_a != signo_b or coef_a != coef_b:
        return None

    info_a = _extraer_cuadrado_trig(factores_a)
    info_b = _extraer_cuadrado_trig(factores_b)

    if info_a is None or info_b is None:
        return None

    tipo_a, argumento_a, restantes_a = info_a
    tipo_b, argumento_b, restantes_b = info_b

    # Uno debe ser seno y el otro coseno
    if tipo_a == tipo_b:
        return None

    if str(argumento_a) != str(argumento_b):
        return None

    # El resto de los factores debe ser igual
    if (
        _claves_factores(restantes_a)
        != _claves_factores(restantes_b)
    ):
        return None

    resultado = coef_a

    for factor in restantes_a:
        resultado = crear_multiplicacion(
            resultado,
            factor
        )

    if signo_a < 0:
        resultado = crear_negativo(resultado)

    return resultado


def _es_potencia_trig(valor, tipo):
    return (
        isinstance(valor, Potencia)
        and isinstance(valor.base, tipo)
        and valor.exponente == 2
    )


def _identidad_pitagoras(a, b):
    """sin(x)^2 + cos(x)^2 -> 1 (en cualquier orden)."""

    if _es_potencia_trig(a, Sin) and _es_potencia_trig(b, Cos):
        if str(a.base.argumento) == str(b.base.argumento):
            return 1

    if _es_potencia_trig(a, Cos) and _es_potencia_trig(b, Sin):
        if str(a.base.argumento) == str(b.base.argumento):
            return 1

    return None


def _pares_de_trig(factores):

    indices = []

    for i in range(len(factores)):
        factor = factores[i]

        if isinstance(factor, (Sin, Cos)):
            indices.append(i)
    return [
        (indices[p], indices[q])
        for p in range(len(indices))
        for q in range(p + 1, len(indices))
    ]


def _sin_indices(factores, i, j):

    restantes = []
    
    for k in range(len(factores)):
        if k != i and k != j:
            restantes.append(factores[k])

    return restantes


def _mismo_par(p, q, r, s):
    sp, sq, sr, ss = str(p), str(q), str(r), str(s)
    return (sp == sr and sq == ss) or (sp == ss and sq == sr)


def _suma_trig_canonica(a, b):
    """Construye A+B con un orden estable para que el resultado se lea igual."""

    if str(a) <= str(b):
        return crear_suma(a, b)

    return crear_suma(b, a)


def _cos_suma_resta(info_a, info_b, combinar):
    """
    Identidad del coseno de suma/resta, combinando un termino cos*cos con
    uno sin*sin. 'combinar' indica si se quiere la version P1 - P2
    (crear_resta) o P1 + P2 (crear_suma), donde P1 = info_a, P2 = info_b.
    """

    cos_cos_a = info_a[0] is Cos and info_a[2] is Cos
    sin_sin_a = info_a[0] is Sin and info_a[2] is Sin
    cos_cos_b = info_b[0] is Cos and info_b[2] is Cos
    sin_sin_b = info_b[0] is Sin and info_b[2] is Sin

    if cos_cos_a and sin_sin_b:
        p, q = info_a[1], info_a[3]
        r, s = info_b[1], info_b[3]

        if _mismo_par(p, q, r, s):
            if combinar is crear_resta:
                return Cos(_suma_trig_canonica(p, q))
            return Cos(crear_resta(p, q))

    if sin_sin_a and cos_cos_b:
        r, s = info_a[1], info_a[3]
        p, q = info_b[1], info_b[3]

        if _mismo_par(p, q, r, s):
            if combinar is crear_resta:
                return crear_negativo(Cos(_suma_trig_canonica(p, q)))
            return Cos(crear_resta(p, q))

    return None


def _sin_suma_resta(info_a, info_b, combinar):


    mixto_a = (info_a[0] is Sin and info_a[2] is Cos) or (
        info_a[0] is Cos and info_a[2] is Sin
    )
    mixto_b = (info_b[0] is Sin and info_b[2] is Cos) or (
        info_b[0] is Cos and info_b[2] is Sin
    )

    if not (mixto_a and mixto_b):
        return None

    if info_a[0] is Sin:
        sin_a, cos_a = info_a[1], info_a[3]
    else:
        sin_a, cos_a = info_a[3], info_a[1]

    if info_b[0] is Sin:
        sin_b, cos_b = info_b[1], info_b[3]
    else:
        sin_b, cos_b = info_b[3], info_b[1]

    if str(sin_a) == str(cos_b) and str(cos_a) == str(sin_b):
        if combinar is crear_suma:
            return Sin(_suma_trig_canonica(sin_a, cos_a))
        return Sin(crear_resta(sin_a, cos_a))

    return None


def _identidad_suma_angulos(a, b, combinar):
    """
    Busca en a y b (cada uno, en general, coeficiente * varios
    factores) dos factores trigonometricos que formen un
    cos(A)cos(B) +/- sin(A)sin(B) o un sin(A)cos(B) +/- cos(A)sin(B),
    con el resto de los factores igual en a y en b (ese resto se
    arrastra como factor comun del resultado). Por eso no alcanza con
    mirar el primer par de factores trig que aparezca: se prueban
    todas las combinaciones hasta encontrar una que realmente
    combine, porque el par que sirve puede no ser el primero.
    """

    signo_a, coef_a, factores_a = _descomponer_producto(a)
    signo_b, coef_b, factores_b = _descomponer_producto(b)

    if coef_a != coef_b:
        return None

    pares_a = _pares_de_trig(factores_a)
    pares_b = _pares_de_trig(factores_b)

    if not pares_a or not pares_b:
        return None

    operacion_efectiva = 1 if combinar is crear_suma else -1
    signo_relativo = signo_a * operacion_efectiva * signo_b

    combinar_normalizado = crear_suma if signo_relativo == 1 else crear_resta

    for i_a, j_a in pares_a:

        primero_a, segundo_a = factores_a[i_a], factores_a[j_a]
        restantes_a = _sin_indices(factores_a, i_a, j_a)
        claves_restantes_a = _claves_factores(restantes_a)

        info_a = (
            type(primero_a), primero_a.argumento,
            type(segundo_a), segundo_a.argumento,
        )

        for i_b, j_b in pares_b:

            restantes_b = _sin_indices(factores_b, i_b, j_b)

            if claves_restantes_a != _claves_factores(restantes_b):
                continue

            primero_b, segundo_b = factores_b[i_b], factores_b[j_b]

            info_b = (
                type(primero_b), primero_b.argumento,
                type(segundo_b), segundo_b.argumento,
            )

            resultado = _cos_suma_resta(info_a, info_b, combinar_normalizado)

            if resultado is None:
                resultado = _sin_suma_resta(
                    info_a, info_b, combinar_normalizado
                )

            if resultado is None:
                continue

            for factor in restantes_a:
                resultado = crear_multiplicacion(resultado, factor)

            if coef_a != 1:
                resultado = crear_multiplicacion(coef_a, resultado)

            if signo_a == -1:
                return crear_negativo(resultado)

            return resultado

    return None


def crear_suma(a, b):

    if es_numero(a) and es_numero(b):
        return a + b

    if es_cero(a):
        return b

    if es_cero(b):
        return a

    # a + (-b) -> a - b   ;   (-a) + b -> b - a
    if isinstance(b, Expresion) and b.operador == "neg":
        return crear_resta(a, b.izquierda)

    if _terminos_opuestos(a, b):
        return 0

    pitagoras = _identidad_pitagoras_factorizada(a, b)

    if pitagoras is not None:
        return pitagoras

    if isinstance(a, Expresion) and a.operador == "neg":
        return crear_resta(b, a.izquierda)

    pitagoras = _identidad_pitagoras(a, b)
    if pitagoras is not None:
        return pitagoras

    angulo = _identidad_suma_angulos(a, b, crear_suma)
    if angulo is not None:
        return angulo

    return Expresion("+", a, b)


def crear_resta(a, b):

    if es_numero(a) and es_numero(b):
        return a - b

    if es_cero(b):
        return a

    if es_cero(a):
        return crear_negativo(b)

    if str(a) == str(b):
        return 0

    # a - (-b) -> a + b
    if isinstance(b, Expresion) and b.operador == "neg":
        return crear_suma(a, b.izquierda)

    if _terminos_equivalentes(a, b):
        return 0

    angulo = _identidad_suma_angulos(a, b, crear_resta)
    if angulo is not None:
        return angulo

    return Expresion("-", a, b)


def _potencia_info(valor):
    if isinstance(valor, Potencia):
        return (valor.base, valor.exponente)

    if isinstance(valor, (Sin, Cos)):
        return (valor, 1)

    return None


def _mismo_termino(x, y):
    if type(x) != type(y):
        return False

    if isinstance(x, (Sin, Cos)):
        return str(x.argumento) == str(y.argumento)

    return str(x) == str(y)


def es_multiplicacion(expresion):
    return (
        isinstance(expresion, Expresion)
        and expresion.operador == "*"
    )


MAX_TERMINOS_EXPANSION = 16


def _cantidad_terminos(expresion, limite=MAX_TERMINOS_EXPANSION + 1):
    """Cuenta terminos aditivos sin dejar que el conteo crezca demasiado."""

    if isinstance(expresion, Expresion):
        if expresion.operador in ("+", "-"):
            izquierda = _cantidad_terminos(expresion.izquierda, limite)
            if izquierda >= limite:
                return limite

            derecha = _cantidad_terminos(expresion.derecha, limite - izquierda)
            total = izquierda + derecha

            if total >= limite:
                return limite

            return total

        if expresion.operador == "neg":
            return _cantidad_terminos(expresion.izquierda, limite)

    return 1


def _terminos_aditivos(expresion, signo=1, salida=None):
    """Devuelve una suma como lista de (signo, termino)."""

    if salida is None:
        salida = []

    if isinstance(expresion, Expresion):
        if expresion.operador == "+":
            _terminos_aditivos(expresion.izquierda, signo, salida)
            _terminos_aditivos(expresion.derecha, signo, salida)
            return salida

        if expresion.operador == "-":
            _terminos_aditivos(expresion.izquierda, signo, salida)
            _terminos_aditivos(expresion.derecha, -signo, salida)
            return salida

        if expresion.operador == "neg":
            _terminos_aditivos(expresion.izquierda, -signo, salida)
            return salida

    salida.append((signo, expresion))
    return salida


def _producto_distribuido(a, b):
    """Distribuye a*b una sola vez, evitando expansion recursiva."""

    cantidad_a = _cantidad_terminos(a)
    cantidad_b = _cantidad_terminos(b)

    if cantidad_a * cantidad_b > MAX_TERMINOS_EXPANSION:
        return None

    terminos_a = _terminos_aditivos(a)
    terminos_b = _terminos_aditivos(b)

    resultado = None

    for signo_a, termino_a in terminos_a:
        for signo_b, termino_b in terminos_b:
            termino = crear_multiplicacion(termino_a, termino_b)

            if signo_a * signo_b == -1:
                termino = crear_negativo(termino)

            if resultado is None:
                resultado = termino
            else:
                resultado = crear_suma(resultado, termino)

    return resultado


def crear_multiplicacion(a, b):

    # Numerico por numerico
    if es_numero(a) and es_numero(b):
        return a * b

    # Cero
    if es_cero(a) or es_cero(b):
        return 0

    # Uno
    if es_uno(a):
        return b

    if es_uno(b):
        return a

    # Signos: se normalizan antes de seguir trabajando.
    signo_a, a_sin_signo = _extraer_signo(a)
    signo_b, b_sin_signo = _extraer_signo(b)

    if signo_a == -1 or signo_b == -1:
        resultado = crear_multiplicacion(a_sin_signo, b_sin_signo)

        if signo_a * signo_b == -1:
            return crear_negativo(resultado)

        return resultado

    a = a_sin_signo
    b = b_sin_signo

    # sin(x) * sin(x) -> sin(x)^2
    # cos(x) * cos(x) -> cos(x)^2
    if str(a) == str(b):
        if isinstance(a, (Sin, Cos)):
            return Potencia(a, 2)

    # Si uno de los factores es una suma/resta, se intenta distribuir
    # solamente cuando la expansion sigue siendo manejable.
    es_suma_a = isinstance(a, Expresion) and a.operador in ("+", "-")
    es_suma_b = isinstance(b, Expresion) and b.operador in ("+", "-")

    if es_suma_a or es_suma_b:
        expandido = _producto_distribuido(a, b)

        if expandido is not None:
            return expandido

        # Si la expansion superaria el limite, se conserva la forma factorizada.
        return Expresion("*", a, b)

    # Combinar factor numerico dentro de una multiplicacion.
    if es_multiplicacion(a) and es_numero(b):
        izquierda = a.izquierda
        derecha = a.derecha

        if es_numero(izquierda):
            return crear_multiplicacion(izquierda * b, derecha)

        if es_numero(derecha):
            return crear_multiplicacion(izquierda, derecha * b)

    if es_multiplicacion(b) and es_numero(a):
        izquierda = b.izquierda
        derecha = b.derecha

        if es_numero(izquierda):
            return crear_multiplicacion(a * izquierda, derecha)

        if es_numero(derecha):
            return crear_multiplicacion(izquierda, a * derecha)

    return Expresion("*", a, b)


def simplificar(expresion):

    # Los numeros y simbolos ya estan en forma simple.
    if not isinstance(expresion, (Expresion, Sin, Cos, Potencia)):
        return expresion

    # Negacion
    if isinstance(expresion, Expresion) and expresion.operador == "neg":
        izquierda = simplificar(expresion.izquierda)

        if es_cero(izquierda):
            return 0

        return crear_negativo(izquierda)

    # Potencia: solo se simplifica el interior de la base.
    if isinstance(expresion, Potencia):
        base = simplificar(expresion.base)
        return Potencia(base, expresion.exponente)

    # Sin
    if isinstance(expresion, Sin):
        argumento = simplificar(expresion.argumento)

        if es_cero(argumento):
            return 0

        if isinstance(argumento, Expresion):
            if argumento.operador == "neg":
                return negativo(Sin(argumento.izquierda))

        return Sin(argumento)

    # Cos
    if isinstance(expresion, Cos):
        argumento = simplificar(expresion.argumento)

        if es_cero(argumento):
            return 1

        if isinstance(argumento, Expresion):
            if argumento.operador == "neg":
                return Cos(argumento.izquierda)

        return Cos(argumento)

    # Expresiones binarias
    izquierda = simplificar(expresion.izquierda)
    derecha = simplificar(expresion.derecha)

    if expresion.operador == "+":
        return crear_suma(izquierda, derecha)

    if expresion.operador == "-":
        return crear_resta(izquierda, derecha)

    if expresion.operador == "*":
        return crear_multiplicacion(izquierda, derecha)


def _combinar(izquierda, derecha, operacion):

    directo = "__" + operacion + "__"
    reflejo = "__r" + operacion + "__"


    if isinstance(izquierda, ExpresionSimbolica):
        return getattr(izquierda, directo)(derecha)

    if isinstance(derecha, ExpresionSimbolica):
        return getattr(derecha, reflejo)(izquierda)

    if operacion == "add":
        return izquierda + derecha

    if operacion == "sub":
        return izquierda - derecha

    if operacion == "mul":
        return izquierda * derecha

    raise ValueError("Operacion no soportada: " + operacion)


def producto(*elementos):

    if len(elementos) == 0:
        return None

    resultado = elementos[0]

    for elemento in elementos[1:]:
        resultado = _combinar(resultado, elemento, "mul")

    return resultado


def _aplanar_suma(valor, signo, salida):

    if isinstance(valor, Expresion):

        if valor.operador == "+":

            _aplanar_suma(
                valor.izquierda,
                signo,
                salida
            )

            _aplanar_suma(
                valor.derecha,
                signo,
                salida
            )

            return

        if valor.operador == "-":

            _aplanar_suma(
                valor.izquierda,
                signo,
                salida
            )

            _aplanar_suma(
                valor.derecha,
                -signo,
                salida
            )

            return

        if valor.operador == "neg":

            _aplanar_suma(
                valor.izquierda,
                -signo,
                salida
            )

            return

    salida.append((signo, valor))

def _combinar_terminos_si_se_puede(x, y):

    if es_numero(x) and es_numero(y):
        return x + y

    if es_cero(x):
        return y

    if es_cero(y):
        return x

    if _terminos_opuestos(x, y):
        return 0

    pitagoras = _identidad_pitagoras_factorizada(x, y)
    if pitagoras is not None:
        return pitagoras

    pitagoras = _identidad_pitagoras(x, y)
    if pitagoras is not None:
        return pitagoras

    return _identidad_suma_angulos(x, y, crear_suma)


def suma(*elementos):

    if len(elementos) == 0:
        return None

    terminos = []

    for elemento in elementos:
        _aplanar_suma(
            elemento,
            1,
            terminos
        )

    pendientes = []

    for signo, termino in terminos:

        if es_cero(termino):
            continue

        pendientes.append(
            termino if signo == 1 else crear_negativo(termino)
        )

    if len(pendientes) == 0:
        return 0

    while len(pendientes) > 1:

        se_fusionaron_dos = False

        for i in range(len(pendientes)):

            for j in range(i + 1, len(pendientes)):

                fusion = _combinar_terminos_si_se_puede(
                    pendientes[i], pendientes[j]
                )

                if fusion is not None:

                    pendientes = [
                        pendientes[k]
                        for k in range(len(pendientes))
                        if k != i and k != j
                    ]

                    pendientes.append(fusion)

                    se_fusionaron_dos = True
                    break

            if se_fusionaron_dos:
                break

        if not se_fusionaron_dos:
            break

    if len(pendientes) == 0:
        return 0

    resultado = pendientes[0]

    for termino in pendientes[1:]:
        resultado = crear_suma(resultado, termino)

    return resultado


def resta(*elementos):

    if len(elementos) == 0:
        return None

    resultado = elementos[0]

    for elemento in elementos[1:]:
        resultado = _combinar(resultado, elemento, "sub")

    return resultado