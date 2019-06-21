from cvxpy import *
import numpy as np
import scipy.sparse as sparse
import matplotlib.pyplot as plt

print("Hello world")

# Models

A = sparse.csc_matrix(
    [ [-0.0423, 0, 0.1268, 0],
      [0, -0.0448, 0, 0.0951],
      [0, 0, -0.1268, 0],
      [0, 0, 0, -0.0951]
     ])

B = sparse.csc_matrix(
    [ [0.3183, 0],
      [0, 0.3183],
      [0, 0.2122],
      [0.2122, 0]
    ])

[nx,nu] = B.shape

# Restrições
u_nom = np.array([166.67, 166.67])
x_nom = np.array([22.5908, 20.1504, 2.5101, 4.4624])

umin = np.array([-np.inf, -np.inf]) - u_nom 
umax = np.array([np.inf, np.inf]) - u_nom
xmin = np.array([-np.inf, -np.inf, -np.inf, -np.inf]) - x_nom
xmax = np.array([np.inf, np.inf, np.inf, np.inf]) - x_nom

# Função Objetivo

Q = np.diag([100,100,.000001, .000001])
QN = Q
R = .0001*np.eye(2)

# Estados

x0 = np.array([1,-2,1,-1]) # initial state
#xr = np.matrix([[0],[1],[0],[0]])
ref = np.array([0,1,0,0])
ref2 = np.array([1,0,0,0])
ref3 = np.array([0,0,1,0])
# Horizonte

N = 3
M = 2
# Definir Problema

u = Variable((nu, N))
x = Variable((nx, N+1))
x_init = Parameter(nx)
xr = Parameter(nx)
objective = 0
constraints = [x[:,0] == x_init]
for k in range(N):
    objective += quad_form(x[:,k] - xr, Q) + quad_form(u[:,k], R)
    constraints += [x[:,k+1] == A*x[:,k] + B*u[:,k]]
    constraints += [xmin <= x[:,k], x[:,k] <= xmax]
    constraints += [umin <= u[:,k], u[:,k] <= umax]
    if (k+1 >= M):
        constraints += [u[:,k] == u[:,1]]
objective += quad_form(x[:,N] - xr, QN)
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
    x0 = A.dot(x0) + B.dot(u[:,0].value)
    all_states.append(x0)
    all_inputs.append(u[:,0].value)
    #print(u.value)
    #print(x0[1])
 
x_for_plot = np.array(all_states)
u_for_plot = np.array(all_inputs)

plt.subplot(211)
plt.plot(x_for_plot.T[0])
plt.plot(x_for_plot.T[1])
plt.plot(x_for_plot.T[2])
plt.plot(x_for_plot.T[3])
plt.subplot(212)
plt.plot(u_for_plot.T[0])
plt.plot(u_for_plot.T[1])
plt.show()