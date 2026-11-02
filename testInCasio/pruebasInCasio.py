# Colocar este archivo junto a matriz.py, syms.py, formato.py y rot.py.
# Ejecutar en fx-CG50. No requiere pytest ni librerias externas.
# Se puede borrar este archivo de la calculadora si todas las pruebas pasan.

import math

from matriz import Matriz, MAX_FILA_NIVEL0
from rot import Des
from derivadas import Derivador
from jacobiano import Jacobiano
from syms import ( Syms, Expresion, Potencia, crear_seno, crear_coseno, crear_suma, crear_resta,
 crear_multiplicacion, crear_negativo, producto, suma, grados, evaluar, n)
from formato import texto_compacto


resultados = []


def verificar(condicion, mensaje):
    if not condicion:
        raise AssertionError(mensaje)


def cerca(a, b, tolerancia=1e-5):
    return abs(a - b) <= tolerancia


def matrices_cerca(A, B, tolerancia=1e-5):
    if A.filas != B.filas or A.columnas != B.columnas:
        return False

    for i in range(A.filas):
        for j in range(A.columnas):
            if abs(A[i, j] - B[i, j]) > tolerancia:
                return False

    return True


def ejecutar(nombre, funcion):
    try:
        funcion()
        resultados.append(True)
        print("[OK]", nombre)
    except Exception as error:
        resultados.append(False)
        print("[FALLO]", nombre, "-", str(error))


# ------------------------------------------------------------
# 1. Multiplicacion de matrices por escalares numericos
# ------------------------------------------------------------
def prueba_escalar_numerico():
    M = Matriz([
        [1, 2],
        [3, 4]
    ])

    izquierda = producto(2, M)
    derecha = producto(M, 2)

    verificar(izquierda[0, 0] == 2, "2*M: elemento [0,0]")
    verificar(izquierda[1, 1] == 8, "2*M: elemento [1,1]")
    verificar(derecha[0, 1] == 4, "M*2: elemento [0,1]")
    verificar(derecha[1, 0] == 6, "M*2: elemento [1,0]")
    verificar(M[0, 0] == 1 and M[1, 1] == 4,
              "La matriz original fue modificada")


# ------------------------------------------------------------
# 2. Multiplicacion de matrices por escalares simbolicos
# ------------------------------------------------------------
def prueba_escalar_simbolico():
    x = Syms("x")
    a = Syms("a")
    M = Matriz([
        [x, 2],
        [0, 3]
    ])

    derecha = producto(M, a)
    izquierda = producto(a, M)

    verificar(str(derecha[0, 0]) == "x * a",
              "M*a no produjo x*a")
    verificar(str(derecha[0, 1]) == "2 * a",
              "M*a no produjo 2*a")
    verificar(str(izquierda[0, 0]) == "a * x",
              "a*M no produjo a*x")
    verificar(str(izquierda[1, 1]) == "3 * a",
              "a*M no produjo 3*a")

    por_x = producto(x, M)
    verificar(str(por_x[0, 0]) == "x^2",
              "x*M no delego la operacion a Matriz")


# ------------------------------------------------------------
# 3. Multiplicacion matricial convencional
# ------------------------------------------------------------
def prueba_producto_matricial():
    A = Matriz([
        [1, 2],
        [3, 4]
    ])
    B = Matriz([
        [2, 0],
        [1, 2]
    ])

    C = Matriz.p_m(A, B)

    verificar(C[0, 0] == 4, "Producto matricial [0,0]")
    verificar(C[0, 1] == 4, "Producto matricial [0,1]")
    verificar(C[1, 0] == 10, "Producto matricial [1,0]")
    verificar(C[1, 1] == 8, "Producto matricial [1,1]")


# ------------------------------------------------------------
# 4. Igualdad estructural de matrices
# ------------------------------------------------------------
def prueba_igualdad_matrices():
    x1 = Syms("x", "x")
    x2 = Syms("x", "q1")
    y1 = Syms("y", "x")
    y2 = Syms("y", "y")
    z = Syms("z", "y")

    A = Matriz([
        [x1, 2],
        [3, y1]
    ])
    B = Matriz([
        [x2, 2],
        [3, y2]
    ])
    C = Matriz([
        [x2, 2],
        [3, z]
    ])

    verificar(A == B,
              "Matrices estructuralmente iguales no coinciden")
    verificar(not (A == C),
              "Se confundieron dos variables distintas")
    verificar(not (A == Matriz([[x1, 2]])),
              "No detecto dimensiones diferentes")
    verificar(Matriz([[1]]) == Matriz([[1.0]]),
              "No reconocio 1 y 1.0 como iguales")
    verificar(not (A == [[x1, 2], [3, y1]]),
              "Una lista no debe considerarse una Matriz")


