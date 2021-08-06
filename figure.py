import matplotlib.pyplot as plt
'''Фигура это клас для хранения одной ЛВП, он хранит в себе ЛВП и некоторые опциональные штуки'''
class figure(object):


    def __init__(self,LWP,id = -1):
        self.LWP = LWP
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
        for x,y,_ in self.LWP:
            if x0 and x1:
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
    
    

