import numpy as np
import random
# Example code for container storage problem

distance_matrix = [[105,378,205,378,400],[118,391,118,291,413],[106,378,165,332,314]]
distance_matrix = np.asarray(distance_matrix)

unload_time = [10,8,20,4,5] # container 0,1,2,3,4
stack_max = [5,1,1]

tau_0 = 5
tau = np.ones((5,3))
tau = np.multiply(tau_0,tau)

tau_max = np.multiply(2,tau)
tau_min = np.multiply(1/5,tau)

eta = np.multiply(1,1/distance_matrix)
eta = np.transpose(eta)

alpha = 0.3
beta = 0.3
sigma = 0.2
n_iter = 1
n_ants = 1
best_so_far = float('inf')

for i in range(n_iter):
    for j in range(n_ants):
        #(i,j)
        best_iter = float('inf')
        ant = []
        stack = [0,0,0]
        n_containers = 1
        #nth_container = np.argsort(unload_time)[-n_containers]
        x = list(range(5))
        nth_container = np.random.choice(x)
        jump_stack = []
        shuffle = 0
        minimum = [float('inf'),float('inf'),float('inf')]
        while(n_containers <= 5):
            prob = np.multiply(tau[nth_container,:]**alpha,eta[nth_container,:]**beta)
            if jump_stack:
                prob[jump_stack] = 0
            for zy in range(0,len(stack)):
                if (stack[zy] == stack_max[zy]):
                    prob[zy] = 0
            
            if (np.sum(prob) == 0):
                #("aqui")
                #(stack)
                #(nth_stack)
                for k in range(0,len(stack)):
                    if (stack[k] < stack_max[k]):
                        ant.append([nth_container,nth_stack])
                        minimum[nth_stack] = unload_time[nth_container]
                        stack[nth_stack] += 1
                        n_containers += 1
                        shuffle += 1
                        jump_stack = []
                        if (n_containers <= 5):
                            #nth_container = np.argsort(unload_time)[-n_containers]
                            ##(x)
                            x.remove(nth_container)
                            ##(x)
                            nth_container = np.random.choice(x)
                            ##(nth_container)
            else:
                prob = prob/np.sum(prob)
                random_number = np.random.random()
                accumulated_prob = np.cumsum(prob)
                where_to_go = random_number < accumulated_prob
                nth_stack = np.where(where_to_go)[0][0]
                
                stack[nth_stack] += 1
                
                if (stack[nth_stack] <= stack_max[nth_stack] and unload_time[nth_container] <= minimum[nth_stack]):
                    #("que")
                    ant.append([nth_container,nth_stack])
                    minimum[nth_stack] = unload_time[nth_container]
                    n_containers += 1
                    jump_stack = []
                    if (n_containers <= 5):
                        #nth_container = np.argsort(unload_time)[-n_containers]
                        #(x)
                        x.remove(nth_container)
                        #(x)
                        nth_container = np.random.choice(x)
                        #(nth_container)
                else:
                    #("oi")
               
                    jump_stack.append(nth_stack)
                    stack[nth_stack] -= 1
               
        fobj = shuffle
        if (fobj < best_so_far):
            best_so_far = fobj
            best_ant = ant
        if (fobj < best_iter):
            best_iter = fobj
    
    for zi in range(0,len(best_ant)):
            tau[best_ant[zi][0]][best_ant[zi][1]] += 1/(best_iter-best_so_far+1)
    tau = (1-sigma)*tau
     
print(best_ant)
print(best_so_far)

            
            
            
            
            
            
        