# ------------------------------------------------------------
# 5. Negacion unaria de expresiones simbolicas
# ------------------------------------------------------------
def prueba_negacion_simbolica():
    x = Syms("x")
    y = Syms("y")

    negativo = n(x)
    doble_negativo = n(negativo)
    negativo_suma = n(x + y)

    verificar(str(negativo) == "-x",
              "-x tiene representacion incorrecta")
    verificar(doble_negativo is x,
              "-(-x) no recupero x")
    verificar(str(negativo_suma) == "-x - y",
              "La negacion de una suma es incorrecta")


# ------------------------------------------------------------
# 6. Comparacion estructural y simplificacion simbolica
# ------------------------------------------------------------
def prueba_motor_simbolico():
    x = Syms("x")
    y = Syms("y")

    x1 = Syms("q1", "q1")
    x2 = Syms("q1", "theta1")
    y1 = Syms("variable_a", "q")
    y2 = Syms("variable_b", "q")

    verificar(crear_resta(x1, x2) == 0,
              "No reconocio simbolos con el mismo nombre interno")

    pitagoras_incorrecto = crear_suma(
        Potencia(crear_seno(y1), 2),
        Potencia(crear_coseno(y2), 2)
    )
    verificar(pitagoras_incorrecto != 1,
              "Confundio variables distintas en identidad pitagorica")

    pitagoras = crear_suma(
        Potencia(crear_seno(x), 2),
        Potencia(crear_coseno(Syms("x")), 2)
    )
    verificar(pitagoras == 1,
              "No simplifico sen(x)^2 + cos(x)^2")

    terminos = suma(
        producto(2, x, y),
        producto(3, y, x)
    )
    verificar(str(terminos) == "5 * x * y",
              "No agrupo factores conmutados")

    A = Syms("A")
    B = Syms("B")

    coseno_suma = crear_suma(
        crear_multiplicacion(crear_coseno(A), crear_coseno(B)),
        crear_negativo(
            crear_multiplicacion(crear_seno(A), crear_seno(B))
        )
    )
    seno_suma = crear_suma(
        crear_multiplicacion(crear_seno(A), crear_coseno(B)),
        crear_multiplicacion(crear_coseno(A), crear_seno(B))
    )

    verificar(str(coseno_suma) == "cos(A + B)",
              "Fallo identidad del coseno de una suma")
    verificar(str(seno_suma) == "sin(A + B)",
              "Fallo identidad del seno de una suma")


# ------------------------------------------------------------
# 7. Matriz.simplificar_m()
# ------------------------------------------------------------
def prueba_matriz_simplificar():
    x = Syms("x")

    identidad = Expresion(
        "+",
        Potencia(crear_seno(x), 2),
        Potencia(crear_coseno(x), 2)
    )
    suma_con_cero = Expresion("+", x, 0)

    original = Matriz([
        [identidad, suma_con_cero],
        [suma_con_cero, 2]
    ])

    resultado = original.simplificar_m()

    verificar(resultado is not original,
              "simplificar_m() debe devolver una matriz nueva")
    verificar(resultado[0, 0] == 1,
              "No simplifico identidad trigonometrica")
    verificar(resultado[0, 1] is x,
              "No simplifico x + 0")
    verificar(resultado[1, 0] is x,
              "No simplifico la segunda aparicion de x + 0")
    verificar(resultado[1, 1] == 2,
              "Modifico un elemento numerico")
    verificar(original[0, 0] is identidad,
              "simplificar_m() modifico la matriz original")
    verificar(original[0, 1] is suma_con_cero,
              "simplificar_m() modifico la expresion original")


