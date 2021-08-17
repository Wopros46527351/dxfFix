from figure import figure
from utility import get_distance,intersect

def bridge_points(f1,f2):
    """Находит индексы ближайщих точек в двух полилиниях

    Args:
        LWP1 (lwp): линия1
        LWP2 (lwp): линия2

    Returns:
        tuple: (индекс точки в первой линии,индекс точки во второй линии)
    """
    links = []
    LWP1=f1.point_list
    LWP2=f2.point_list
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
            p1,p2 = bridge_points(current,target)
            dot1 = current.point_list[p1]
            dot2 = target.point_list[p2]

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