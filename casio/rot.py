from matriz import Matriz
from syms import crear_seno, crear_coseno, negativo, crear_multiplicacion, crear_suma, crear_resta, grados, radianes_a_grados, grados
import math
class Des:

    def rotz(t):
        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [ct, negativo(st), 0, 0],
            [st, ct, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def rotz3(t):

        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [ct, negativo(st), 0],
            [st, ct, 0],
            [0, 0, 1]
        ])

    def rotx(t):
        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [1, 0, 0, 0],
            [0, ct, negativo(st), 0],
            [0, st, ct, 0],
            [0, 0, 0, 1]
        ])

    def rotx3(t):

        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [1, 0, 0],
            [0, ct, negativo(st)],
            [0, st, ct]
        ])

    def roty(t):
        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [ct, 0, st, 0],
            [0, 1, 0, 0],
            [negativo(st), 0, ct, 0],
            [0, 0, 0, 1]
        ])

    def roty3(t):

        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [ct, 0, st],
            [0, 1, 0],
            [negativo(st), 0, ct]
        ])

    def trans(x, y, z):

        X = x
        Y = y
        Z = z

        return Matriz([
            [1, 0, 0, X],
            [0, 1, 0, Y],
            [0, 0, 1, Z],
            [0, 0, 0, 1]
        ])

    def Rot_RPY(psi, theta, phi):

        return Matriz.p_m(Des.rotz3(psi), Des.roty3(theta), Des.rotx3(phi))

    def Rot_RPY_grados(phi, theta, psi):

        return Des.Rot_RPY(
            grados(phi),
            grados(theta),
            grados(psi)
        )

    def Rot_lt(lx, ly, lz, theta):

        ct = crear_coseno(theta)
        st = crear_seno(theta)

        vtheta = ct.__rsub__(1)

        return Matriz([
            [crear_suma(crear_multiplicacion(crear_multiplicacion(lx, lx), vtheta), ct), crear_resta(crear_multiplicacion(crear_multiplicacion(lx, ly), vtheta), crear_multiplicacion(lz, st)), crear_suma(crear_multiplicacion(crear_multiplicacion(lx, lz), vtheta), crear_multiplicacion(ly, st))],
            [crear_suma(crear_multiplicacion(crear_multiplicacion(lx, ly), vtheta), crear_multiplicacion(lz, st)), crear_suma(crear_multiplicacion(crear_multiplicacion(ly, ly), vtheta), ct), crear_resta(crear_multiplicacion(crear_multiplicacion(ly, lz), vtheta), crear_multiplicacion(lx, st))],
            [crear_resta(crear_multiplicacion(crear_multiplicacion(lx, lz), vtheta), crear_multiplicacion(ly, st)), crear_suma(crear_multiplicacion(crear_multiplicacion(ly, lz), vtheta), crear_multiplicacion(lx, st)), crear_suma(crear_multiplicacion(crear_multiplicacion(lz, lz), vtheta), ct)]
        ])

    def LT(H, mostrar=True):
        R = Matriz([
            [H[0, 0], H[0, 1], H[0, 2]],
            [H[1, 0], H[1, 1], H[1, 2]],
            [H[2, 0], H[2, 1], H[2, 2]]
        ])


        traza = R[0, 0] + R[1, 1] + R[2, 2]

        cos_theta = (traza - 1) / 2.0
        if cos_theta > 1:
            cos_theta = 1

        if cos_theta < -1:
            cos_theta = -1

        theta = math.acos(cos_theta)

        # Detectar theta = pi


        tolerancia = 1e-9

        tolerancia_imprimible = 1e-3

        

        if abs(cos_theta + 1) < tolerancia:

            # Caso especial:
            # theta = pi

            lx = math.sqrt((R[0, 0] + 1) / 2.0)
            ly = math.sqrt((R[1, 1] + 1) / 2.0)
            lz = math.sqrt((R[2, 2] + 1) / 2.0)

            print("CASO ESPECIAL: theta = pi o 180")
            print("Solo se obtienen magnitudes de lambda:")
            print("|lx| =", lx)
            print("|ly| =", ly)
            print("|lz| =", lz)
            print("Los signos deben determinarse aparte.")

            return lx, ly, lz, theta

        # . Caso general


        sin_theta = math.sin(theta)

        lx = (R[2, 1] - R[1, 2]) / (2.0 * sin_theta)

        ly = (R[0, 2] - R[2, 0]) / (2.0 * sin_theta)

        lz = (R[1, 0] - R[0, 1]) / (2.0 * sin_theta)

        theta_mostrar = theta

        if abs(theta_mostrar) < tolerancia_imprimible:
            theta_mostrar = 0.0

        print("Caso general:")
        print("lx =", lx)
        print("ly =", ly)
        print("lz =", lz)
        if mostrar:

            print("theta =", theta_mostrar)

        return lx, ly, lz, theta_mostrar


    def LT_grados(H):
        lx, ly, lz, theta = Des.LT(H, False)

        theta_grados = theta

        if abs(theta) < 1e-3:
           theta_grados = 0.0


        print("Theta =", radianes_a_grados(theta_grados), "grados")

        return lx, ly, lz, radianes_a_grados(theta_grados)


    def RPY(H, mostrar = True):

        R = Matriz([
            [H[0, 0], H[0, 1], H[0, 2]],
            [H[1, 0], H[1, 1], H[1, 2]],
            [H[2, 0], H[2, 1], H[2, 2]]
        ])

        # -----------------------------
        # Pitch
        # -----------------------------

        cos_theta = math.sqrt(
            R[0, 0] ** 2 +
            R[1, 0] ** 2
        )

        Pitch = math.atan2(
            -R[2, 0],
            cos_theta
        )

        # Tolerancia para detectar cos(theta) = 0
        tolerancia = 1e-8


        # Caso especial: theta = +90°


        if abs(cos_theta) < tolerancia:

            if R[2, 0] < 0:

                Roll = 0.0

                Yaw = math.atan2(
                    R[0, 1],
                    R[0, 2]
                )

            # Caso especial: theta = -90°
            
            else:

                # theta = -90°
                #
                # psi + phi = atan2(-R23, R22)

                Roll = 0.0

                Yaw = math.atan2(
                    -R[1, 2],
                    R[1, 1]
                )

        # -----------------------------
        # Caso general
        # -----------------------------

        else:

            Yaw = math.atan2(
                R[2, 1],
                R[2, 2]
            )

            Roll = math.atan2(
                R[1, 0],
                R[0, 0]
            )
        if mostrar:
                
            print("Roll: ", Roll)
            print("Pitch: ", Pitch)
            print("Yaw: ", Yaw)

        return Roll, Pitch, Yaw

    def RPY_grados(H):
        Roll, Pitch, Yaw = Des.RPY(H, False)

        print("Roll: ", radianes_a_grados(Roll))
        print("Pitch: ", radianes_a_grados(Pitch))
        print("Yaw: ", radianes_a_grados(Yaw))

    def camara(L, A, B):

        return Matriz.p_m(
            Des.rotz(A),
            Des.rotx(-grados(90) - B),
            Des.trans(0, 0, -L)
        )

    def camara_grados(L, A, B):

        return Des.camara(
            L,
            grados(A),
            grados(B)
        )

    def DH(theta,d,a,alpha):

        return(
            Matriz.p_m(Des.rotz(theta), Des.trans(a,0,d), Des.rotx(alpha))
        )

    def H_inv(H):

        R = Matriz([
            [H[0, 0], H[0, 1], H[0, 2]],
            [H[1, 0], H[1, 1], H[1, 2]],
            [H[2, 0], H[2, 1], H[2, 2]]
        ])

        d = Matriz([
            [H[0, 3]],
            [H[1, 3]],
            [H[2, 3]]
        ])

        RT = R.traspuesta()

        d_inv = Matriz.p_m(negativo(RT, d))

        return Matriz([
            [RT[0, 0], RT[0, 1], RT[0, 2], d_inv[0, 0]],
            [RT[1, 0], RT[1, 1], RT[1, 2], d_inv[1, 0]],
            [RT[2, 0], RT[2, 1], RT[2, 2], d_inv[2, 0]],
            [0,         0,         0,         1]
        ])

    def DH_table(DH_t, mostrar = True):

        if DH_t.columnas != 4:
            raise ValueError("La tabla DH carece de argumentos(Argumentos necesrios por fila 4)")

        T = Matriz([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

        t = []

        t_acumuladas = []

        for i in range(DH_t.filas):

            theta = DH_t[i, 0]
            d = DH_t[i, 1]
            a = DH_t[i, 2]
            alpha = DH_t[i, 3]

            T_i = Des.DH(theta, d, a, alpha)

            if mostrar:
                print("\nT" + str(i) + str(i + 1) + " =")
                T_i.mostrar()

            T = Matriz.p_m(T, T_i)

        if mostrar:
            print("\nT0" + str(DH_t.filas) + " =")
            T.mostrar()

        return T
