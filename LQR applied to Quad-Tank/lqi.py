import numpy as np
import random
import matplotlib.pyplot
import matplotlib.pyplot as plt
from lqrlib import lqr, dlqr
from scipy.signal import StateSpace

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


C = np.matrix([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
             ])
#C = np.concatenate((C,np.zeros((4,4))),axis=1)
D = np.zeros((2,2))

top = np.concatenate((A,np.zeros((4,2))),axis=1)
bottom = np.concatenate((-C, np.zeros((2,2))),axis=1)
Ahat = np.concatenate((top,bottom), axis=0)
Bhat = np.concatenate((B,np.zeros((2,2))),axis=0)
Q = np.diag([1, 1, .0000001, .0000001, 1, 1])*np.eye(6)
R = np.eye(2)

sys = StateSpace(Ahat, Bhat, np.concatenate((C,np.zeros((2,2))),axis=1), D)
#sys_d = sys.to_discrete(1)
#Ahat, Bhat = sys_d.A, sys_d.B

K, S, E = lqr(Ahat,Bhat,Q,R)

""" Control """
x = np.matrix([[1],[-1],[2],[3],[0],[0]]) # initial state
ref = np.matrix([[0],[0]])
cont = 0
record_x = []
record_u = []
record_SP = []

y = [[0], [0]]
e_dot = [[0], [0], [0], [0]]
xsi = 0
w = 0

while (cont < 1000):
    
    cont += 1
    if (cont >= 50 and cont <= 100):
        ref = np.matrix([[1],[0]])
    elif (cont > 100 and cont <= 200):
        ref = np.matrix([[0],[1]])
    elif (cont > 200 and cont <= 300):
        ref = np.matrix([[2],[0]])
    elif (cont > 300 and cont <= 500):
        ref = np.matrix([[0],[2]])
    elif (cont > 500):
        ref = np.matrix([[-1],[-2]])
        
    xsi = np.add(xsi, np.subtract(ref, y))
    aux = np.dot(K.T[4:].T,xsi)
    u = - K*x - aux 
    x = Ahat*x + Bhat*u
    
    record_x.append(x)
    record_u.append(u)
    record_SP.append(ref)
    y = np.dot(C,x[:4])
    
x_for_plot = np.squeeze(record_x)
u_for_plot = np.squeeze(record_u)
SP_for_plot = np.squeeze(record_SP)

plt.subplot(211)
plt.plot(np.add(x_for_plot.T[0], x_nom[0]))
plt.plot(np.add(x_for_plot.T[1], x_nom[1]))
plt.plot(np.add(x_for_plot.T[2], x_nom[2]))
plt.plot(np.add(x_for_plot.T[3], x_nom[3]))
plt.plot(np.add(SP_for_plot.T[0], x_nom[0]), '--',linewidth=.5)
plt.plot(np.add(SP_for_plot.T[1], x_nom[1]), '--',linewidth=.5)
plt.subplot(212)
plt.plot(np.add(u_for_plot.T[0], u_nom[0]))
plt.plot(np.add(u_for_plot.T[1], u_nom[1]))
plt.show()