# ------------------------------------------------------------
# 8. Formato compacto y longitudes de filas
# ------------------------------------------------------------
def prueba_formato_compacto():
    l1 = Syms("l1")
    l2 = Syms("l2")
    x = Syms("x")
    y = Syms("y")
    theta1 = Syms("theta1")
    theta2 = Syms("theta2")

    texto_1 = texto_compacto(producto(l1, l2))
    texto_2 = texto_compacto(producto(Potencia(x, 2), y))
    texto_3 = texto_compacto(producto(theta1, crear_coseno(theta2)))

    verificar(texto_1 == "l1*l2", "Formato compacto de l1*l2")
    verificar(texto_2 == "x^2*y", "Formato compacto de x^2*y")
    verificar(texto_3 == "t1*c(t2)", "Formato compacto de t1*c(t2)")

    M = Matriz([
        [1, 22, 333],
        [4444, 55, 6]
    ])

    completos = M._textos_completos()
    compactos = M._textos_compactos()

    for i in range(M.filas):
        longitud_real = len(M._fila_nivel0(completos, i))
        longitud_calculada = M._longitud_fila_nivel0(completos, i)
        verificar(longitud_real == longitud_calculada,
                  "Longitud incorrecta en nivel 0, fila " + str(i))

        longitud_real = len(M._fila_compacta(compactos, i))
        longitud_calculada = M._longitud_fila_compacta(compactos, i)
        verificar(longitud_real == longitud_calculada,
                  "Longitud incorrecta en nivel 1, fila " + str(i))


# ------------------------------------------------------------
# 9. Cambio automatico a nivel compacto (nivel 1)
# ------------------------------------------------------------
def prueba_cambio_nivel_presentacion():
    elementos = []
    for i in range(1, 71):
        elementos.append(Syms("theta" + str(i)))

    M = Matriz([elementos])
    completos = M._textos_completos()
    compactos = M._textos_compactos()

    largo_nivel0 = M._longitud_fila_nivel0(completos, 0)
    largo_nivel1 = M._longitud_fila_compacta(compactos, 0)

    verificar(largo_nivel0 > MAX_FILA_NIVEL0,
              "La prueba no alcanzo el limite del nivel 0")
    verificar(largo_nivel1 <= MAX_FILA_NIVEL0,
              "La representacion compacta no redujo la fila")

    print("   Longitud nivel 0:", largo_nivel0)
    print("   Longitud nivel 1:", largo_nivel1)
    print("   Salida compacta esperada:")
    M.mostrar()


# ------------------------------------------------------------
# 10. Rot_lt: forma numerica y simbolica
# ------------------------------------------------------------
def prueba_rot_lt():
    theta = 0.5
    R = Des.Rot_lt(1, 0, 0, theta)

    verificar(R.filas == 3 and R.columnas == 3,
              "Rot_lt no genero una matriz 3x3")
    verificar(cerca(R[0, 0], 1.0), "Rot_lt elemento [0,0]")
    verificar(cerca(R[1, 1], math.cos(theta)), "Rot_lt coseno")
    verificar(cerca(R[1, 2], -math.sin(theta)), "Rot_lt seno negativo")
    verificar(cerca(R[2, 1], math.sin(theta)), "Rot_lt seno positivo")

    angulo_simbolico = Syms("theta")
    Rs = Des.Rot_lt(1, 0, 0, angulo_simbolico)
    verificar(Rs.filas == 3 and Rs.columnas == 3,
              "Rot_lt no acepto un angulo simbolico")

    Rs_simplificada = Rs.simplificar_m()
    verificar(Rs_simplificada[0, 0] == 1,
              "No simplifico la expresion de Rot_lt")


# ------------------------------------------------------------
# 11. LT: identidad y angulo pequeno
# ------------------------------------------------------------
def prueba_lt_identidad_y_angulo_pequeno():
    I = Matriz([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ])

    eje_x, eje_y, eje_z, theta = Des.LT(I, False)
    verificar(eje_x == 0 and eje_y == 0 and eje_z == 0 and theta == 0,
              "LT no identifico la matriz identidad")

    angulo = 0.0005
    R = Des.rotx3(angulo)
    lx, ly, lz, theta = Des.LT(R, False)

    verificar(cerca(theta, angulo, 1e-5),
              "LT altero el angulo pequeno")
    verificar(cerca(lx, 1.0), "LT eje X para angulo pequeno")
    verificar(cerca(ly, 0.0), "LT eje Y para angulo pequeno")
    verificar(cerca(lz, 0.0), "LT eje Z para angulo pequeno")


