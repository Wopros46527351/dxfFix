import sys
import ezdxf
from figure import figure
import matplotlib.pyplot as plt
from Generics import *
from LWPFunctions import *
from Solver import *



"""1. Открываем файл"""
"""____________________________________________________________________"""
doc=open_file(file_name="111.dxf")

"""2. Считываем все объекты и выводим информацию"""
"""____________________________________________________________________"""
msp = doc.modelspace()

figs = [figure(i) for i in msp]
figs = sorted(figs,key = sort_min_x)

for i in figs:
    i.merge_double_points(0.01,debug=True)
    i.make_arcs()   
    #i.drawFigurePlt()
    i.draw_in_steps(10)
    #i.drawId()
plt.axis('equal')
plt.show()
plt.clf()

