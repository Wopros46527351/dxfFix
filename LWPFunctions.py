from utility import get_distance,intersect
from figure import figure



def bridge_points(LWP1,LWP2):
    """Находит индексы ближайщих точек в двух полилиниях

    Args:
        LWP1 (lwp): линия1
        LWP2 (lwp): линия2

    Returns:
        tuple: (индекс точки в первой линии,индекс точки во второй линии)
    """
    links = []
    for i1,v1 in enumerate(LWP1):
        for i2,v2 in enumerate(LWP2):
            dist = get_distance(v1[:2:],v2[:2:])
            links.append((i1,i2,v1,v2,dist))
    links = sorted(links,key = lambda x:x[4])
    L = len(LWP1)
    LWP1_lines = [(i1,i2) for i1,i2 in zip(range(0,L-1),range(1,L))]+[(L-1,0)]
    L = len(LWP2)
    LWP2_lines = [(i1,i2) for i1,i2 in zip(range(0,L-1),range(1,L))]+[(L-1,0)]
    for link in links:
        eligible = True
        nono_index  = link[0]
        for c,d in [i for i in LWP1_lines if nono_index not in i]:
            A = link[2]
            B = link[3]
            C = LWP1[c]
            D = LWP1[d]
            #print(A,B,C,D)
            if intersect(A,B,C,D):
                eligible = False
                break
        nono_index  = link[1]
        for c,d in [i for i in LWP2_lines if nono_index not in i]:
            A = link[2]
            B = link[3]
            C = LWP2[c]
            D = LWP2[d]
            if intersect(A,B,C,D):
                eligible = False
                break        
        if eligible:
            #print(link)
            return link[:2:]
    print("fail")
    return (0,0)


def top_points(LWP1):
    """Находит индекс ближайшей точки в полилинии

    Args:
        LWP1 (lwp): линия1

    Returns:
        tuple: (индекс точки в первой линии)
    """
    #Ближайшей к чему?
    links = []
    for i1,v1 in enumerate(LWP1):
        
        dist = get_distance(v1[:2:],(0,0))
        links.append((i1,v1,dist))
    links = sorted(links,key = lambda x:x[4])
    L = len(LWP1)
    LWP1_lines = [(i1,i2) for i1,i2 in zip(range(0,L-1),range(1,L))]+[(L-1,0)] 
    for link in links:
        eligible = True
        nono_index  = link[0]
        for c,d in [i for i in LWP1_lines if nono_index not in i]:
            A = link[2]
            B = link[3]
            C = LWP1[c]
            D = LWP1[d]
            #print(A,B,C,D)
            if intersect(A,B,C,D):
                eligible = False
                break    
        if eligible:
            #print(link)
            return link[:2:]
    print("fail")
    return (0,0)


def make_connections(layer):
    """создаёт связи между всеми фигурами

    Args:
        layer (msp): слой

    Returns:
        array list: все связи
    """
    connections = list()
    for i1 in range(len(layer)):
        for i2 in range(i1+1,len(layer)):
            a,b = bridge_points(layer[i1],layer[i2])
            distance = get_distance(layer[i1][a],layer[i2][b])
            connections.append((i1,i2,distance))
    connections  = sorted(connections,key = lambda connections:connections[2])
    return connections


def rate(lwp):
    """Находит стартовую точку"""
    minx = None
    for dot in lwp:
        if minx:
            if dot[0] <  minx:
                minx = dot[0]
        else:
            minx = dot[0]
    return minx


def find_entry_point(start_point,layer):
    """
    Args:
        start_point (tuple): стартовая точка(x,y)
        layer (msp): слой со всеми фигурами

    Returns:
        tuple: индекс фигуры, индекс точки фигуры
    """
    mini = get_distance(start_point,layer[0][0])
    LWPindex = 0
    Pindex = 0
    for i in range(len(layer)):
        LWP = layer[i]
        for pindex in range(len(LWP)):
            point = get_distance(start_point,LWP[pindex])
            if point<mini:
                mini = point
                LWPindex = i
                Pindex = pindex
    return LWPindex,Pindex


def find_shift(lwps):
    '''Находит сдвиг для переноса всех объектов в первую четвертьArgs: 
        array lwps: список всех LWP
    Returns:
        tuple shift: (сдвиг по x, сдвиг по y)'''
    minx, miny = None, None
    for lwp in lwps:
        for dot in lwp:
            #print(dot[0])
            if minx and miny:
                if dot[0] < minx:
                    minx = dot[0]
                if dot[1] < miny:
                    miny = dot[1]
            else:
                minx, miny = dot[0], dot[1]
    shift = (abs(minx), abs(miny))
    return shift