# ------------------------------------------------------------
# 12. LT: reconstruccion de rotacion general
# ------------------------------------------------------------
def prueba_lt_reconstruccion_general():
    norma = math.sqrt(14.0)
    lx = 1.0 / norma
    ly = -2.0 / norma
    lz = 3.0 / norma
    angulo = 0.73

    original = Des.Rot_lt(lx, ly, lz, angulo)
    lx2, ly2, lz2, theta2 = Des.LT(original, False)
    reconstruida = Des.Rot_lt(lx2, ly2, lz2, theta2)

    verificar(cerca(theta2, angulo),
              "LT no recupero el angulo")
    verificar(matrices_cerca(original, reconstruida),
              "La reconstruccion eje-angula no coincide")


# ------------------------------------------------------------
# 13. LT: reconstruccion a 180 grados
# ------------------------------------------------------------
def prueba_lt_reconstruccion_180():
    norma = math.sqrt(14.0)
    original = Des.Rot_lt(
        1.0 / norma,
        -2.0 / norma,
        3.0 / norma,
        math.pi
    )

    lx, ly, lz, theta = Des.LT(original, False)
    reconstruida = Des.Rot_lt(lx, ly, lz, theta)

    verificar(cerca(theta, math.pi, 1e-5),
              "LT no recupero el angulo de 180 grados")
    verificar(matrices_cerca(original, reconstruida, 1e-5),
              "No reconstruyo el eje a 180 grados")


# ------------------------------------------------------------
# 14. LT_grados
# ------------------------------------------------------------
def prueba_lt_grados():
    angulo = 0.0005
    R = Des.rotx3(angulo)
    lx, ly, lz, theta_grados = Des.LT_grados(R)
    esperado = angulo * 180.0 / math.pi

    verificar(cerca(theta_grados, esperado, 1e-7),
              "LT_grados altero el angulo pequeno")
    verificar(cerca(lx, 1.0) and cerca(ly, 0.0) and cerca(lz, 0.0),
              "LT_grados no recupero el eje")


# ------------------------------------------------------------
# 15. RPY: caso general y conversion a grados
# ------------------------------------------------------------
def prueba_rpy_caso_general():
    phi = grados(30)
    theta = grados(20)
    psi = grados(40)

    R = Des.Rot_RPY(phi, theta, psi)
    phi2, theta2, psi2 = Des.RPY(R, False)

    verificar(cerca(phi2, phi), "RPY no recupero phi")
    verificar(cerca(theta2, theta), "RPY no recupero theta")
    verificar(cerca(psi2, psi), "RPY no recupero psi")

    reconstruida = Des.Rot_RPY(phi2, theta2, psi2)
    verificar(matrices_cerca(R, reconstruida),
              "RPY no reconstruyo la matriz original")

    R_grados = Des.Rot_RPY_grados(30, 20, 40)
    verificar(matrices_cerca(R, R_grados),
              "Rot_RPY_grados no coincide con Rot_RPY")


# ------------------------------------------------------------
# 16. RPY: bloqueo de cardan
# ------------------------------------------------------------
def prueba_rpy_bloqueo_gimbal():
    phi = grados(30)
    psi = grados(40)

    for theta in (math.pi / 2.0, -math.pi / 2.0):
        original = Des.Rot_RPY(phi, theta, psi)
        phi2, theta2, psi2 = Des.RPY(original, False)
        reconstruida = Des.Rot_RPY(phi2, theta2, psi2)

        verificar(matrices_cerca(original, reconstruida, 1e-5),
                  "RPY fallo en bloqueo de cardan")


# ------------------------------------------------------------
# 17. Operaciones matriciales y validacion de dimensiones
# ------------------------------------------------------------
def prueba_operaciones_matriciales():
    A = Matriz([
        [1, 2, 3],
        [4, 5, 6]
    ])
    B = Matriz([
        [6, 5, 4],
        [3, 2, 1]
    ])

    C = A + B
    D = A - B

    verificar(C == Matriz([[7, 7, 7], [7, 7, 7]]),
              "Suma matricial incorrecta")
    verificar(D == Matriz([[-5, -3, -1], [1, 3, 5]]),
              "Resta matricial incorrecta")

    AT = A.traspuesta()
    verificar(AT.filas == 3 and AT.columnas == 2,
              "Dimensiones incorrectas de la traspuesta")
    verificar(AT == Matriz([[1, 4], [2, 5], [3, 6]]),
              "Traspuesta incorrecta")

    error_suma = False
    try:
        A + Matriz([[1, 2]])
    except ValueError:
        error_suma = True
    verificar(error_suma, "Acepto suma con dimensiones incompatibles")

    error_producto = False
    try:
        Matriz.p_m(A, Matriz([[1, 2], [3, 4]]))
    except ValueError:
        error_producto = True
    verificar(error_producto,
              "Acepto producto con dimensiones incompatibles")

    error_constructor = False
    try:
        Matriz([[1, 2], [3]])
    except ValueError:
        error_constructor = True
    verificar(error_constructor,
              "Acepto filas con diferente numero de columnas")


