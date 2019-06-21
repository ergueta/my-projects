import numpy as np
from aux_methods import Formiga,Roleta,Objetivo,Atualiza,\
                               Atualiza_Bestsofar,\
                               Atualiza_Rank,Atualiza_Bestiter
from nn_vrptw import NN_vrptw

def Otimiza(distance_time,
            nodes_number,limit,fleet,demand,truck_cap,mode,h_initial,h_final,
            time_service,start_op,algorithm="as"):
    """ Otimiza as Rotas.
        
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
        demand: array_lie(float)
            Demanda de cada cliente.
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
        Os parâmetro do AS, MMAS, RBAS e EAS estão internos. A etapa de evaporação
        também é feita internamente.
    """

    if (algorithm=="as"):
            Max_It = 2        # Numero maximo de iteracoes
            Num_Formigas = 2  # Numero de Formigas
            Q = 1      # Constante de Atualizacao do Feromonio
            alpha = 1           # Peso exponencial do Feromonio
            beta = 2      # Peso heuristico Exponencial
            sigma = 0.05        # Taxa de evarapocao
    elif (algorithm=="mmas"):
            Max_It = 250        # Numero maximo de iteracoes
            Num_Formigas = 25    # Numero de Formigas
            Q = 1      # Constante de Atualizacao do Feromonio
            alpha = 1           # Peso exponencial do Feromonio
            beta = 4     # Peso heuristico Exponencial
            sigma = 0.5
    elif (algorithm=="eas"):
            Max_It = 200        # Numero maximo de iteracoes
            Num_Formigas = 40    # Numero de Formigas
            Q = 1      # Constante de Atualizacao do Feromonio
            alpha = 1           # Peso exponencial do Feromonio
            beta = 5      # Peso heuristico Exponencial
            sigma = 0.5
            e = 10
    elif (algorithm=="rbas"):
            Max_It = 200        # Numero maximo de iteracoes
            Num_Formigas = 40    # Numero de Formigas
            Q = 1      # Constante de Atualizacao do Feromonio
            alpha = 1           # Peso exponencial do Feromonio
            beta = 5      # Peso heuristico Exponencial
            sigma = 0.5
            weight = 6
            
    sum_clients = 0
    minimo = float('Inf')
    minimo_iter = float('Inf')
    time_limit = 0
    
    min_vei_iter = float('inf')
    min_vei_global = float('inf')
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
    if (algorithm == "as"):
        tau_0 = np.multiply(Num_Formigas,1/(best_so_far))
        tau = np.multiply(tau_0,np.ones(dim))  # tau vira uma matrix
    elif (algorithm == "mmas"):
        tau_0 = np.multiply(1,1/(sigma*best_so_far))
        tau = np.multiply(tau_0,np.ones(dim))  # tau vira uma matrix
        tau_max = tau
        tau_max_0 = 0
        reset = [0]
        cont_reset = 0
    elif (algorithm == "eas"):
        tau_0 = np.multiply((Num_Formigas+e),1/(best_so_far))
        tau = np.multiply(tau_0,np.ones(dim))
    elif(algorithm == "rbas"):
        tau_0 = np.multiply(0.5*weight*(weight-1),1/(sigma*best_so_far))
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
                    #Probabilidade[-1] = 0                         # Probabilidade zero dos depositos virtuais serem escolhidos     
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
                        j=Roleta(Probabilidade)   
                        total_demand += demand[j]
                        total_length += distance_time[ultimo][j]+wait[j]+time_service[j]
                        time_limit = total_length + distance_time[j][0]
                        if (time_limit <= limit) and (total_demand <= truck_cap[formiga.vehicles-1]) and (urgency[j] >= 0):
                            formiga.adiciona(j)
                            sum_clients += 1 
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
            
            no_visiting = []
            if (formiga.caminho[-1] != 0):
                all_wait.append(0)
                formiga.adiciona(0) # It is exactly in here that I add the destination
            
            L = Objetivo(formiga.caminho,distance_time)
            
            Custo = L

            formiga.fcusto(Custo)

            if (formiga.vehicles <= min_vei_global):    
                if (Custo < minimo):
                    Melhor_Solucao = formiga
                    minimo = Custo
                    all_wait_output = []
                    all_wait_output.append(all_wait)
                    min_vei_global = Melhor_Solucao.vehicles
            if (formiga.vehicles <= min_vei_iter):
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
            wait = [0]
            urgency = [0]
            delta_time = [0]
            delivery_time = [0]

        Evolucao_Obj.append(minimo)  # atribui o custo minimo dessa primeira iteracao
        minimo_iter = float('inf')
        min_balance_iter = float('inf')
        min_vei_iter = float('inf')
        min_custo_iter = float('inf')
        max_custo_iter = 0
        
        if (algorithm == "as"):
            if (mode == 'time'):
                tau = Atualiza(Percorrido,Trilhas,Num_Formigas,length_size,tau,Q)  
            tau = (1-sigma)*tau 
        elif (algorithm == "mmas"):
            tau_max_0 = 1/(sigma*minimo)
            tau_max = np.multiply(tau_max_0,np.ones(dim))
            if (mode == "time"):
                tau = np.minimum(tau_max,Atualiza_Bestsofar(Melhor_Solucao.custo,Melhor_Solucao.caminho,len(Melhor_Solucao.caminho),tau,Q))
                #tau = np.minimum(tau_max,Atualiza_Bestiter(Melhor_Iter.custo,Melhor_Iter.caminho,len(Melhor_Iter.caminho),tau,Q)) 
            tau_min = np.multiply(tau_max,(1-(0.05)**(1/nodes_number))/((nodes_number/2-1)*(0.05)**(1/nodes_number)))
            tau = np.maximum(tau_min,(1-sigma)*tau) 
            if (minimo == reset[-1]):
                cont_reset += 1
                if (cont_reset == 20):
                    tau = tau_max
                    cont_reset = 0
            reset.append(minimo)
        elif (algorithm == "eas"):
            if (mode == 'time'):
                tau = Atualiza(Percorrido,Trilhas,Num_Formigas,length_size,tau,Q)+\
                      e*Atualiza_Bestsofar(Melhor_Solucao.custo,Melhor_Solucao.caminho,len(Melhor_Solucao.caminho),tau,Q) 
            tau = (1-sigma)*tau
        elif (algorithm == "rbas"):
            if (mode == 'time'):
                tau = Atualiza_Rank(Percorrido,Trilhas,Num_Formigas,length_size,tau,Q,weight)+\
                      weight*Atualiza_Bestsofar(Melhor_Solucao.custo,Melhor_Solucao.caminho,len(Melhor_Solucao.caminho),tau,Q) 
            tau = (1-sigma)*tau
            
        Percorrido = []
        Trilhas = []
        length_size = []
    return [Melhor_Solucao,Evolucao_Obj,all_wait_output]