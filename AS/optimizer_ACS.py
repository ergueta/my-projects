import numpy as np
from aux_methods import Formiga,Roleta,Objetivo,Atualiza,\
                               Atualiza_Bestsofar,\
                               Atualiza_Rank,Atualiza_ACS,Roleta_ACS,\
                               Atualiza_Bestiter
from nn_vrptw import NN_vrptw


def Otimiza_ACS(distance_time,
            nodes_number,limit,fleet,demand,truck_cap,mode,h_initial,h_final,
            time_service,start_op):
    """ Otimiza as Rotas para o ACS.
        
        Parameters
        ----------
        distance_time : matrix(float)
            Matriz de distâncias.
        nodes_number : int
            Número de clientes visitados.
        limit : float
            Tempo de duração máximo de cada rota.
        fleet : int
            Número de veiculos disponíveis
        truck_cap : array_like(float)
            Capacidade de cada veiculo.
        mode : str
            Variável a ser minimizada na otimização.
        h_initial : array_like(float)
            Início da Janela de Tempo de cada cliente.
        h_final : array_like(float)
            Fim da Janela de Tempo de cada cliente.
        time_service : array_like(float)
            Tempo de serviço em cada cliente.
        start_op: int
            Tempo inicial da operação.
        algorithm: str, default="as"
            Algoritmo usado.
        Returns
        -------
        Melhor_Solucao : obj 
            Melhor Formiga da otimização.
        Evolucao_Obj : array_like(float)
            Valor da Função objetivo para cada iteração.
        all_wait_output : array_like(float)
            Esperas para cada cliente da melhor formiga.
        Notes
        -----
        Os parâmetros do ACS estão internos.
    """
    Max_It = 50        # Numero maximo de iteracoes
    Num_Formigas = 10   # Numero de Formigas
    Q = 1     # Constante de Atualizacao do Feromonio
    alpha = 1           # Peso exponencial do Feromonio
    beta = 1   # Peso heuristico Exponencial
    sigma = 0.5        # Taxa de evarapocao
    xsi = 0.5
    q0 = 0.9
    
    sum_clients = 0
    minimo = float('Inf')  ## Should be changed depending on minimizing Cost or maximizing Profit
    minimo_iter = float('Inf')
    time_limit = 0
    
    min_vei_iter = float('Inf')
    min_vei_global = float('Inf')
    min_balance = float('inf')
    min_balance_iter = float('inf')
    min_custo_global = float('inf')
    min_custo_iter = float('inf')
    max_custo_iter = 0
    extra_hour = 0
    idle_time = 0
    Receita = 0
    
    wait = [0]    
    all_wait = [0]
    urgency = [0]
    no_visiting = []
    delivery_time = [0]
    delta_time = [0]
    
    Trilhas = []   
    Percorrido = []
    Evolucao_Obj = []
    length_size = []
    
    dim = (nodes_number,nodes_number)    # variavel dimensao  

    np.seterr(divide='ignore')
    dist = distance_time.copy()
    eta = np.multiply(1,1/(distance_time))   # matrix do inverso da distance_time (Estatica!)
   
   
   
    if (mode == 'distance'):
            retorno_nn = NN_vrptw(distance_time,nodes_number,limit,demand,truck_cap,time_service,h_initial,h_final,start_op)
            best_so_far = retorno_nn
    else:
            retorno_nn = NN_vrptw(distance_time,nodes_number,limit,demand,truck_cap,time_service,h_initial,h_final,start_op)
            best_so_far = retorno_nn
    tau_0 = np.multiply(1,1/(nodes_number*best_so_far))
    tau = np.multiply(tau_0,np.ones(dim))
    
    for i in range (0,Max_It):             # Numero de iteracoes
            for k in range (0,Num_Formigas):   # Numero de formigas para cada iteracao
                formiga = Formiga(k)           # Classe Formiga atribuida a variavel formiga
                inicio = 0
                formiga.adiciona(inicio)       # adiciona a primeira rota a essa formiga
                sum_clients = 0
                total_length = start_op
                total_demand = 0
                while(sum_clients!=nodes_number-1):                                               # forma o caminho de cada formiga
                        ultimo = formiga.caminho[-1]                                              # pega o ultimo valor do vetor caminho
                        for m in range (0,nodes_number-1):
                            wait.append(max(h_initial[m+1]-total_length-\
                                            distance_time[ultimo][m+1],0))
                            urgency.append(h_final[m+1]-total_length-\
                                           distance_time[ultimo][m+1])            
                            delivery_time.append(max(total_length+\
                                                     distance_time[ultimo,m+1],h_initial[m+1])) # tempo para se chegar a cada cliente                                                                                            
                            delta_time.append(delivery_time[m+1]-total_length) # calcula da "atratividade", cliente com menor distance_time
                            dist[ultimo,m+1] = delta_time[m+1]*max((h_final[m+1]-total_length),
                                                                   0.1) # a segunda parte se refere a urgencia
                            
                        eta[ultimo,:] = np.multiply(1,1/(dist[ultimo,:]))
                        Probabilidade = np.multiply(tau[ultimo,:]**alpha,eta[ultimo,:]**beta)  # Faz multiplicacao ponto a ponto de tau e eta
                        Probabilidade[formiga.caminho]=0                                          # cada cliente percorrido nao sera retornado    
                        if no_visiting:
                            Probabilidade[no_visiting] = 0
                        
                        if (np.sum(Probabilidade) == 0):
                            if (formiga.caminho[-1] != 0):
                                if (formiga.vehicles == fleet):
                                        break
                                formiga.n_vehicles(formiga.caminho.index(formiga.caminho[-1])) 
                                formiga.adiciona(0)   
                                total_length = start_op
                                total_demand = 0
                                no_visiting = []
                                all_wait.append(0)
                            else:
                                if (formiga.vehicles == fleet):
                                        break
                                formiga.n_vehicles(formiga.caminho.index(formiga.caminho[-2]))
                                total_length = start_op
                                total_demand = 0
                                no_visiting = []
                        else:
                            Probabilidade = Probabilidade/np.sum(Probabilidade)
                            j=Roleta_ACS(Probabilidade,q0)   
                            total_demand += demand[j]
                            total_length += distance_time[ultimo][j]+wait[j]+time_service[j]
                            time_limit = total_length + distance_time[j][0]
                            if (time_limit <= limit) and (total_demand <= truck_cap[formiga.vehicles-1]) and (urgency[j] >= 0):
                                formiga.adiciona(j)
                                sum_clients += 1 # novo cliente visitado                                                  # Demanda do cliente contabilizada
                                all_wait.append(wait[j])
                            elif (urgency[j] < 0):
                                no_visiting.append(j)
                                total_demand += -demand[j]
                                total_length += -distance_time[ultimo][j]-wait[j]-time_service[j]
                            else:
                                if (time_limit > limit):
                                    if (formiga.caminho[-1] != 0):
                                        if (formiga.vehicles == fleet):
                                            break
                                        formiga.n_vehicles(formiga.caminho.index(formiga.caminho[-1]))
                                        formiga.adiciona(0)
                                        total_demand = 0
                                        total_length = start_op
                                        no_visiting = []
                                        all_wait.append(0)
                                    else:
                                        no_visiting.append(j)
                                        total_demand += -demand[j]
                                        total_length += -distance_time[ultimo][j]-wait[j]-time_service[j]
                                else:
                                    formiga.adiciona(0)
                                    total_demand = 0
                                    total_length += -distance_time[ultimo][j]-wait[j]-time_service[j]
                                    all_wait.append(0)
                        
                        wait = [0]
                        urgency = [0]
                        delta_time = [0]
                        delivery_time = [0]
                        if (len(formiga.caminho) > 1):
                            if (j != formiga.caminho[-2]):
                                tau[formiga.caminho[-2]][j] = (1-xsi)*tau[formiga.caminho[-2]][j] + xsi*tau_0 ## LOCAL UPDATE
                    
                no_visiting = []
                if (formiga.caminho[-1] != 0):
                    all_wait.append(0)
                    formiga.adiciona(0) # It is exactly in here that I add the destination
                L = Objetivo(formiga.caminho,distance_time)

                Custo = L
                formiga.fcusto(Custo)

                if (Custo < minimo):
                        Melhor_Solucao = formiga
                        minimo = Custo
                        all_wait_output = []
                        all_wait_output.append(all_wait)
                        min_vei_global = Melhor_Solucao.vehicles
                if (Custo < min_custo_iter):
                        Melhor_Iter = formiga
                        min_custo_iter = Custo
                        min_vei_iter = Melhor_Iter.vehicles
                Percorrido.append(Custo)                      # Caminho Percorrido pela formiga 
                Trilhas.append(formiga.caminho)           # Trilha Seguida
                length_size.append(len(formiga.caminho))
                all_wait = [0]   
                extra_hour = 0
                idle_time = 0
                Receita = 0
                
            Evolucao_Obj.append(minimo)  # atribui o custo minimo dessa primeira iteracao
            minimo_iter = float('inf')
            min_vei_iter = float('inf')
            min_balance_iter = float('inf')
            min_custo_iter = float('inf')
            max_custo_iter = 0
            wait = [0]
            urgency = [0]
            delta_time = [0]
            delivery_time = [0]
            
            if (mode == 'time'):
                tau = Atualiza_ACS(Melhor_Solucao.custo,Melhor_Solucao.caminho,len(Melhor_Solucao.caminho),tau,Q,sigma)
                #tau = Atualiza_ACS(Melhor_Iter.custo,Melhor_Iter.caminho,len(Melhor_Iter.caminho),tau,Q,sigma)
            Percorrido = []
            Trilhas = []
            length_size = []
            
    return [Melhor_Solucao,Evolucao_Obj,all_wait_output]
            
