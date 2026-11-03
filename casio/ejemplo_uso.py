from syms import Syms, grados, n, pi, crear_seno , crear_coseno, producto as pm, suma as sm
from rot import Des
from matriz import Matriz as mt
from jacobiano import Jacobiano 

theta1 = Syms("theta1")
theta2 = Syms("theta2")
d3 = Syms("d3")

l1 = Syms("l1")
l2 = Syms("l2")
l3 = Syms("l3")

DH = mt([[sm(n(90), theta1), l1, 0, n(grados(90))],
        [sm(n(90), theta2), 0, l2, n(grados(90))],
        [0, l3 + d3, 0, 0],])

T03 = Des.DH_table(DH)
T03_inv = Des.nsad()
T01 = Des.DH(sm(n(90), theta1), l1, 0, n(grados(90)))
T12 = Des.DH(sm(n(90), theta2), 0, l2, n(grados(90)))
T23 = Des.DH(0,l3+d3,0,0)
T01_inv=Des.H_inv(T01)
T01_inv.mostrar()
T12_inv=Des.H_inv(T12)
mt.p_m(T12_inv ,T01_inv,T03_inv).mostrar()

print("°")
