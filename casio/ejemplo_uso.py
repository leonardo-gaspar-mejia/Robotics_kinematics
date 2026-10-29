from syms import Syms, grados, negativo, pi
from rot import Des
from matriz import Matriz

theta1 = Syms("theta1")
y = Syms("y")
z = Syms("z")

l1 = Syms("l1")
l2 = Syms("l2")
l3 = Syms("l3")

DH = Matriz([[0, l1, 0, grados(90)],
             [grados(90), l2, 0, grados(90)],
             [0, l3, 0, 0],])

T03 = Des.DH_table(DH, False)

T01 = Matriz([[1,0,0,0],
              [0,0,-1,0],
              [0,1,0,l1],
              [0,0,0,1],])

T01.mostrar()

T01.traspuesta().mostrar()