from math import hypot

#gets distance between two points
#впомогательные функции
def get_distance(point1,point2):
    """Возвращает растояние между двумя точками

    Args:
        point1 (array): [Точка (x,y)]
        point2 (array): [Точка (x,y)]

    Returns:
        [float]: [растояние в единицах]
    """
    return hypot(point1[0] - point2[0], point1[1] - point2[1])

#utilty func do no touch
def ccw(A,B,C):
    """[не трогать в любом случае!!!!!!!!!!!]

    Args:
        A (float): vector1
        B (float): vector2
        C (float): vector3

    Returns:
        bool: ccw
    """
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    """определяет пересекается ли AB и CD

    Args:
        A (float): A
        B (float): B
        C (float): C
        D (float): D

    Returns:
        bool: True если пересекаются/False если нет
    """
    # Return true if line segments AB and CD intersect
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
