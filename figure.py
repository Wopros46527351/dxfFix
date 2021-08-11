import matplotlib.pyplot as plt
from utility import get_distance, intersect
'''Фигура это клас для хранения одной ЛВП, он хранит в себе ЛВП и некоторые опциональные штуки'''
class figure(object):


    def __init__(self,LWP,id = -1):
        self.LWP = LWP
        self.point_list = self.LWP_to_List()
        self.id = id
        self.x0,self.x1,self.y0,self.y1 = self.calculate_bounding_box()
        self.center = self.calculateMid()

    def printFigure(self):
        for dot in self.LWP:
            print(dot)
    
    def drawFigure(self):
        L = self.LWP
        for i in range(len(L)-1):
            if L[i][4]!=0:
                plt.plot([L[i][0],L[i+1][0]],[L[i][1],L[i+1][1]],'ro-')
            else:
                plt.plot([L[i][0],L[i+1][0]],[L[i][1],L[i+1][1]],'bo-')
        #for p in self.LWP:
        #    plt.plot(p[0],p[1],'ro-')
        plt.axis('equal')
        plt.show()
        
    def drawFigurePlt(self):
        L = self.LWP
        for i in range(len(L)-1):
            if L[i][4]!=0:
                plt.plot([L[i][0],L[i+1][0]],[L[i][1],L[i+1][1]],'ro-', markersize=2)
            else:
                plt.plot([L[i][0],L[i+1][0]],[L[i][1],L[i+1][1]],'bo-', markersize=2)

    def calculateMid(self):
        l = len(self.LWP)-1
        ''
        summX=[p[0] for p in self.LWP]
        summY=[p[1] for p in self.LWP]
        ''
        midX = sum(summX[1:])/l
        midY = sum(summY[1:])/l
        return (midX,midY)

    def drawCenter(self):
        plt.plot(*self.center,'ro-', markersize=3)

    def drawId(self):
        if self.id>=0:
            plt.text(*self.center,str(self.id))
    
    def calculate_bounding_box(self):
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
    
    def LWP_to_List(self):
        point_list = []
        for i in self.LWP:
            point_list.append(i)
        return point_list

    def bounding_box(self):
        s=[(self.x0,self.y0),(self.x1,self.y0),(self.x1,self.y1),(self.x0,self.y1),(self.x0,self.y0)]
        for i in range(len(s)-1):
            plt.plot([s[i][0],s[i+1][0]],[s[i][1],s[i+1][1]],'yo-', markersize=1)

        
    def quick_intersection(self,p1,p2):
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
        for i in range(len(self.LWP)-2):
            p1 = self.LWP[i]
            p2 = self.LWP[i+1]
            if intersect(p1,p2,p3,p4):
                return True
        return False

    def way(self,p1, p2):
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

    
    def merge_double_points(self,distance):
        L = self.LWP
        while True:
            for i in range(len(self.LWP)-2):
                if get_distance(self.LWP[i],self.LWP[i+1])<=distance:
                    self.LWP = self.LWP[:i:]+self.LWP[i+1::]
                    break
            else:
                break

                







    def draw_figure_tochka(self,ind):
        L = self.LWP
        j=ind%len(L)
        nn=len(L)-1
        
        for i in range(nn):
            kk=(i+j)%nn
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



            

        
        
        
        
        

        