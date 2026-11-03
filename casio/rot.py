from matriz import Matriz
from syms import Syms, crear_seno, crear_coseno, n, crear_multiplicacion, crear_suma, crear_resta, grados, radianes_a_grados, grados
import math
class Des:

    def rotz(t):
        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [ct, n(st), 0, 0],
            [st, ct, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def rotz3(t):

        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [ct, n(st), 0],
            [st, ct, 0],
            [0, 0, 1]
        ])

    def rotx(t):
        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [1, 0, 0, 0],
            [0, ct, n(st), 0],
            [0, st, ct, 0],
            [0, 0, 0, 1]
        ])

    def rotx3(t):

        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [1, 0, 0],
            [0, ct, n(st)],
            [0, st, ct]
        ])

    def roty(t):
        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [ct, 0, st, 0],
            [0, 1, 0, 0],
            [n(st), 0, ct, 0],
            [0, 0, 0, 1]
        ])

    def roty3(t):

        ct = crear_coseno(t)
        st = crear_seno(t)

        return Matriz([
            [ct, 0, st],
            [0, 1, 0],
            [n(st), 0, ct]
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

    def Rot_RPY(phi, theta, psi):

        return Matriz.p_m(Des.rotz3(phi), Des.roty3(theta), Des.rotx3(psi))

    def Rot_RPY_grados(phi, theta, psi):

        return Des.Rot_RPY(
            grados(phi),
            grados(theta),
            grados(psi)
        )

    def Rot_lt(lx, ly, lz, theta):

        ct = crear_coseno(theta)
        st = crear_seno(theta)

        vtheta =  crear_resta(1, ct)

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

        vx = R[2, 1] - R[1, 2]
        vy = R[0, 2] - R[2, 0]
        vz = R[1, 0] - R[0, 1]

        sin_theta = math.sqrt(vx**2 + vy**2 + vz**2) / 2.0

        theta = math.atan2(sin_theta, cos_theta)

        tolerancia = 1e-9

        # Caso especial: rotacion nula
        if theta <= tolerancia:

            if mostrar:
                print("Rotacion nula")

            return 0.0, 0.0, 0.0, theta

        if abs(cos_theta + 1) < tolerancia:

            # Caso especial: theta = pi

            dx = (R[0, 0] + 1) / 2.0
            dy = (R[1, 1] + 1) / 2.0
            dz = (R[2, 2] + 1) / 2.0

            # Elegir el componente de mayor magnitud
            # para evitar divisiones entre valores cercanos a cero.

            if dx >= dy and dx >= dz:

                lx = math.sqrt(max(0.0, dx))

                ly = (R[0, 1] + R[1, 0]) / (4.0 * lx)
                lz = (R[0, 2] + R[2, 0]) / (4.0 * lx)

            elif dy >= dz:

                ly = math.sqrt(max(0.0, dy))

                lx = (R[0, 1] + R[1, 0]) / (4.0 * ly)
                lz = (R[1, 2] + R[2, 1]) / (4.0 * ly)

            else:

                lz = math.sqrt(max(0.0, dz))

                lx = (R[0, 2] + R[2, 0]) / (4.0 * lz)
                ly = (R[1, 2] + R[2, 1]) / (4.0 * lz)

            # Normalizar para compensar errores numericos
            norma = math.sqrt(lx**2 + ly**2 + lz**2)

            lx /= norma
            ly /= norma
            lz /= norma

            if mostrar:
                print("Caso especial: theta = pi")
                print("lx =", lx)
                print("ly =", ly)
                print("lz =", lz)

            return lx, ly, lz, theta

        # Caso general
        denominador = 2.0 * sin_theta

        lx = vx / denominador
        ly = vy / denominador
        lz = vz / denominador

        if mostrar:
            print("Caso general:")
            print("lx =", lx)
            print("ly =", ly)
            print("lz =", lz)
            print("theta =", theta)

        return lx, ly, lz, theta


    def LT_grados(H):

        lx, ly, lz, theta = Des.LT(H, False)

        theta_grados = radianes_a_grados(theta)

        print("Theta =", theta_grados, "grados")

        return lx, ly, lz, theta_grados


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

        roll_grados = radianes_a_grados(Roll)
        pitch_grados = radianes_a_grados(Pitch)
        yaw_grados = radianes_a_grados(Yaw)

        print("Roll: ", roll_grados)
        print("Pitch: ", pitch_grados)
        print("Yaw: ", yaw_grados)

        return roll_grados, pitch_grados, yaw_grados

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
            [n(H[0, 3])],
            [n(H[1, 3])],
            [n(H[2, 3])]
        ])

        RT = R.traspuesta()

        d_inv = Matriz.p_m(RT, d)

        return Matriz([
            [RT[0, 0], RT[0, 1], RT[0, 2], d_inv[0, 0]],
            [RT[1, 0], RT[1, 1], RT[1, 2], d_inv[1, 0]],
            [RT[2, 0], RT[2, 1], RT[2, 2], d_inv[2, 0]],
            [0,         0,         0,         1]
        ])

    def DH_table(DH_t, grados=False ,mostrar = True):

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
                T_i.mostrar(grados)

            T = Matriz.p_m(T, T_i)

        if mostrar:
            print("\nT0" + str(DH_t.filas) + " =")
            T.mostrar(grados)

        return T

    def nsad():

        nx = Syms("nx")
        ny = Syms("ny")
        nz = Syms("nz")

        sx = Syms("sx")
        sy = Syms("sy")
        sz = Syms("sz")

        ax = Syms("ax")
        ay = Syms("ay")
        az = Syms("az")

        dx = Syms("dx")
        dy = Syms("dy")
        dz = Syms("dz")


        return Matriz([
            [nx, sx, ax, dx],
            [ny, sy, ay, dy],
            [nz, sz, az, dz],
            [0, 0, 0, 1]
        ])