# ------------------------------------------------------------
# 18. Determinantes numericos y simbolicos
# ------------------------------------------------------------
def prueba_determinantes():
    A = Matriz([[7]])
    verificar(A.determinante() == 7,
              "Determinante 1x1 incorrecto")

    B = Matriz([
        [1, 2],
        [3, 4]
    ])
    verificar(B.determinante() == -2,
              "Determinante 2x2 incorrecto")

    C = Matriz([
        [6, 1, 1],
        [4, -2, 5],
        [2, 8, 7]
    ])
    verificar(C.determinante() == -306,
              "Determinante 3x3 incorrecto")

    D = Matriz([
        [1, 2, 3],
        [1, 2, 3],
        [4, 5, 6]
    ])
    verificar(D.determinante() == 0,
              "No detecto determinante nulo")

    x = Syms("x")
    E = Matriz([
        [x, 1],
        [2, 3]
    ])
    resultado = evaluar(E.determinante(), {"x": 4})
    verificar(cerca(resultado, 10),
              "Determinante simbolico incorrecto")

    F = Matriz([
        [1, 2, 3],
        [4, 5, 6]
    ])
    error_no_cuadrada = False
    try:
        F.determinante()
    except ValueError:
        error_no_cuadrada = True
    verificar(error_no_cuadrada,
              "Acepto determinante de matriz no cuadrada")


# ------------------------------------------------------------
# 19. Evaluacion simbolica y sustitucion numerica
# ------------------------------------------------------------
def prueba_evaluacion_simbolica():
    x = Syms("x")
    y = Syms("y")

    expresion = crear_suma(
        producto(2, x),
        crear_seno(y)
    )
    resultado = evaluar(
        expresion,
        {"x": 3, "y": math.pi / 2.0}
    )
    verificar(cerca(resultado, 7),
              "Evaluacion con varias variables incorrecta")

    potencia = Potencia(x, 3)
    verificar(evaluar(potencia, {"x": 2}) == 8,
              "Evaluacion de potencia incorrecta")

    matriz = Matriz([
        [x, crear_seno(y)],
        [producto(x, y), Potencia(x, 2)]
    ])
    numerica = matriz.evaluar_numerico(
        {"x": 2, "y": math.pi / 2.0}
    )
    esperado = Matriz([
        [2, 1],
        [math.pi, 4]
    ])
    verificar(matrices_cerca(numerica, esperado),
              "Evaluacion numerica de matriz incorrecta")

    error_variable = False
    try:
        evaluar(x, {})
    except ValueError:
        error_variable = True
    verificar(error_variable,
              "No detecto variable sin valor asignado")


# ------------------------------------------------------------
# 20. Reglas de derivacion
# ------------------------------------------------------------
def prueba_derivadas():
    x = Syms("x")
    y = Syms("y")

    verificar(Derivador(5).derivar(x) == 0,
              "Derivada de constante incorrecta")
    verificar(Derivador(x).derivar(x) == 1,
              "Derivada de variable incorrecta")

    derivada_potencia = Derivador(Potencia(x, 3)).derivar(x)
    verificar(cerca(evaluar(derivada_potencia, {"x": 2}), 12),
              "Regla de potencia incorrecta")

    suma_expr = crear_suma(Potencia(x, 2), x)
    derivada_suma = Derivador(suma_expr).derivar(x)
    verificar(cerca(evaluar(derivada_suma, {"x": 2}), 5),
              "Regla de suma incorrecta")

    producto_expr = producto(x, crear_seno(x))
    derivada_producto = Derivador(producto_expr).derivar(x)
    valor_x = 0.4
    esperado_producto = (
        math.sin(valor_x)
        + valor_x * math.cos(valor_x)
    )
    obtenido_producto = evaluar(
        derivada_producto,
        {"x": valor_x}
    )
    verificar(cerca(obtenido_producto, esperado_producto),
              "Regla del producto incorrecta")

    derivada_seno = Derivador(crear_seno(x)).derivar(x)
    verificar(cerca(
        evaluar(derivada_seno, {"x": valor_x}),
        math.cos(valor_x)
    ), "Derivada de seno incorrecta")

    derivada_coseno = Derivador(crear_coseno(x)).derivar(x)
    verificar(cerca(
        evaluar(derivada_coseno, {"x": valor_x}),
        -math.sin(valor_x)
    ), "Derivada de coseno incorrecta")

    cadena_expr = crear_seno(Potencia(x, 2))
    derivada_cadena = Derivador(cadena_expr).derivar(x)
    esperado_cadena = 2 * valor_x * math.cos(valor_x ** 2)
    obtenido_cadena = evaluar(
        derivada_cadena,
        {"x": valor_x}
    )
    verificar(cerca(obtenido_cadena, esperado_cadena),
              "Regla de la cadena incorrecta")

    error_exponente = False
    try:
        Derivador(Potencia(x, y)).derivar(x)
    except TypeError:
        error_exponente = True
    verificar(error_exponente,
              "No rechazo exponente simbolico no soportado")


