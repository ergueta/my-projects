import numpy as np
from random import randint

class TS:
    def __init__(self,nodes,iter,n_set,matrix):
        self.nodes = nodes
        self.iter = iter
        self.n_set = n_set
        self.matrix = matrix
        self.costo = self.InitialCost()
        self.sol = np.arange(nodes)
        self.tabu = np.zeros((nodes,nodes))
        self.tabu_d = np.zeros((nodes,nodes))
        
    def Optimizer(self):
        nodes = self.nodes
        iter = self.iter
        sol = self.sol
        sol_iter = sol.copy()
        cost = self.costo
        n_set = self.n_set
        tabu = self.tabu
        tabu_d = self.tabu_d

        all_set = []
        all_swaps = []
        aux = []
        
        for i in range(iter):
            j = 0
            while (j < n_set):
                pick1, pick2 = randint(1,nodes-2),randint(1,nodes-2)
                new_sol = sol_iter.copy()
                if (pick1 != pick2):
                    if (pick1 < pick2):
                        new_sol[pick1:pick2] = list(reversed(sol_iter[pick1:pick2]))
                    else:
                        new_sol[pick2:pick1] = list(reversed(sol_iter[pick2:pick1]))
                #print(new_sol)
                    all_set.append(new_sol)
                    all_swaps.append((pick1,pick2,))
                    j += 1
                    
            each_cost = list(map(self.Cost,all_set))        
            if (i <= iter/2):
                idx = np.argsort(each_cost)
                each_cost = np.sort(each_cost)
            else: # diversification
                for w in range(0,len(all_set)):
                    aux.append(self.Cost_d(all_set[w],all_swaps[w],tabu_d))
                each_cost_d = aux.copy()
                aux = []
            
                idx = np.argsort(each_cost_d)
                each_cost = [each_cost[u] for u in idx]
            
            all_set = [all_set[u] for u in idx]
            all_swaps = [all_swaps[u] for u in idx]
                    
                #each_cost = list(map(self.Cost_d,all_set,all_swaps))
            #best_now_idx = np.argmin(each_cost)
            
        
            cos_iter = self.costo
            tabu = np.add(tabu,-1)
            tabu[np.where(tabu<0)] = 0
            
            for k in range(0,len(each_cost)):
                if (tabu[all_swaps[k][0],all_swaps[k][1]] == 0):
                    cost_iter = each_cost[k]
                    sol_iter = all_set[k]
                    swap = all_swaps[k]
                elif (each_cost[k] < cost):
                    cost_iter = each_cost[k]
                    sol_iter = all_set[k]
                    swap = all_swaps[k]
            
            if (cost_iter < cost):
                cost = cost_iter
                sol = sol_iter.copy()
                #print(sol)
            tabu[swap[0],swap[1]] = 3
            tabu[swap[1],swap[0]] = 3
            
            tabu_d[swap[0],swap[1]] += 1
            tabu_d[swap[1],swap[0]] += 1

            all_set = []
            all_swaps = []
        return (cost,sol,)
            
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
        
    def Cost_d(self,s,swaps,tabu_d):
            matrix = self.matrix
            nodes = self.nodes
            sum = 0
            for i in range(nodes-1):
                sum += matrix[s[i]][s[i+1]]
            return sum+tabu_d[swaps[0],swaps[1]]
            
            
