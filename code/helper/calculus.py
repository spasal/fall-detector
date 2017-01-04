from math import atan2,degrees, sqrt, pow, acos
import numpy as np

def calculate_points(eig_vecs, mean_vec, axis_length):
    points = []
    points.append([]), points.append([])
    index = 0
    
    startpoint = mean_vec[0]

    for direction in eig_vecs:
        x_add, y_add = direction[0] * axis_length, direction[1] * axis_length
        add = [x_add, y_add]
        endpoint = startpoint + add
        points[index].extend([startpoint, endpoint])
        index += 1  

    return points

def calculate_vectors_angle(points):
    # todo kan gevectorizeerd
    # http://stackoverflow.com/questions/31735499/calculate-angle-clockwise-between-two-points
    angles = []
    for point_combination in points:
        p1 = point_combination[0]
        p2 = point_combination[1]

        xDiff = p2[0] - p1[0]
        yDiff = p2[1] - p1[1]
        angle = degrees(atan2(yDiff, xDiff))

        # re-orient to new map
        angle += 90
        if angle < 0:
            angle = 360 + angle

        angles.append(angle) #% 360)

    return angles

def calculate_delta_angle(vector1, vector2):
    # determine movement vector
    x1, y1 = vector1[1][0] - vector1[0][0], vector1[1][1] - vector1[0][1]
    x2, y2 = vector2[1][0] - vector2[0][0], vector2[1][1] - vector2[0][1]

    # calculate dot vector
    dot_product = (x1*x2) + (y1*y2)

    # calculate length of vectors
    lvector1 = sqrt( pow(x1, 2) + pow(y1, 2) )
    lvector2 = sqrt( pow(x2, 2) + pow(y2, 2) )

    # calculate angle based on cos
    cos_delta = dot_product / (lvector1 * lvector2)
    delta = acos(cos_delta)
    delta = degrees(delta)

    if delta > 180:
        delta -= 360

    return abs(delta)
