import numpy as np

class Matriz:
    """ Monta a matriz de distâncias.
            
        Parameters
        ----------
        x_coord : array_like(float)
            Coordenadas euclidianas horizontais.
        y_coord : array_like(float)
            Coordenadas euclidianas verticais.
        Attributes
        ----------
        D : matrix(float)
            Matriz de distâncias.
        Len : int
            Quantidade de clientes
        Notes
        -----
            A distância calculada é euclidiana.
            
    """

    def __init__(self,x_coord,y_coord):
        Num_Elem = len(x_coord)
        D = np.zeros((Num_Elem,Num_Elem))
        for i in range (0,Num_Elem-1):
            for j in range (i+1,Num_Elem):
                D[i][j] = np.sqrt((x_coord[i]-x_coord[j])**2+(y_coord[i]-y_coord[j])**2)
                D[j][i] = D[i][j]
        self.D = D
        self.Len = Num_Elem
