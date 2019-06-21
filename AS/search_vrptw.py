import numpy

def Busca_vrptw(dist,d_tmp,nao_visitados,ultimo):
    """ Encontra o vizinho mais próximo.
        
        Parameters
        ----------
        dist : matrix(float)
            Matriz de distâncias que contabiliza a espera a urgência.
        d_tmp : matrix(float)
            Matriz de distâncias.
        nao_visitados : array_like(float)
            Clientes não visitados.
        último: int
            Cliente atual.
        Returns
        -------
        indice : int 
            Próximo cliente a ser visitado.
        time_arc : float
            Distância entre o cliente atual e o próximo visitado.
        
    """    
    Menor = dist[ultimo][nao_visitados[0]]
    time_arc = d_tmp[ultimo][nao_visitados[0]]
    indice = nao_visitados[0]
    for j in range(1,len(nao_visitados)):
        if (dist[ultimo][nao_visitados[j]] <= Menor):
                Menor = dist[ultimo][nao_visitados[j]]
                indice = nao_visitados[j]
                time_arc = d_tmp[ultimo][nao_visitados[j]]
    return [indice, time_arc]
    
    
