import numpy as np
import numdifftools as nd
import plot
from numpy.linalg import multi_dot, inv

class EFK:
    def __init__(self,x0,C,Q,R):
        self.Q = Q
        self.R = R
        self.C = C
        self.xhat = x0
        self.P = np.diag(np.ones(len(Q)))
        self.f = fun()
        self.F = nd.Jacobian(self.f,step=1)

    def filter(self,z):
        """
            Filtro de Kalman Extendido
        """
        P = self.P
        xhat = self.xhat
        C = self.C
        Q = self.Q
        R = self.R
        f = self.f
        d_F = self.F

        # prediction
        xhatminus = f(xhat)

        F = d_F(xhat)

        Pminus = multi_dot([F,P,np.transpose(F)]) + Q

        # measurement update
        y = np.dot(C,xhatminus)
        
        K = np.dot(np.dot(Pminus,np.transpose(C)),inv((multi_dot([C,Pminus,np.transpose(C)]) + R)))
        
        xhat = xhatminus+np.dot(K,(z-y))
        P = Pminus-multi_dot([K,C,Pminus])
        
        self.xhat = xhat
        self.P = P
        
class FK(EFK):
    def __init__(self,x0,C,Q,R):
        super().__init__(x0,C,Q,R)
        f = fun()
        self.F = nd.Jacobian(f)(x0)
                 
    def filter(self,z):
        """
            Filtro de Kalman Extendido
        """
        P = self.P
        xhat = self.xhat
        C = self.C
        Q = self.Q
        R = self.R
        F = self.F

        # prediction
        xhatminus = np.dot(F,xhat)    
        
        Pminus = multi_dot([F,P,np.transpose(F)]) + Q

        # measurement update
        y = np.dot(C,xhatminus)
        
        K = np.dot(np.dot(Pminus,np.transpose(C)),inv((multi_dot([C,Pminus,np.transpose(C)]) + R)))
        
        xhat = xhatminus+np.dot(K,(z-y))
        P = Pminus-multi_dot([K,C,Pminus])
        
        self.xhat = xhat
        self.P = P
        
        
def fun():
    """
        Escreva seu modelo
    """
    
    #return np.array([x[0],x[1]])
    fun = lambda x: np.array([np.sqrt(abs(x[0])),
                              x[1]])
    return fun
        
x0 = np.array([0,
               0])

Q = np.diag([1,1])
#R = np.diag([0.1,0.1])
R = np.diag([0.1])
#C = np.reshape((1,0,0,1),(2,2))
C = np.reshape((1,0),(1,2))

# instancia
b = EFK(x0,C,Q,R)
c = FK(x0,C,Q,R)

z_vec = []
xhat_vec = []
xhat_vec_fk = []
estimado = []
estimado_fk = []

for i in range(0,50):
    #z = np.array([np.sqrt(abs(np.random.normal(2,0.1))),
    #              1])
    z = np.array([np.sqrt(abs(np.random.normal(2,0.1)))])
    b.filter(z)
    c.filter(z)
    z_vec.append(z[0])
    xhat_vec.append(b.xhat[0])
    xhat_vec_fk.append(c.xhat[0])
    estimado.append(b.xhat[1])
    estimado_fk.append(c.xhat[1])
    
plot.Plot_compare(z_vec,xhat_vec,'medicao','filtrado')    
plot.Plot_compare(z_vec,xhat_vec_fk,'medicao','filtrado fk')
plot.Plot_compare(xhat_vec,xhat_vec_fk,'efk','fk')    
plot.Plot_compare(estimado,estimado_fk,'estimado efk','estimado fk')    
