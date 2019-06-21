import numpy as np
from search_vrptw import Busca_vrptw

def NN_vrptw(distance_time,n_nodes,limit,demand,truck_cap,time_service,h_initial,h_final,start_op):
    """ Rotas geradas para o método do vizinho mais próximo.
        
        Parameters
        ----------
        distance_time_time : matrix(float)
            Matriz de distâncias.
        n_nodes : int
            Número de clientes visitados.
        limit : float
            Tempo de duração máximo de cada rota.
        demand: array_lie(float)
            Demanda de cada cliente.
        truck_cap : array_like(float)
            Capacidade de cada veiculo.
        time_service : array_like(float)
            Tempo de serviço em cada cliente.
        h_initial : array_like(float)
            Início da Janela de Tempo de cada cliente.
        h_final : array_like(float)
            Fim da Janela de Tempo de cada cliente.
        start_op : int
            Tempo inicial da operação.
        Returns
        -------
        Custo : float
            Custo da Rota encontrada para o método do vizinho mais próximo.
    """    
    d_tmp = distance_time.copy()
    weight_1 = 0.6
    weight_2 = 0.2
    weight_3 = 0.2
    wait = [0]
    cada_espera = []
    urgency = [0]
    
    extra_hour = 0
    idle_time = 0
    
    total_trilha = []
    total_tempo = []
    
    all_routes = []
    sum_demand = 0
    indice = 0
    total_length = start_op
    time_arc = 0
    total_arc = 0
    
    distance_time[0][0] = float(distance_time[0][0])
    d_tmp[0][0] = float(d_tmp[0][0])
    
    nao_visitados = []
    
    distance_time = np.array(distance_time)
    d_tmp = np.array(d_tmp)
    
    first_node = []
    for i in range(0,n_nodes):
        if (h_initial[i] == 0):
            first_node.append(i)
    
    inicio = 0
    rota = [inicio]
    
    cont = 0
    n_vei = 1
    
    dist = d_tmp.copy()
    for i in range (0,n_nodes):
        #distance_time[i][i] = 'inf'
        dist[i][i] = 'inf'
        nao_visitados.append(i)
    
    ultimo = rota[-1]
    for m in range (0,n_nodes-1):
        wait.append(max(h_initial[m+1]-total_length-time_service[ultimo]-d_tmp[ultimo][m+1],0))
        urgency.append(h_final[m+1]-total_length-time_service[ultimo]-d_tmp[ultimo][m+1])
        dist[ultimo,m+1] = weight_1*dist[ultimo,m+1] + weight_2*wait[m+1] + weight_3*urgency[m+1]
        
    
    index = np.argmin(dist[ultimo,:])
    rota.append(index)
    nao_visitados.remove(rota[1]) 
    nao_visitados.remove(rota[0])
    
    trilha = distance_time[rota[-2],rota[-1]]
    total_length += d_tmp[rota[-2],rota[-1]]
    
    if (n_nodes == 2):
        trilha = distance_time[0][1] + distance_time[1][0]
        cont=1000
    if (n_nodes == 3):
        trilha = distance_time[0][1] + distance_time[1][2]
        cont=1000
    while(cont<n_nodes-2):
            ultimo = rota[-1]
            for m in range (0,n_nodes-1):
                wait.append(max(h_initial[m+1]-total_length-d_tmp[ultimo][m+1],0))
                urgency.append(h_final[m+1]-total_length-d_tmp[ultimo][m+1])
                dist[ultimo,m+1] = weight_1*dist[ultimo,m+1] + weight_2*wait[m+1] + weight_3*urgency[m+1]
            valores = Busca_vrptw(dist,d_tmp,nao_visitados,ultimo)
            indice = valores[0]
            time_arc = valores[1]
            total_length += time_arc + time_service[indice] + wait[indice]
            total_arc += time_arc
            time_limit = total_length + d_tmp[ultimo][rota[0]]
            sum_demand += demand[indice]
            if (time_limit <= limit and urgency[indice] >= 0 and truck_cap[n_vei] >= sum_demand):
                trilha += distance_time[ultimo][indice] # Implementar
                rota.append(indice)
                nao_visitados.remove(indice)
                cada_espera.append(wait[indice])
                if (cont == n_nodes-3):
                    trilha += distance_time[indice][rota[0]]
                    total_length += d_tmp[indice][rota[0]]
                    rota.append(rota[0])
                    all_routes.append(rota)
                    total_trilha.append(trilha)
                    total_arc += d_tmp[indice][rota[0]]
                    total_tempo.append(total_arc)
                cont += 1
            else:
                total_arc -= time_arc
                all_routes.append(rota)
                rota = [0]
                trilha += distance_time[ultimo][rota[0]]
                n_vei += 1
                sum_demand = 0
                total_trilha.append(trilha)
                total_tempo.append(total_arc)
                total_length = start_op
                trilha = 0
            urgency = [0]
            wait = [0]
        
    Custo = sum(total_tempo)
    return Custo 
    
    