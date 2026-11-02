from syms import Syms, grados, n, pi, crear_seno , crear_coseno, producto as pm 
from rot import Des
from matriz import Matriz as mt
from jacobiano import Jacobiano 

s = crear_seno
c = crear_coseno
theta1 = Syms("theta1")
theta2 = Syms("theta2")
d3 = Syms("d3")

l0 = Syms("l0")
l1 = Syms("l1")
l2 = Syms("l2")
l3 = Syms("l3")

DH = mt([[grados(30), 50, 35, 0],
             [grados(60), 0, 30, 0],
             [0, n(5 + 1.1), 0, 0],])

DH2 = mt([[grados(-84.914), 50, 35, 0],
             [grados(60), 0, 30, 0],
             [0, n(5 + 1.1), 0, 0],])

T03 = Des.DH_table(DH)
T03 = Des.DH_table(DH2)
T03_inv = Des.nsad()
T01 = Des.DH(theta1, l0, l1, 0)
T12 = Des.DH(theta2,0,l2,0)
T23 = Des.DH(0,n(l3+d3),0,0)
T01_inv=Des.H_inv(T01)
T01_inv.mostrar()
T12_inv=Des.H_inv(T12)
mt.p_m(T12_inv ,T01_inv,T03_inv).mostrar()

funciones = mt([
    [T03[0, 3]],
    [T03[1, 3]],
    [T03[2, 3]],
])

variables = mt([
    [theta1],
    [theta2],
    [d3],
])

J = Jacobiano(funciones, variables)

J.mostrar()

