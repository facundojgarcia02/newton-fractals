import numpy as np
import matplotlib.pyplot as plt
import time

from numpy.polynomial import Polynomial as poly
from utils import nr, distance_matrix

plt.rcParams["mathtext.fontset"] = "cm"

start_time = time.time()

xi, xf = -1, 1 #Intervalo de Re(z)
yi, yf = -1, 1 #Intervalo de Im(z)
size = 2500 #Tamaño de la matriz (Idealmente = 2500.)

#ADVERTENCIA: 15000 me gasto 14 gb de ram durante 13 minutos. 
#Cuidado con el pantallazo azul.

#Casos interesantes
#z3 - 2z + 2
#z3 - 1
#[-16, 0, 0, 0, 15, 0, 0, 0, 1]
coeff = [0.624, 0.696, 0, -1] #ESTAN ORDENADOS AL REVES. EL PRIMER ELEMENTO ES EL TERMINO INDEPENDIENTE.
                                       #(Asi lo toma la clase de numpy yqc tan re locos).

#Creacion de polinomio y calculo de raices
my_poly = poly(coeff)
roots = my_poly.roots()

#Creacion de dominio espacial.


x = np.linspace(xi,xf,size)
y = np.linspace(yi,yf,size)
xx, yy = np.meshgrid(x,y)

del(x)
del(y)

#Calculo con NR las raices a las que se aproxima
aproximated_roots = nr(f = my_poly, fprime = my_poly.deriv(1), x0 = xx+1j*yy, max_iter = 15, a = 2)

#Calculo la distancia para cada raiz.
root_dist = [distance_matrix(np.array([root.real, root.imag]), aproximated_roots) for root in roots]

del(aproximated_roots)

root_dist_s = [ matrix.reshape((*matrix.shape, 1)) for matrix in root_dist] #Aca reshapeo para poder concatenarla despues.

del(root_dist)

mat = np.concatenate(root_dist_s, axis = -1)                                #Concateno de modo que para cada punto (x,y) 
                                                                            #hay una lista con la distancia de las n-raices.

del(root_dist_s)

min_dist_root = np.argmin(mat, axis= -1)                                    #Busco el index que tiene menor distancia 
                                                                            #para cada punto (x,y).

del(mat)

print("Tiempo calculado:", time.time() - start_time)

#Ploteo y guardo.
fig, ax = plt.subplots(figsize = (20, 20))
ax.imshow(min_dist_root, interpolation = "none", cmap = "plasma")
ax.set_xticks([])
ax.set_yticks([])

#String para el titulo.
if coeff[0] != 0:
    title = rf"$P(z) = {coeff[0]}$"
else:
    title = r"$P(z) = $"

for i in range(1, len(coeff)):
    if coeff[i] != 0:
        title += rf"$ + ({coeff[i]}) z^{i}$"
ax.set_title(title, fontsize = 50, pad=20)

print("Tiempo hasta crear la figura:", time.time() - start_time)

plt.savefig(f"Fractal {coeff} Prueba.png", dpi = 300)

print("Tiempo hasta guardar la imagen:", time.time() - start_time)