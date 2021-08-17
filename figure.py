import matplotlib.pyplot as plt
from utility import get_distance, intersect
from LWPFunctions import approximate_arc

'''Фигура это клас для хранения одной ЛВП, он хранит в себе ЛВП и некоторые опциональные штуки'''
class figure(object):


    def __init__(self,LWP,id = -1):
        """Генеририрует фигуру по полилинии

        Args:
            LWP (LWPolyline): Изначальная полилиния
            id (int, optional): Порядок при построении. Defaults to -1.
        """
        self.LWP = LWP #Полилиния!
        self.point_list = [e for e in self.LWP].copy()#Лист точек для внутреннего пользования
        #print(self.point_list)
        self.id = id #
        self.x0,self.x1,self.y0,self.y1 = self.calculate_bounding_box()#
        self.center = self.calculateMid()#


    def printFigure(self):
        """Выводит все точки в ЛВП
        """
        for dot in self.LWP:
            print(dot)
    

    def drawFigure(self):
        """Рисует фигуру в собственном окошке, синим цветом прямые,красным - кривые"""
        L = self.LWP
        for i in range(len(L)-1):
            if len(L[i]) == 5 and L[i][-1]!=0:
                plt.plot([L[i][0],L[i+1][0]],[L[i][1],L[i+1][1]],'ro-')
            else:
                plt.plot([L[i][0],L[i+1][0]],[L[i][1],L[i+1][1]],'bo-')
        plt.axis('equal')
        plt.show()
        plt.clf()


    def drawFigurePlt(self):
        """Рисует не открывая отдельного окна, что бы отобразить нарисуйте весь график
        """
        '''
        L = self.LWP
        '''
        L=self.point_list
        #print(L)
        
        for i in range(len(L)-1):
            if len(L[i]) == 5 and L[i][-1]!=0:
                plt.plot([L[i][0],L[i+1][0]],[L[i][1],L[i+1][1]],'ro-')
            else:
                plt.plot([L[i][0],L[i+1][0]],[L[i][1],L[i+1][1]],'bo-')
        '''
        for i in range(1,len(L)):
            if len(L[i]) == 5 and L[i][-1]!=0:
                plt.plot([L[i][0],L[i-1][0]],[L[i][1],L[i-1][1]],'ro-')
            else:
                plt.plot([L[i][0],L[i-1][0]],[L[i][1],L[i-1][1]],'bo-')
        '''

    def calculateMid(self):
        """Вычисляет центр фигуры

        Returns:
            tuple: Координаты точки x y
        """
        l = len(self.LWP)-1
        sumX = 0
        sumY = 0
        for d in self.point_list[1::]:
            sumX+=d[0]
            sumY+=d[1]
        return (sumX/l,sumY/l)


    def drawCenter(self):
        """Отрисовывает центр,окно не открывает
        """
        plt.plot(*self.center,'ro-', markersize=3)


    def drawId(self):
        """Если айди есть - напишет в центре
        """
        if self.id>=0:
            plt.text(*self.center,str(self.id))


    def calculate_bounding_box(self):
        """Находит крайние значения фигуры

        Returns:
            tuple: Наименьший/наибольший x потом у
        """
        x0 = None
        x1 = None
        y0 = None
        y1 = None
        #print(self.point_list)
        for x,y,_,_,_ in self.point_list:
            if x0:
                if x<x0:
                    x0=x
                elif x>x1:
                    x1=x
            else:
                x0,x1=x,x

            if y0 and y1:
                if y<y0:
                    y0=y
                if y>y1:
                    y1=y
            else:
                y0,y1=y,y
        return x0,x1,y0,y1


    def bounding_box(self):
        """Рисует коробку, без окна
        """
        s=[(self.x0,self.y0),(self.x1,self.y0),(self.x1,self.y1),(self.x0,self.y1),(self.x0,self.y0)]
        for i in range(len(s)-1):
            plt.plot([s[i][0],s[i+1][0]],[s[i][1],s[i+1][1]],'yo-', markersize=1)

        
    def quick_intersection(self,p1,p2):
        """Находит пересечение с коробкой

        Args:
            p1 (vertex): Начальная точка отрезка
            p2 (vertex): Конечная точка

        Returns:
            bool: True если есть пересечение
        """
        borders = [((self.x0,self.y0),(self.x1,self.y0)),
        ((self.x1, self.y0), (self.x1, self.y1)),
        ((self.x1, self.y1), (self.x0, self.y1)),
        ((self.x0, self.y1), (self.x0, self.y0))
        ]
        for line in borders:
            if intersect(line[0],line[1],p1,p2):
                return True
        return False     


    def full_intersection(self,p3,p4):
        """Находит пересечения со всеми отрезками фигуры,долго

        Args:
            p3 (vertex): Начальный отрезок
            p4 (vertex ): Конечный отрезок

        Returns:
            bool: True если пересекает фигуру
        """
        for i in range(len(self.LWP)-2):
            p1 = self.LWP[i]
            p2 = self.LWP[i+1]
            if intersect(p1,p2,p3,p4):
                return True
        return False


    def way(self,p1, p2):
        """Находит кратчайший маршрут от одной точки до другой по фигуре

        Args:
            p1 (int): Индекс начала
            p2 (int): Индекс конца

        Returns:
            list: Список точек
        """
        if p1 < p2:
            way1 = self.point_list[p1:p2+1:]
            way2 = self.point_list[p2::]+self.point_list[:p1+1:]
            way2.reverse()
        else:
            way1 = self.point_list[p2:p1+1:]
            way2 = self.point_list[p1::]+self.point_list[:p2+1:]
            way1.reverse()
        l_way1 = sum([get_distance(way1[i],way1[i+1]) for i in range(len(way1)-2)])
        l_way2 = sum([get_distance(way2[i],way2[i+1]) for i in range(len(way2)-2)])
        if l_way1<l_way2:
            return way1
        else:
            return way2

    
    def merge_double_points(self,distance,debug = False):
        """Убирает точки которые ближе к соседним чем заданная дистанция

        Args:
            distance (float): мнимальное растояние между точками
        """
        L = self.point_list
        if debug:
            print(len(self.point_list),end=' ')
        while True:
            for i in range(len(L)-2):
                if get_distance(L[i],L[i+1])<=distance:
                    #print(L[i],L[i+1])
                    L = L[:i:]+L[i+1::]
                    
                    break
            else:
                break
        self.point_list=L
        if debug:
            print(len(self.point_list))
        
        
    def draw_from_point(self,index):
        """Определяет маршрут по кривой начиная с заданой точки

        Args:
            index (int): Индекс начальной точки
        """
        L = self.point_list
        if index:
            return L[index::]+L[:index:]
        else:
            return L


    def draw_figure_tochka(self,ind):
        L = self.point_list
        j=ind%len(L)
        nn=len(L)-1
        
        for i in range(nn):
            kk=(i+j+nn)%nn
            plt.text(L[kk][0],L[kk][1],f"{i}\n{kk}")
            #plt.text(L[kk][0],L[kk+1][1],str(kk))
            if L[kk][4]!=0:
                plt.plot([L[kk][0],L[kk+1][0]],[L[kk][1],L[kk+1][1]],'ro-', markersize=2)
            else:
                plt.plot([L[kk][0],L[kk+1][0]],[L[kk][1],L[kk+1][1]],'bo-', markersize=2)
        
        if j==0:
            plt.plot([L[nn][0],L[j][0]],[L[nn][1],L[j][1]],'bo-', markersize=2)
        else:
            plt.plot([L[j-1][0],L[j][0]],[L[j-1][1],L[j][1]],'bo-', markersize=2)
    

    def normalize_lwp(self):
        L = self.point_list
        for i in range(len(L)):
            if len(L[i]) < 5:
                L[i] = (L[i][0], L[i][1], 0, 0, 0)
        self.point_list = L


    def make_arcs(self,segments = 5):
        
        L = self.point_list
        arcs=self.find_arcs()
        new_L =[]
        for i,e in enumerate(L):
            new_L.append((e[0],e[1],0,0,0))
            if i in arcs:
                path = approximate_arc(*arcs[i],segments)
                if get_distance(new_L[-1], path[0])>get_distance(new_L[-1], path[-1]):
                    path.reverse()
                new_L.extend(path)
            
        
        
            

        self.point_list=new_L
        self.normalize_lwp()


    def find_arcs(self):
        """Находит дуги 

        Returns:
            Словарь с дугами: key- идекс точки, value - кортеж данных, модержащий начальную точку дуги, конечную точку дуги и скривление дуги 
        """
        arcs = {}
        n=0
        L=self.point_list
        for e1,e2 in zip(L,L[1::]):
            if len(e1) == 5 and e1[-1]!=0:
                arcs[n]=(e1,e2,e1[-1])
            n+=1

            
        return arcs

    def draw_in_steps(self,speed = 1):

        L = self.point_list
        for e1,e2 in zip(L,L[1::]):
            if len(e1) == 5 and e1[-1]!=0:
                plt.plot([e1[0],e2[0]],[e1[1],e2[1]],'ro-')
            else:
                plt.plot([e1[0],e2[0]],[e1[1],e2[1]],'bo-')
            plt.axis('equal')
            plt.draw()
            plt.pause(1/speed)

    
                




            

        
        
        
        
        

        