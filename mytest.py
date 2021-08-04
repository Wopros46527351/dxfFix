import sys
import ezdxf
from figure import figure
import matplotlib.pyplot as plt
from utility import get_distance,intersect


try:
    doc = ezdxf.readfile("111.dxf")
except IOError:
    print(f'Not a DXF file or a generic I/O error.')
    sys.exit(1)
except ezdxf.DXFStructureError:
    print(f'Invalid or corrupted DXF file.')
    sys.exit(2)

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
def make_connections(layer):
    connections = list()
    for i1 in range(len(layer)):
        for i2 in range(i1+1,len(layer)):
            a,b = bridge_points(layer[i1],layer[i2])
            distance = get_distance(layer[i1][a],layer[i2][b])
            connections.append((i1,i2,distance))
    connections  = sorted(connections,key = lambda connections:connections[2])
    return connections
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

msp = doc.modelspace()
print(len(msp))
for e in msp:
    print(e.dxftype())
figs = [figure(i) for i in msp]
for f in figs[0:2]:
    f.drawFigurePlt()
    f.drawCenter()
p1,p2 = bridge_points(figs[0].LWP,figs[1].LWP)
dot1 = figs[0].LWP[p1]
dot2 = figs[1].LWP[p2]
s=[(dot1[0],dot1[1]),(dot2[0],dot2[1])]
msp.add_lwpolyline(s)
f=figure(msp[-1])
f.drawFigurePlt()
print(dot1,dot2)
plt.axis('equal')
plt.show()
plt.clf()
