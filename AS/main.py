import numpy as np 
from optimizer import Otimiza
from optimizer_ACS import Otimiza_ACS

def Main(time_matrix,n_nodes,demand,h_initial,h_final,time_service,mode,algorithm,truck_cap,start_op,max_time_op,fleet):
    """ Otimiza as Rotas.
        
        Parameters
        ----------
        time_matrix: matrix(float)
            Matriz de distâncias.
        n_nodes : int
            Número de clientes visitados.
        demand: array_lie(float)
            Demanda de cada cliente.
        h_initial : array_like(float)
            Início da Janela de Tempo de cada cliente.
        h_final : array_like(float)
            Fim da Janela de Tempo de cada cliente.
        time_service : array_like(float)
            Tempo de serviço em cada cliente.
        mode : str
            Variável a ser minimizada na otimização.
        algorithm: str, default="as"
            Algoritmo usado.
        truck_cap : array_like(float)
            Capacidade de cada veiculo.
        start_op: float
            Tempo inicial da operação.
        max_time_op: float
            Tempo final da operação.
        fleet : int
            Número de veiculos disponíveis
    """

    limit = start_op+max_time_op # maximum hours driven

    if (algorithm != "acs"):
        solved = Otimiza(time_matrix,
                     n_nodes,limit,fleet,demand,truck_cap,mode,
                     h_initial,h_final,time_service,start_op,algorithm=algorithm)
    else:
        solved = Otimiza_ACS(time_matrix,
                     n_nodes,limit,fleet,demand,truck_cap,mode,
                     h_initial,h_final,time_service,start_op)
    
    return solved

