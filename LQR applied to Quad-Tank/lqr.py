import numpy as np
import random
import matplotlib.pyplot
import matplotlib.pyplot as plt
from lqrlib import lqr, dlqr
from numpy import linalg

""" SISTEMA """

x_nom = [22.5908, 20.1504, 2.5101, 4.4624]
u_nom = [166.67, 166.67]

A = np.matrix(
    [ [-0.0423, 0, 0.1268, 0],
      [0, -0.0448, 0, 0.0951],
      [0, 0, -0.1268, 0],
      [0, 0, 0, -0.0951]
     ])

B = np.matrix(
    [ [0.3183, 0],
      [0, 0.3183],
      [0, 0.2122],
      [0.2122, 0]
    ])

C = np.eye(4)
D = np.zeros((4,2))

""" PESOS """
Q = np.eye(4)
R = np.eye(2)

""" LQR """
K, S, E = dlqr(A,B,Q,R)

""" Control """
x = np.matrix([[10-x_nom[0]],
               [5-x_nom[1]],
               [10-x_nom[2]],
               [10-x_nom[3]]
               ]) # initial state
ref = np.matrix([[2],[3],[5],[10]])
cont = 0
record_x = []
record_u = []

while (cont < 1000):
    #u = np.matrix([[u1[cont]],[u2[cont]]])
    cont += 1
    x = x + (A-B*K)*x
    record_x.append(x)
    record_u.append(K*x)

x_for_plot = np.squeeze(record_x)
u_for_plot = np.squeeze(record_u)

plt.subplot(211)
plt.plot(np.add(x_for_plot.T[0], x_nom[0]))
plt.plot(np.add(x_for_plot.T[1], x_nom[1]))
plt.plot(np.add(x_for_plot.T[2], x_nom[2]))
plt.plot(np.add(x_for_plot.T[3], x_nom[3]))
plt.subplot(212)
plt.plot(np.add(u_for_plot.T[0], u_nom[0]))
plt.plot(np.add(u_for_plot.T[1], u_nom[1]))
plt.show()


    