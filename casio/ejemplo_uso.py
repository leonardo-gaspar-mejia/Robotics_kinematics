from syms import Syms, grados, negativo, pi
from rot import Des
from matriz import Matriz

theta1 = Syms("theta1")
y = Syms("y")
z = Syms("z")

l1 = Syms("l1")
l2 = Syms("l2")
l3 = Syms("l3")

T01 = Des.Rot_lt(1,0,0,theta1).mostrar()

