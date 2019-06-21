import numpy as np  
from random import random
from random import randint

def Roleta(P):
    """ Sorteia o próximo cliente a ser visitado.

        Parameters
        ----------
        P : array_like(float)
            Probabilidade de visitar cada um dos clientes.
            
        Returns
        -------
        j : int
            Cliente sorteado.
            
    """
    r = np.random.random()
    C = np.cumsum(P)
    s = C>=r
    j = np.where(s)[0]
    j = j[0]
    return j

class Ga:
    def __init__(self,val,wei,cap,items):
        self.val = val
        self.wei = wei
        self.cap = cap
        self.items = items
        self.popul = 10
        self.gener = 100
        self.sol = []
        self.best = -float('inf')
        self.bestpop = []
        self.bestwei = []
        self.initial = self.initial_sol()
        self.gama = 0.1
        self.ga()
        
    def selection(self,fits):
        popul = self.popul
        individuals = self.sol
        items = self.items
        
        new_individuals = []
        for i in range(0,popul):
            fits_aux = fits.copy()
            P = np.multiply(fits_aux,1/sum(fits_aux))
            j1 = Roleta(P)
            fits_aux[j1] = 0
            P = np.multiply(fits_aux,1/sum(fits_aux))
            j2 = Roleta(P)
            
            rdn = randint(0,items-1)
            new_individuals.append(individuals[j1][:rdn] + individuals[j2][rdn:])
        
        new_individuals = self.mutation(new_individuals.copy())        
        return new_individuals
        
    def mutation(self,new_individuals):
        for i in range(0,len(new_individuals)):
            if (random() > self.gama):
                alea = randint(0,self.items-1)
                if (new_individuals[i][alea]):
                    new_individuals[i][alea] = 0
                else:
                    new_individuals[i][alea] = 1
        return new_individuals
        
    def fitness(self,population):
        fits = []
        total_wei = 0
        fit = 0
        val = self.val
        wei = self.wei
        cap = self.cap
        for pop in population:
            for i in pop:
                fit += val[i]*i
                total_wei += wei[i]*i
            fit = fit - np.sum(wei)*np.abs(total_wei-cap)
            if (fit > self.best):
                self.best = fit
                self.bestpop = pop
                self.bestwei = total_wei
            fits.append(fit)
            fit = 0
            total_wei = 0
        return fits
        
    def initial_sol(self):
        aux = []
        sol = self.sol
        for i in range(0, self.popul):
            for j in range(0, self.items):
                aux.append(randint(0,1))
            sol.append(aux)
            aux = []
        return sol
    
    def ga(self):
        initial = self.initial
        generations = self.gener
        items = self.items
        population = initial.copy()
        self.sol = population
        for i in range(0,generations):
            fits = self.fitness(population)
            new_population = self.selection(fits)
            new_fits = self.fitness(new_population)
            
            old = np.argsort(fits)[::-1]
            new = np.argsort(new_fits)
            population = [population[i] for i in old]
            new_population = [new_population[i] for i in new]
            fits = np.sort(fits)[::-1]
            new_fits = np.sort(new_fits)

            population = [population[i] if (fits[i] > new_fits[i]) else new_population[i] for i in range(len(population))]
            
            self.sol = population
        pass

values = [] 
weights = []
#capacity = 9
#values = [6,5,8,9,6,7,3,10]
#weights = [2,3,6,7,5,9,4,1]
#items = len(values)

capacity = 165
weights = np.array([23, 31, 29, 44, 53, 38, 63, 85, 89, 82])
values = np.array([92, 57, 49, 68, 60, 43, 67, 84, 87, 72])
items = len(values)

ga = Ga(values,weights,capacity,items)
print(f"fitness: {ga.best}, solution: {ga.bestpop}, weigth: {ga.bestwei}")