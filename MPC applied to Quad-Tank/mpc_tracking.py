from cvxpy import *
import numpy as np
import scipy.sparse as sparse
import matplotlib.pyplot as plt

print("Hello world")

# Models

A = np.array(
    [ [-0.0423, 0, 0.1268, 0],
      [0, -0.0448, 0, 0.0951],
      [0, 0, -0.1268, 0],
      [0, 0, 0, -0.0951]
     ])

B = np.array(
    [ [0.3183, 0],
      [0, 0.3183],
      [0, 0.2122],
      [0.2122, 0]
    ])

C = np.eye(4)

[nx,nu] = B.shape
[ny,nx] = C.shape
A1 = np.concatenate((A,B), axis=1)
A2 = np.concatenate((np.zeros((nu,nx)), np.eye(nu,nu)), axis=1)
A_hat = np.concatenate((A1,A2),axis=0)

B_hat = np.concatenate((B,np.eye(nu,nu)),axis=0) 
C_hat = np.concatenate((C,np.zeros((nx,nu))), axis=1)
# Restrições
u_nom = np.array([166.67, 166.67])
x_nom = np.array([22.5908, 20.1504, 2.5101, 4.4624])

umin = np.array([-np.inf, -np.inf])# - u_nom 
umax = np.array([np.inf, np.inf]) #- u_nom
xmin = np.array([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf]) #- x_nom
xmax = np.array([np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]) #- x_nom

# Função Objetivo

Q = np.diag([100,100,.000001, .000001])
QN = Q
R = 1*np.eye(2)

# Estados

x0 = np.array([1,-2,1,-1,0,0]) # initial state
#xr = np.matrix([[0],[1],[0],[0]])
ref = np.array([0,0,0,0])
ref2 = np.array([1,-1,0,0])
ref3 = np.array([-1,1,0,0])
# Horizonte

N = 10
M = 2
# Definir Problema

du = Variable((nu, N))
x = Variable((nx+nu, N+1))

x_init = Parameter(nx+nu)
xr = Parameter(nx)
objective = 0
constraints = [x[:,0] == x_init]
for k in range(N):
    objective += quad_form(C_hat*x[:,k] - xr, Q) + quad_form(du[:,k], R)
    constraints += [x[:,k+1] == A_hat*x[:,k] + B_hat*du[:,k]]
    constraints += [xmin <= x[:,k], x[:,k] <= xmax]
    constraints += [umin <= du[:,k], du[:,k] <= umax]
    #if (k+1 >= M):
    #    constraints += [u[:,k] == u[:,1]]
objective += quad_form(C_hat*x[:,N] - xr, QN)
prob = Problem(Minimize(objective), constraints)

# Simulacao
nsim = 60
all_states, all_inputs = [],[]
for i in range(nsim):
    x_init.value = x0
    if (i >=0 and i < 20):
        xr.value = ref
    elif (i >=20 and i < 40):
        xr.value = ref2
    else:
        xr.value = ref3
    prob.solve(solver=OSQP, warm_start=True)
    
    # process
    x0 = A_hat.dot(x0) + B_hat.dot(du[:,0].value)+.00001*np.random.rand(len(x0),1).ravel()
    all_states.append(x0)
    all_inputs.append(du[:,0].value)
    #print(u.value)
    #print(x0[1])
 
x_for_plot = np.array(all_states)
u_for_plot = np.array(all_inputs)

plt.subplot(311)
plt.plot(x_for_plot.T[0] + x_nom[0])
plt.plot(x_for_plot.T[1] + x_nom[1])
plt.plot(x_for_plot.T[2] + x_nom[2])
plt.plot(x_for_plot.T[3] + x_nom[3])
plt.subplot(312)
plt.plot(x_for_plot.T[4] + u_nom[0])
plt.plot(x_for_plot.T[5] + u_nom[1])
plt.subplot(313)
plt.plot(u_for_plot.T[0])
plt.plot(u_for_plot.T[1])
plt.show()
