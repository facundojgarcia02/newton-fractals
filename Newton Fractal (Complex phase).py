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
a = -1/2    #Termino del fractal generalizado. Usar 1 para el metodo clasico.

#ADVERTENCIA: 15000 me gasto 14 gb de ram durante 13 minutos. 
#Cuidado con el pantallazo azul.

#Casos interesantes
#z3 - 2z + 2
#z3 - 1
#[-16, 0, 0, 0, 15, 0, 0, 0, 1]
coeff = [-1,0,0,1] #ESTAN ORDENADOS AL REVES. EL PRIMER ELEMENTO ES EL TERMINO INDEPENDIENTE.
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
aproximated_roots = nr(f = my_poly, fprime = my_poly.deriv(1), x0 = xx+1j*yy, max_iter = 5, a = a)

print("Tiempo calculado:", time.time() - start_time)

#Ploteo y guardo.
fig, ax = plt.subplots(figsize = (20, 20))
ax.imshow(np.angle(aproximated_roots), cmap = "viridis")
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

plt.savefig(f"Fractal {coeff} a = {a}.png", dpi = 300)

print("Tiempo hasta guardar la imagen:", time.time() - start_time)