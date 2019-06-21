import numpy

class Formiga:
    """ Inicializa a classe Formiga.
            
        Parameters
        ----------
        i : int
            Identificador da formiga.       
        Attributes
        ----------
        i : int
            Identificador da formiga.
        caminho : array_like(int)
            Rota percorrida.
        custo : array_like(float)
            Custo da Rota.
        vehicles : int
            Numero de veiculos usados na Rota.
        limit : array_like(float)
            Último cliente de uma rota.
            
    """
    def __init__(self,i):
        self.i = i
        self.caminho = []
        self.custo = []
        self.vehicles = 1
        self.limited = []

        
    def adiciona(self,caminho):
        """ Adiciona cliente à rota.
            
            Parameters
            ----------
            caminho : array_like(int)
                Rota percorrida.
   
        """
        self.caminho.append(caminho)
        
    def fcusto(self,custo):
        """ Adiciona o custo da rota.
    
            Parameters
            ----------
            custo : array_like(float)
                Custo da Rota.
            
        """
        self.custo = custo
    
    def n_vehicles(self,j):
        """ Adiciona um veiculo usado e o último cliente da rota.
            
            Parameters
            ----------
            vehicles : int
                Numero de veiculos usados na Rota.
            limit : array_like(float)
                Último cliente de uma rota.

        """
        self.vehicles += 1
        self.limited.append(j)
            
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
    r = numpy.random.random()
    C = numpy.cumsum(P)
    s = C>=r
    j = numpy.where(s)[0]
    j = j[0]
    return j

def Roleta_ACS(P,q0):
    """ Sorteia o próximo cliente a ser visitado para o ACS.

        Parameters
        ----------
        P : array_like(float)
            Probabilidade de visitar cada um dos clientes.
        q0 : float
            Probabilidade da próxima visita ser determinística.
        Returns
        -------
        j : int
            Cliente sorteado.
            
    """
    r = numpy.random.random()
    if (r <= q0):
        aux = numpy.argsort(P)
        j = aux[-1]
    else:
        C = numpy.cumsum(P)
        s = C>=r
        j = numpy.where(s)[0]
        j = j[0]
    return j

def Objetivo(caminho,distancia):
    """ Calcula a função objetivo.

        Parameters
        ----------
        caminho : array_like(int)
            Rota percorrida.
        distancia : matrix(float)
            Matriz de distâncias.
        Returns
        -------
        L : float
            Distância total percorrida.
            
    """
    Num_Elem = len(caminho)
    L = 0
    for i in range (0,Num_Elem-1):
            L += distancia[caminho[i]][caminho[i+1]]
    return L  

def Atualiza(Percorrido,Trilhas,Num_Formigas,Num_Elem,tau,Q):
    """ Atualiza o Feromônio.

        Parameters
        ----------
        Percorrido : array_like(float)
            Distancia percorrida em cada rota construída por cada formiga de uma iteração.
        Trilhas : list of array_like(int)
            Rota percorrida por cada formiga de uma iteração.
        Num_Formigas : int
            Número de formigas usadas.
        Num_Elem : array_like(int)
            Número de nós adicionadas a rota.
        tau: matrix(float)
            Matriz de feromônios.
        Q: float
            Constante de atualização do feromõnio.
        Returns
        -------
        tau : matrix(float)
            Matriz de feromônios atualizada.
    """            
    for i in range (0,Num_Formigas):
        for j in range (0,Num_Elem[i]-1):
            zi = Trilhas[i][j]
            zj = Trilhas[i][j+1]
            tau[zi][zj] += (Q)/Percorrido[i]
    return tau


def Atualiza_Rank(Percorrido,Trilhas,Num_Formigas,Num_Elem,tau,Q,weight):
    """ Atualiza o Feromônio para o RBAS.

        Parameters
        ----------
        Percorrido : array_like(float)
            Distancia percorrida em cada rota construída por cada formiga de uma iteração.
        Trilhas : list of array_like(int)
            Rota percorrida por cada formiga de uma iteração.
        Num_Formigas : int
            Número de formigas usadas.
        Num_Elem : array_like(int)
            Número de nós adicionadas a rota.
        tau: matrix(float)
            Matriz de feromônios.
        Q: float
            Constante de atualização do feromõnio.
        weight : int
            Peso usado no RBAS.
        Returns
        -------
        tau : matrix(float)
            Matriz de feromônios atualizada.
    """            
    idx_ordered = numpy.argsort(Percorrido)
    r = 1
    for i in range (0,weight):
        for j in range (0,Num_Elem[idx_ordered[i]]-1):
            zi = Trilhas[idx_ordered[i]][j]
            zj = Trilhas[idx_ordered[i]][j+1]
            tau[zi][zj] += (max((weight-r),0)*Q)/Percorrido[idx_ordered[i]]
        r += 1
    return tau

def Atualiza_Bestsofar(Percorrido,Trilhas,Num_Elem,tau,Q):
    """ Atualiza o Feromônio para melhor formiga até então.

        Parameters
        ----------
        Percorrido : int
            Distancia percorrida pela melhor formiga até então.
        Trilhas : array_like(int)
            Rota percorrida pela melhor formiga até então.
        Num_Elem : int
            Número de nós adicionadas a rota da melhor formiga até então.
        tau: matrix(float)
            Matriz de feromônios.
        Q: float
            Constante de atualização do feromõnio.
        Returns
        -------
        tau : matrix(float)
            Matriz de feromônios atualizada.
    """            
    for j in range (0,Num_Elem-1):
        zi = Trilhas[j]
        zj = Trilhas[j+1]
        tau[zi][zj] += (Q)/Percorrido
    return tau

