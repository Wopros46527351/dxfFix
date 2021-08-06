import sys
import ezdxf
from figure import figure
import matplotlib.pyplot as plt
from Generics import *
from LWPFunctions import *
#Верните функции туда где они были и просто импортируйте их!           

"""1. Открываем файл"""
"""____________________________________________________________________"""
doc=open_file(file_name="111.dxf")

"""2. Считываем все объекты и выводим информацию"""
"""____________________________________________________________________"""
msp = doc.modelspace()
read_dxf(msp)
    

figs = [figure(i) for i in msp]
figs = sorted(figs,key = sort_min_x)

for i,f in enumerate(figs):
    f.id = i
    f.drawFigurePlt()
    f.drawId()
    f.drawCenter()
    f.bounding_box()
'''
lwps = [i.LWP for i in figs]
shift = find_shift(lwps)
print(lwps)
lwps.sort(key=rate)
print(lwps)
'''



'''тут строятся мосты'''
"""
msp.add_lwpolyline(bridge_len(1,3,figs))
p1,p2 = bridge_points(figs[0].LWP,figs[1].LWP)
s1=top_points(figs[0].LWP)
print(s1,'top_points')
dot1 = figs[0].LWP[p1]
dot2 = figs[1].LWP[p2]
s=[(dot1[0],dot1[1]),(dot2[0],dot2[1])]
msp.add_lwpolyline(s)
f=figure(msp[-1])
f.drawFigurePlt()
"""

lwps = [i.LWP for i in figs]
our_coords=rate(lwps)
print(our_coords)

"""
s=[]
for i1 in range(len(figs)):#for i1 in len(figs):
    xy=[]
    for i2 in range(len(figs[i1].LWP)):
        dot = figs[i1].LWP[i2]
        x,y=dot[0],dot[1]
        xy.append([x,y])
    s.append([xy[0][0],xy[0][1],i1])
s=sorted(s)

print(s,'wowoowowo')

""" 
"""  
s=id_order(figs)  
for i in range(1,len(s)):
    msp.add_lwpolyline(bridge_len(s[i-1][2],s[i][2],figs))
    f=figure(msp[-1])
    f.drawFigurePlt()
""" 
id_order_build(figs,msp)

        


"""
lwps = [i.LWP for i in figs]
shift = find_shift(lwps)
print(lwps)
lwps.sort(key=rate)
print(lwps)

print(dot1,dot2)
"""
plt.axis('equal')
plt.show()
plt.clf()


"""4. Рисуем все через матплотлиб (нельзя ли его встроить в окно ткинтера?)"""



"""5. Определяем стартовую точку и сторону начала"""



"""6. Отрисовываем ближайшую к стартовой точке фигуру"""



"""7. Пока есть неотрисованные фигуры"""


"""___7.i. Берем неотрисованную фигру в которой есть точка ближайшая к стороне начала"""


"""___7.ii. Если невозможно провести мостик от предыдущей фигуры"""


"""______7.ii.a. Берем ближайшую фигру которая мешает провести мостик"""


"""______7.ii.b. Отрисовываем её"""


"""8. Полученный массив точек объединяем в одну длинную кривую"""


"""9. СОхраняем в отдельный файл"""


"""10. Выводим через матплотлиб"""
