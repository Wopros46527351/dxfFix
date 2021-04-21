import time
from collections import defaultdict 
from utility import get_distance,intersect
from graph import Graph
import ezdxf

#TODO0 Find closest line,way better!
#Return indexes of bridge points
def bridge_points(LWP1,LWP2):
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

#finds closest point to list edge
def find_entry_point(start_point,layer):
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

#makes connections between all figs on layer[index1,index2,weight]
def make_connections(layer):
    connections = list()
    for i1 in range(len(layer)):
        for i2 in range(i1+1,len(layer)):
            a,b = bridge_points(layer[i1],layer[i2])
            distance = get_distance(layer[i1][a],layer[i2][b])
            connections.append((i1,i2,distance))
    connections  = sorted(connections,key = lambda connections:connections[2])
    return connections
    
#cuts backtrack to shortest path
def optimise_backtrack(track):
    while len(track)!=len(set(track)):
        for v in track:
            if track.count(v)>1:
                pos = track.index(v)
                pos_2 = track[pos+1::].index(v)+pos
                track = track[:pos:]+track[pos_2+1::]
                break
    return track
                
#makes optimal path
def solveTree(tree,start_point):
    visited = [start_point]
    path =[start_point]
    back_track = []
    c_point = start_point
    while len(visited)!=len(tree):
        back = True
        for opt in tree[c_point]:
            if opt not in visited:#still never tried this dot
                back_track=optimise_backtrack(back_track)
                #print(f"found new dot {opt},new opts ={tree[opt]}")
                #print(f"backtrack = {back_track},path = {path}")
                path.extend(back_track)
                back_track=[]
                c_point = opt
                path.append(opt)
                visited.append(opt)
                back = False
                break
            #hit a stop
            #go back
        if back:
            c_point = path[-2-len(back_track)]
            back_track.append(c_point)
    return path
    #print(*path,sep = "=")     

#draws on fig LWP from point1 to point2
def draw_on_fig(LWP,start_point,end_point):
    #refine to draw lengh optimal lines
    if start_point>end_point:
        
        points = [i for i in LWP[start_point+1::]]
        points.extend([i for i in LWP[:end_point+1:]])
        return points
    else:
        points = [i for i in LWP[start_point+1:end_point+1:]]
        return points

#draws fig from start point
def draw_fig(LWP,start_point):
    points = []
    for point in LWP[start_point::]:
        points.append(point)
    for point in LWP[:start_point+1:]:
        points.append(point)
    #print(points[0],points[-1])
    return points


def make_box_copy(msp,layer):
    maxx,minx,maxy,miny = get_max_min(layer)
    #for LWP in layer:
    #    copy_LWP(msp,LWP)
    sizex = maxx-minx
    sizey = maxy-miny
    points = [(maxx-sizex*1.25,maxy),(maxx-sizex*1.25,miny+sizey/2),(minx-sizex,miny+sizey/2),(minx-sizex,maxy),(maxx-sizex*1.25,maxy)]
    msp.add_lwpolyline(points)

#gets max/min of dxf
def get_max_min(layer):
    maxx = layer[0][0][0]
    minx= layer[0][0][1]
    maxy = layer[0][0][0]
    miny = layer[0][0][1]
    for LWP in layer:
        for point in LWP:
            px,py = point[:2:]
            if px > maxx:
                maxx = px
            elif px < minx:
                minx = px
            if py > maxy:
                maxy = py
            elif py < miny:
                miny = py
    return maxx,minx,maxy,miny

#give it a filename and it will redraw dxf and redraw it. Func wont save it.
def redraw_figure_way(dxf):
    total_time = time.time()
    delta_time = total_time
    doc = dxf
    result = ezdxf.new('R2010')
    layer = doc.modelspace()
    msp = result.modelspace()
    MYgraph = Graph(len(layer))
    connections = make_connections(layer)
    print(f"Геометрия считана успешно, время выполнения:{time.time()-delta_time} секунд")
    delta_time = time.time()
    for i in connections:
        MYgraph.addEdge(*i)
    connections = MYgraph.KruskalMST()
    print(f"Кратчайшие связи высчитанны успешно, время выполнения:{time.time()-delta_time} секунд")
    delta_time = time.time()
    MYgraph = Graph(len(layer))
    for u,v,w in connections:
        MYgraph.addEdge(u,v,w)
    MYgraph.sort_tree()
    print(f"Древо построенно успешно, время выполнения:{time.time()-delta_time} секунд")
    delta_time = time.time()
    maxx,minx,maxy,miny = get_max_min(layer)
    start_point = (minx,maxy)
    LWPindex, Pindex = find_entry_point(start_point,layer)
    path = solveTree(MYgraph.tree,LWPindex)
    back_track = path[::-1]
    back_track = optimise_backtrack(back_track)
    print(f"Путь построен, время выполнения:{time.time()-delta_time} секунд")
    delta_time = time.time()  
    big_line = [start_point]
    dot_pointer = Pindex
    #draw path
    for fig,next_fig in zip(path[:-1:],path[1::]):
        points = draw_fig(layer[fig],dot_pointer)
        big_line.extend(points)
        a,b = bridge_points(layer[fig],layer[next_fig])
        #print(f"points is {a} for start and {b} for end")
        points = draw_on_fig(layer[fig],dot_pointer,a)
        big_line.extend(points)
        dot_pointer = b
    #draw last fig
    points = draw_fig(layer[path[-1]],dot_pointer)
    big_line.extend(points)
    #print(f"ended on {path[-1]}")
    #draw backtrack
    a,b = bridge_points(layer[back_track[0]],layer[back_track[1]])
    dot_pointer = b
    #print(list(zip(back_track[1:-1:],back_track[2::])))
    for fig,next_fig in zip(back_track[1:-1:],back_track[2::]):
        a,b = bridge_points(layer[fig],layer[next_fig])
        points = draw_on_fig(layer[fig],dot_pointer,a)
        #print(f"drew on {fig}")
        dot_pointer = b
        big_line.extend(points)
    points = draw_on_fig(layer[back_track[-1]],dot_pointer,Pindex)
    big_line.extend(points)
    big_line.extend([start_point,(maxx,maxy),(maxx,miny),(minx,miny)])
    msp.add_lwpolyline(big_line)
    print(f"Отрисовка завершена, время выполнения:{time.time()-delta_time} секунд")
    print(f"Файл готов,общее время{time.time()-total_time}")
    return result

