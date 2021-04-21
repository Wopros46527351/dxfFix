import matplotlib.pyplot as plt

class figure(object):
    def __init__(self,LWP):
        self.LWP = LWP
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
        l = len(self.LWP)
        midX = sum([p[0] for p in self.LWP])/l
        midY = sum([p[1] for p in self.LWP])/l
        return (midX,midY)

    def drawCenter(self):
        plt.plot(*self.center,'ro-', markersize=3)            