# ------------------------------------------------------------
# 21. Jacobiano y validacion de vectores columna
# ------------------------------------------------------------
def prueba_jacobiano():
    x = Syms("x")
    y = Syms("y")

    f1 = crear_suma(Potencia(x, 2), y)
    f2 = producto(x, y)

    funciones = Matriz([
        [f1],
        [f2]
    ])
    variables = Matriz([
        [x],
        [y]
    ])

    J = Jacobiano(funciones, variables)
    esperado = Matriz([
        [4, 1],
        [3, 2]
    ])

    verificar(J.filas == 2 and J.columnas == 2,
              "Dimensiones incorrectas del Jacobiano")
    verificar(J.evaluar_numerico({"x": 2, "y": 3}) == esperado,
              "Valores del Jacobiano incorrectos")

    error_funciones = False
    try:
        Jacobiano(Matriz([[x, y]]), variables)
    except ValueError:
        error_funciones = True
    verificar(error_funciones,
              "Acepto funciones que no son vector columna")

    error_variables = False
    try:
        Jacobiano(funciones, Matriz([[x, y]]))
    except ValueError:
        error_variables = True
    verificar(error_variables,
              "Acepto variables que no son vector columna")


# ------------------------------------------------------------
# 22. Rotaciones y transformaciones DH
# ------------------------------------------------------------
def prueba_rotaciones_y_dh():
    Rz = Des.rotz3(math.pi / 2.0)
    verificar(cerca(Rz[0, 0], 0), "Rotacion Z [0,0]")
    verificar(cerca(Rz[0, 1], -1), "Rotacion Z [0,1]")
    verificar(cerca(Rz[1, 0], 1), "Rotacion Z [1,0]")
    verificar(cerca(Rz[1, 1], 0), "Rotacion Z [1,1]")

    Rx0 = Des.rotx3(0)
    verificar(Rx0 == Matriz([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]), "Rotacion X identidad incorrecta")

    H = Des.DH(0, 3, 2, 0)
    esperado = Matriz([
        [1, 0, 0, 2],
        [0, 1, 0, 0],
        [0, 0, 1, 3],
        [0, 0, 0, 1]
    ])
    verificar(H.filas == 4 and H.columnas == 4,
              "DH no genero matriz 4x4")
    verificar(matrices_cerca(H, esperado),
              "Transformacion DH simple incorrecta")

    tabla = Matriz([
        [0, 0, 2, 0],
        [0, 0, 3, 0]
    ])
    T02 = Des.DH_table(tabla, False)
    verificar(cerca(T02[0, 3], 5),
              "DH_table no acumulo las traslaciones")
    verificar(cerca(T02[1, 3], 0),
              "DH_table genero desplazamiento Y inesperado")
    verificar(T02[3, 3] == 1,
              "DH_table genero una transformacion invalida")

    error_tabla = False
    try:
        Des.DH_table(Matriz([[0, 0, 1]]), False)
    except ValueError:
        error_tabla = True
    verificar(error_tabla,
              "DH_table acepto una tabla con columnas incorrectas")


