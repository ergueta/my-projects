import numpy as np  
from random import random
from random import randint

class SimulatedAnnealing:
    def __init__(self,To,iter,alfa,matrix,nodes):
            self.To = To
            self.iter = iter
            self.alfa = alfa
            self.matrix = matrix
            self.nodes = nodes
            self.costo = self.InitialCost()
            self.sol = np.arange(nodes)
    
    def Optimizer(self):
            T = self.To
            n = self.iter
            alfa = self.alfa
            cost = self.costo
            sol = self.sol
            nodes = self.nodes
            
            while(T > 0.0001):
                    for i in range(n):
                            pick1, pick2 = randint(1,nodes-2),randint(1,nodes-2)
                            new_sol = sol.copy()
                            
                            if (pick1 != pick2):
                                    if (pick1 < pick2):
                                            new_sol[pick1:pick2] = list(reversed(sol[pick1:pick2]))
                                    else:
                                            new_sol[pick2:pick1] = list(reversed(sol[pick2:pick1]))
                            new_cost = self.Cost(new_sol)
                            delta_e = new_cost - cost
                            if (delta_e < 0):
                                    cost = new_cost
                                    sol = new_sol.copy()
                            else:
                                    u = random()
                                    prob = np.exp(-delta_e/T)
                                    if (prob > u):
                                            cost = new_cost
                                            sol = new_sol.copy()
                    T = alfa*T
            return (cost,sol)
                    
    def InitialCost(self):
            matrix = self.matrix
            nodes = self.nodes
            sum = 0
            
            for i in range(nodes-1):
                    sum += matrix[i][i+1] 
            return sum
    
    def Cost(self,s):
            matrix = self.matrix
            nodes = self.nodes
            sum = 0
            
            for i in range(nodes-1):
                sum += matrix[s[i]][s[i+1]]
            return sum
