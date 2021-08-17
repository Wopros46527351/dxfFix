import ezdxf
import matplotlib.pyplot as plt
from math import pi,radians,degrees, cos, sin


def arc(p1,p2):
    print(p1,p2)
    b = p1[-1]
    v1 = ezdxf.math.Vec2(p1[0],p1[1])
    v2 = ezdxf.math.Vec2(p2[0],p2[1])
    center,start,end,radius = ezdxf.math.bulge_to_arc(v1,v2,b)
    n_p1 = (p1[0], p1[1], 0.0, 0.0, 0.0)
    points2 = [n_p1]
    d0 = int(degrees(start))
    d1 = int(degrees(end))
    x0 = center[0]
    y0 = center[1]
    k=10000//((p1[1]-p2[1])**2+(p1[0]-p2[0])**2)

    for d in range(d0, d1, k):
        d = radians(d)
        x1 = x0 + radius*cos(d) 
        y1 = y0 + radius*sin(d)
        #if (x1-x0)**2+(y1-y0)**2>100:
        points2.append((x1,y1))
    n_p2 = (p2[0], p2[1], 0.0, 0.0, 0.0)
    points2.append(n_p2)
    return points2



