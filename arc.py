import ezdxf
import matplotlib.pyplot as plt
from math import pi,radians,degrees, cos, sin


def arc(p1,p2):
    b = p2[-1]
    v1 = ezdxf.math.Vec2(p1[0],p1[1])
    v2 = ezdxf.math.Vec2(p2[0],p2[1])
    center,start,end,radius = ezdxf.math.bulge_to_arc(v1,v2,b)
    n_p1 = (p1[0], p1[1], 0.0, 0.0, 0.0)
    points2 = [n_p1]
    d0 = int(degrees(start))
    d1 = int(degrees(end))
    x0 = center[0]
    y0 = center[1]
    for d in range(d0, d1, 1):
        d = radians(d)
        x1 = x0 + radius*cos(d) 
        y1 = y0 + radius*sin(d)
        points2.append((x1,y1))
    n_p2 = (p2[0], p2[1], 0.0, 0.0, 0.0)
    points2.append(n_p2)
    return points2




result = ezdxf.new('R2010')
msp = result.modelspace()
points = [(0,50,0,0,1),(0,100,0,0,-1),(0,150,0,0,0)]
v1 = ezdxf.math.Vec2(100,50)
v2 = ezdxf.math.Vec2(100,100)
center,start,end,radius = ezdxf.math.bulge_to_arc(v1,v2,1)
print(center,start,end,radius)
msp.add_lwpolyline(points)
points2 = [v1]
d0 = int(degrees(start))
d1 = int(degrees(end))
x0 = center[0]
y0 = center[1]
for d in range(d0, d1, 5):
    d = radians(d)
    x1 = x0 + radius*cos(d) 
    y1 = y0 + radius*sin(d)
    points2.append((x1,y1))
points2.append(v2)
msp.add_lwpolyline(points2)
result.saveas(filename="1111bip.dxf")