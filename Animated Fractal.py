import numpy as np
import matplotlib.pyplot as plt
import time

from numpy.polynomial import Polynomial as poly
from matplotlib.widgets import Slider
from utils import nr, distance_matrix

plt.rcParams["mathtext.fontset"] = "cm"

xi, xf = -1, 1 #Intervalo en Re(z)
yi, yf = -1, 1 #Intervalo en Im(z)

def fractal(coeff, size = 350, max_iter = 10):
    
    size = int(size)
    max_iter = int(max_iter)
    #ADVERTENCIA: 15000 me gasto 14 gb de ram durante 13 minutos. Cuidado con el pantallazo azul.

    #Casos interesantes
    #z3 - 2z + 2
    #z3 - 1
    #[-16, 0, 0, 0, 15, 0, 0, 0, 1]

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
    aproximated_roots = nr(f = my_poly, fprime = my_poly.deriv(1), x0 = xx+1j*yy, max_iter = max_iter, a = 2)

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

    return min_dist_root

def sliders_on_changed(val):
    plt.subplots_adjust(bottom = 0.18)
    min_dist_root = fractal([s1.val, s2.val, s3.val, s4.val], size = ssize.val, max_iter = siter.val)
    im.set_data(min_dist_root)
    fig.canvas.draw_idle()

#Ploteo y guardo.
fig, ax = plt.subplots(figsize = (5,5))

min_dist_root = fractal([1,0,0,-1])

im = ax.imshow(min_dist_root, interpolation = "none", cmap = "plasma")
ax.set_xticks([])
ax.set_yticks([])
#ax.set_title(r"$[-1,1] \times [-1,1]$")

plt.subplots_adjust(bottom = 0.18, left = 0.3)

ssize_x  = fig.add_axes([0.05, 0.25, 0.02, 0.55], facecolor= "black")
ssize = Slider(ssize_x, r'Size', 200, 500, valinit= 300, color = "black", orientation = "vertical")

siter_x  = fig.add_axes([0.18, 0.25, 0.02, 0.55], facecolor= "black")
siter = Slider(siter_x, r'Iterations', 1, 15, valinit= 5, color = "black", orientation = "vertical")

s1_x  = fig.add_axes([0.35, 0.14, 0.5, 0.02], facecolor= "black")
s1 = Slider(s1_x, r'$P_1$', -3, 3, valinit= 1, color = "black")

s2_x  = fig.add_axes([0.35, 0.10, 0.5, 0.02], facecolor= "black")
s2 = Slider(s2_x, r'$P_2$', -3, 3, valinit= 0, color = "black")

s3_x  = fig.add_axes([0.35, 0.06, 0.5, 0.02], facecolor= "black")
s3 = Slider(s3_x, r'$P_3$', -3, 3, valinit= 0, color = "black")

s4_x  = fig.add_axes([0.35, 0.02, 0.5, 0.02], facecolor= "black")
s4 = Slider(s4_x, r'$P_4$', -3, 3, valinit= -1, color = "black")

ax.text(0.5,-0.075,r"$0 = P_1 + P_2 z + P_3 z^2 + P_4 z^3$", fontsize = 12, transform = ax.transAxes, ha = "center",)

ssize.on_changed(sliders_on_changed)
siter.on_changed(sliders_on_changed)
s1.on_changed(sliders_on_changed)
s2.on_changed(sliders_on_changed)
s3.on_changed(sliders_on_changed)
s4.on_changed(sliders_on_changed)

plt.show()