def Atualiza_Bestiter(Percorrido,Trilhas,Num_Elem,tau,Q):
    """ Atualiza o Feromônio para melhor formiga da iteração.

        Parameters
        ----------
        Percorrido : int
            Distancia percorrida pela melhor formiga da iteração.
        Trilhas : array_like(int)
            Rota percorrida pela melhor formiga da iteração.
        Num_Elem : int
            Número de nós adicionadas a rota da melhor formiga da iteração.
        tau: matrix(float)
            Matriz de feromônios.
        Q: float
            Constante de atualização do feromõnio.
        Returns
        -------
        tau : matrix(float)
            Matriz de feromônios atualizada.
    """     
    for j in range (0,Num_Elem-1):
        zi = Trilhas[j]
        zj = Trilhas[j+1]
        tau[zi][zj] += (Q)/Percorrido
    return tau

def Atualiza_ACS(Percorrido,Trilhas,Num_Elem,tau,Q,sigma):
    """ Atualiza e Evapora o feromônio para o ACS.

        Parameters
        ----------
        Percorrido : int
            Distancia percorrida pela melhor formiga até então.
        Trilhas : array_like(int)
            Rota percorrida pela melhor formiga até então.
        Num_Elem : int
            Número de nós adicionadas a rota da melhor formiga até então.
        tau: matrix(float)
            Matriz de feromônios.
        Q: float
            Constante de atualização do feromõnio.
        sigma: float
            Constante de evaporação.
        Returns
        -------
        tau : matrix(float)
            Matriz de feromônios atualizada.
    """     
    for j in range (0,Num_Elem-1):
        zi = Trilhas[j]
        zj = Trilhas[j+1]
        tau[zi][zj] += (Q*sigma)/Percorrido
        tau[zi][zj] = (1-sigma)*tau[zi][zj]
    return tau

def Separate_route(opt_route,limit_after_client):
    """ Separa as rotas.
        
        Parameters
        ----------
        opt_route : array_like(int)
            Rota otimizada.
        limit_after_client : array_like(int)
            Último cliente de cada rota.
        Returns
        -------
        each_route : list of array_like(int)
            Rotas separadas.        
    """
    each_route = []
    first = 0
    to_separate = 0
    stop = 0
    for i in range (0,len(opt_route)-1):
        if (limit_after_client) and (stop==0): 
             if (i==limit_after_client[to_separate]):
                    each_route.append(opt_route[first:i+2])
                    first = i+1
                    to_separate += 1
                    if (to_separate == len(limit_after_client)):
                        stop = 1
                        each_route.append(opt_route[first:])
        elif (limit_after_client == []):
            each_route.append(opt_route)
            break
    return each_route
          
def Separate_demand(each_route,demand):
    """ Separa a demanda de cada rota.
        
        Parameters
        ----------
        each_route : list of array_like(int)
            Rotas separadas.
        demand : array_like(float)
            Demanda de cada cliente.
        Returns
        -------
        each_demand : array_like(float)
            Demanda de cada rota.        
    """
    each_demand = []
    sum_demand = 0
    for i in range (0,len(each_route)):
        for j in range (0,len(each_route[i])):
            sum_demand += demand[each_route[i][j]]
            #if(each_route[i][j]==0)and(j!=0)and(j!=len(each_route[i])-1):
            #    each_demand.append(sum_demand)
            #    each_demand.append("-")
            #    sum_demand = 0
        each_demand.append(sum_demand)
        #each_demand.append(":")
        sum_demand = 0
    return each_demand

def Separate_time(each_route,time_matrix,wait,time_service,n_nodes):
    """ Separa o tempo de duração de cada rota.
        
        Parameters
        ----------
        each_route : list of array_like(int)
            Rotas separadas.
        time_matrix : matrix(float)
            Matriz de distâncias.
        wait : array_like(float)
            Espera em cada cliente.
        time_service : array_like(float)
            Tempo de serviço em cada cliente.
        n_nodes : int
            Número de clientes visitados.
        Returns
        -------
        each_time : array_like(float)
            Tempo de duração de cada rota.        
    """
    each_time = []
    sum_time = 0
    for i in range (0,len(each_route)):        
        for j in range (0,len(each_route[i])-2):
            sum_time += time_matrix[each_route[i][j]][each_route[i][j+1]]+wait[i][j+1] \
                        +time_service[each_route[i][j+1]]
        #if (i != len(each_route)-1):
        sum_time += time_matrix[each_route[i][j+1]][n_nodes-1]
        each_time.append(sum_time)
        sum_time = 0
    return each_time

def Break_wait(each_route,wait):
    """ Separa a espera de cada rota.
        
        Parameters
        ----------
        each_route : list of array_like(int)
            Rotas separadas.
        wait : array_like(float)
            Espera em cada cliente.
        Returns
        -------
        broken_wait_output : array_like(float) 
            Espera em cada rota.        
    """
    broken_wait = []
    broken_wait_output = []
    sum_up = 0
    for i in range(0,len(each_route)):
        for j in range (0,len(each_route[i])-1):
                if (i != 0):
                    broken_wait.append(wait[sum_up+j])
                else:
                    broken_wait.append(wait[j])
        sum_up += len(each_route[i])-1
        broken_wait_output.append(broken_wait)
        broken_wait = []
    return broken_wait_output