# ------------------------------------------------------------
# 23. Inversa de transformacion homogenea
# ------------------------------------------------------------
def prueba_inversa_homogenea():
    H = Des.DH(
        grados(30),
        2,
        3,
        grados(-20)
    )
    H_inv = Des.H_inv(H)

    identidad = Matriz([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    producto_1 = Matriz.p_m(H, H_inv)
    producto_2 = Matriz.p_m(H_inv, H)

    verificar(matrices_cerca(producto_1, identidad),
              "H * H_inv no produjo identidad")
    verificar(matrices_cerca(producto_2, identidad),
              "H_inv * H no produjo identidad")


# ------------------------------------------------------------
# 24. Integracion: manipulador planar RR de dos articulaciones
# ------------------------------------------------------------
def prueba_manipulador_2r():
    q1 = Syms("q1")
    q2 = Syms("q2")
    l1 = Syms("l1")
    l2 = Syms("l2")

    tabla_DH = Matriz([
        [q1, 0, l1, 0],
        [q2, 0, l2, 0]
    ])

    T02 = Des.DH_table(tabla_DH, False)

    verificar(T02.filas == 4 and T02.columnas == 4,
              "Cinematica directa no genero una matriz 4x4")

    posicion = Matriz([
        [T02[0, 3]],
        [T02[1, 3]]
    ])
    variables = Matriz([
        [q1],
        [q2]
    ])

    J = Jacobiano(posicion, variables)

    valores = {
        "q1": math.pi / 2.0,
        "q2": 0,
        "l1": 2,
        "l2": 1
    }

    posicion_numerica = posicion.evaluar_numerico(valores)
    J_numerico = J.evaluar_numerico(valores)

    verificar(cerca(posicion_numerica[0, 0], 0),
              "Posicion X del manipulador 2R incorrecta")
    verificar(cerca(posicion_numerica[1, 0], 3),
              "Posicion Y del manipulador 2R incorrecta")

    esperado_J = Matriz([
        [-3, -1],
        [0, 0]
    ])
    verificar(matrices_cerca(J_numerico, esperado_J),
              "Jacobiano numerico del manipulador 2R incorrecto")


# ------------------------------------------------------------
# Ejecutar todas las pruebas
# ------------------------------------------------------------
print("")
print("========================================")
print(" PRUEBAS DE REGRESION - ROBOTICS TOOLBOX")
print("========================================")

pruebas = [
    ("Multiplicacion escalar numerica", prueba_escalar_numerico),
    ("Multiplicacion escalar simbolica", prueba_escalar_simbolico),
    ("Producto matricial convencional", prueba_producto_matricial),
    ("Igualdad estructural de matrices", prueba_igualdad_matrices),
    ("Negacion unaria simbolica", prueba_negacion_simbolica),
    ("Motor simbolico e identidades", prueba_motor_simbolico),
    ("Matriz.simplificar_m()", prueba_matriz_simplificar),
    ("Formato compacto y longitudes", prueba_formato_compacto),
    ("Cambio automatico a nivel 1", prueba_cambio_nivel_presentacion),
    ("Rot_lt numerico y simbolico", prueba_rot_lt),
    ("LT identidad y angulo pequeno", prueba_lt_identidad_y_angulo_pequeno),
    ("LT reconstruccion general", prueba_lt_reconstruccion_general),
    ("LT reconstruccion a 180 grados", prueba_lt_reconstruccion_180),
    ("LT_grados conserva angulos pequenos", prueba_lt_grados),
    ("RPY caso general y conversion a grados", prueba_rpy_caso_general),
    ("RPY en bloqueo de cardan", prueba_rpy_bloqueo_gimbal),
    ("Operaciones matriciales y dimensiones", prueba_operaciones_matriciales),
    ("Determinantes numericos y simbolicos", prueba_determinantes),
    ("Evaluacion simbolica", prueba_evaluacion_simbolica),
    ("Reglas de derivacion", prueba_derivadas),
    ("Jacobiano", prueba_jacobiano),
    ("Rotaciones y transformaciones DH", prueba_rotaciones_y_dh),
    ("Inversa homogenea", prueba_inversa_homogenea),
    ("Integracion de manipulador 2R", prueba_manipulador_2r),
]

for nombre, funcion in pruebas:
    ejecutar(nombre, funcion)

aprobadas = 0
for resultado in resultados:
    if resultado:
        aprobadas += 1

print("")
print("========================================")
print("RESULTADO:", aprobadas, "de", len(resultados), "pruebas aprobadas")

if aprobadas == len(resultados):
    print("ESTADO: TODAS LAS PRUEBAS APROBADAS")
else:
    print("ESTADO: HAY PRUEBAS FALLIDAS")

print("========================================")