#print full dxf info
#TODOwell every thing
def check_dxf_info(dxf):
    doc = dxf
    print("Layers info")
    for layer in doc.layers:
        print(layer.dxf.name)
    msp = doc.modelspace()
    flag = False
    print("Figure info")
    for fig in msp:
        print(fig)
        if fig.dxftype() == "POLYLINE":
            flag = True
            print("This is 2d polyline:",fig.is_2d_polyline,fig.dxf.layer)
    return flag

#redraws all polylines to LWPolyline
def fix_polylines(dxf):
    def RedrawPolylineToLWP(polyline):
        return [i for i in polyline]
        
    result = ezdxf.new('R2010')
    msp = dxf.modelspace()
    result_msp = result.modelspace()
    for poly in msp:
        result_msp.add_lwpolyline(RedrawPolylineToLWP(poly))
    print("dxf fixed")
    return result


def get_LWP_distance(LWP1,LWP2):
    a,b = bridge_points(LWP1,LWP2)
    return [get_distance(LWP1[a],LWP2[b]),LWP1[a],LWP2[b]]
    

def redraw_path_way_vertical(dxf):
    def find_closest_top_LWP(exclution,layer,cLWP):
        candidates = [i for i in range(len(layer)) if i not in exclution]
        variants = [get_LWP_distance(layer[cLWP],layer[i]) for i in candidates]
        variants = [[i[0],i[2][0]] for i in variants]
        top_variants = sorted(variants,key = lambda x:x[1])
        close_variants = sorted(variants,key = lambda x:x[0])
        for i1,i2 in zip(top_variants,close_variants):
            print(i1,i2)
    total_time = time.time()#setting up timers
    delta_time = total_time
    print(1)
    result = ezdxf.new('R2010')#make new dxf
    layer = dxf.modelspace()#get modelspace
    msp = result.modelspace()#set up target modelspace
    print(2)
    maxx,minx,maxy,miny = get_max_min(layer)
    print(3)
    start_point = (minx,maxy)
    cLWP,pIndex = find_entry_point(start_point,layer)
    print(3)
    #go forth!
    visited = [] #format is LWP_index,(start_index,end_index)
    visited_parts = []
    #find closest high point to cLWP
    find_closest_top_LWP(visited,layer,cLWP)
    return None


def fix_dupes(dxf):
    msp = dxf.modelspace()
    mark = []
    for LWP1 in range(len(msp)):
        for LWP2 in range(LWP1+1,len(msp)):
            if [i for i in msp[LWP1]] == [i for i in msp[LWP2]]:
                mark.append(LWP1)
    print("Has dupes",*mark)
    shift=0
    for i in mark:
        msp.delete_entity(msp[i-shift])
        shift+=1
    return dxf

#def draw_box(dxf,sizex,sizey)
def test_line():
    result = ezdxf.new('R2010')
    msp = result.modelspace()
    points = [(0,0),(0,50),(0,100,0,0,1),(0,150),(0,200)]
    msp.add_lwpolyline(points)
    print(points)
    #FIX POINTS
    points = [list(p)+[0]*(5-len(p)) for p in points]
    print(points)
    reverse_points = points[::-1]
    for i in range(len(reverse_points)-1):
        reverse_points[i][4]=-reverse_points[i+1][4]
        reverse_points[i][0] = 50
    reverse_points[-1][0] = 50
    msp.add_lwpolyline(reverse_points)
    print(reverse_points)
    reverse_points = [(10,200,0,0,0),(10,150,0,0,-1),(10,100,0,0,0),(10,50,0,0,0),(10,0,0,0,0)]
    print(reverse_points)
    msp.add_lwpolyline(points)
    msp.add_lwpolyline(reverse_points)
    return result

def draw_box(msp,sizeX,sizeY):
    maxx,minx,maxy,miny = get_max_min(msp)
    print(miny)
    points = [(0,-miny-10),(sizeX,-miny-10),(sizeX,-sizeY-miny-10),(0,-sizeY-miny-10),(0,-miny-10)]
    msp.add_lwpolyline(points)