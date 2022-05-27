import numpy as np

def nr(f: callable, fprime: callable , x0: np.ndarray, 
    max_iter: int = 100, a: complex = 1) -> np.ndarray: 
    """
    Metodo de Newton Ralphson para matrices sin tolerancia. 
    (Corta despues de calcular necesariamente las max_iter iteraciones).

    Parametros:
        - f: callable -> Función a la que calcular las raices.
        - fprime: callable -> Derivada de f(x).
        - x0: np.ndarray -> Valores iniciales.
        - max_iter: int (default = 100) -> Cantida de iteraciones.
        - a: complex (default = 1) -> Generalizacion del metodo de NR.
    Retorna:
        - (array-like) Lista de valores a los que converge el metodo.
    """
    xn = x0
    for i in range(max_iter):
        xn = xn - a*f(xn)/fprime(xn)
    return xn

def distance_matrix(p1: tuple, matrix: np.ndarray):
    """
    Calcula la distancia de cada punto de una matriz a un punto dado "p_1".
    
    Parametros:
        - p1: tuple -> Punto (x,y) al que calcularle la distancia.
        - matrix: np.ndarray -> Matriz que contiene los puntos a calcular la distancia hasta 'p1'.

    Retorna:
        - (array-like) Matriz con la distancia de cada punto de 'matrix' a 'p1'.
    """
    
    composed_matrix = np.array([matrix.real, matrix.imag])             #Para cada punto creo una nueva 
                                                                       #matriz que tenga (a,b) para un a+ib.
    size = composed_matrix.shape[1]
    p1 = p1.reshape((2, 1, 1)).repeat(size, axis = -1).repeat(size, 1) #Reshapeo y repito sobre los ejes para que
                                                                       #sea del mismo tamaño que composed_matrix.

    dist = np.linalg.norm(composed_matrix - p1, ord = 2, axis = 0)     #Finalmente calculo la distancia euclideana 
                                                                       #de cada punto en una matriz.

    return dist