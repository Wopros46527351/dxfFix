from math import hypot
#gets distance between two points
def get_distance(point1,point2):
    return hypot(point1[0] - point2[0], point1[1] - point2[1])

#utilty func do no touch
def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    # Return true if line segments AB and CD intersect
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