def bridge_len(i1,i2,figs):
    """Находит индексы ближайщи точек в двух полилиниях

    Args:
        int (i1): фигура 1
        int (i2): фигура 2
        list: figs

    Returns:
        lwp: линия
    """
    p1,p2 = bridge_points(figs[i1].LWP,figs[i2].LWP)
    dot1 = figs[i1].LWP[p1]
    dot2 = figs[i2].LWP[p2]
    s=[(dot1[0],dot1[1]),(dot2[0],dot2[1])]
    return s


def id_order(figs):
    """Проверяет и находит точки, ближайшие к центру
    Args:
        figs: figs
        

    Returns:
        list: [x,y,id-фигуры]
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
    return s
'''
def id_order_build(figs,msp):
    #s=id_order(figs)
    for i in range(1,len(figs)):
        p1,p2 = bridge_points(figs[i-1].LWP,figs[i].LWP)
        dot1 = figs[i-1].LWP[p1]
        dot2 = figs[i].LWP[p2]
        obstacle = None
        for index,f in enumerate(figs):
            if not (index == i or index == i-1):
                if f.full_intersection(dot1,dot2):
                    obstacle = index
                    break
        
        if not obstacle:
            msp.add_lwpolyline(bridge_len(i-1,i,figs))
            f=figure(msp[-1])
            f.drawFigurePlt()
        else:
            msp.add_lwpolyline(bridge_len(i-1,obstacle,figs))
            f=figure(msp[-1])
            f.drawFigurePlt()
            msp.add_lwpolyline(bridge_len(obstacle,i,figs))
            f=figure(msp[-1])
            f.drawFigurePlt()
'''
def id_order_build(figs,msp):
    s=[int(i) for i in range(len(figs[:5]))]
    s_ind=1
    now=s[0]
    stack=None
    nextt=s[1]
    while s_ind!=len(s)-1:
        stack=check(now,nextt,figs)
        if stack:
            msp.add_lwpolyline(bridge_len(now,stack,figs))
            f=figure(msp[-1])
            f.drawFigurePlt()
            now = stack
            stack=None
        else:
            msp.add_lwpolyline(bridge_len(now,nextt,figs))
            f=figure(msp[-1])
            f.drawFigurePlt()
            now=nextt
            s_ind+=1
            nextt=s[s_ind]

    while s_ind!=0:
        stack=check(now,nextt,figs)
        if stack!=None:
            msp.add_lwpolyline(bridge_len(now,stack,figs))
            f=figure(msp[-1])
            f.drawFigurePlt()
            now = stack
            stack=None
        else:
            msp.add_lwpolyline(bridge_len(now,nextt,figs))
            f=figure(msp[-1])
            f.drawFigurePlt()
            s_ind=0
            break
                
    
def check(now,nextt,figs):  
    p1,p2 = bridge_points(figs[now].LWP,figs[nextt].LWP)
    dot1 = figs[now].LWP[p1]
    dot2 = figs[nextt].LWP[p2]
    for index,f in enumerate(figs[:4]):
        if not (index == now or index == next):
            if f.full_intersection(dot1,dot2):
                return index
                print("*************")
                break
    else:
        return None
        

def sort_min_x(fig):
    return fig.x0


def stack_solve(figs):
    stack = figs
    current = None
    big_line = []
    pIndex = 0
    flag = False
    while stack:
        if current == None:
            current = stack.pop()
            big_line.extend(current.point_list)
            print(f"ended {current.point_list[-1]}")
        else:
            target = stack.pop()
            p1,p2 = bridge_points(current.LWP,target.LWP)
            dot1 = current.LWP[p1]
            dot2 = target.LWP[p2]

            for f in figs:
                if not (f == current or f == target):
                    if f.full_intersection(dot1,dot2):
                        stack.append(target)
                        stack.append(f)
                        flag = True
                        break
            if flag:
                flag = False
                continue
            else:
                way = current.way(pIndex,p1)
                print(f"started {way[0]} ended {way[-1]}")
                big_line.extend(way)
                big_line.append(dot2)
                print(f"ended {dot2}")
                way= target.way(p2,0)
                print(f"started {way[0]} ended {way[-1]}")
                big_line.extend(way)
                big_line.extend(target.point_list)
                pIndex=0
                current = target
    return big_line
        