# By Mark Schneider

import math

def angle_to_vector(ang):
    '''Given the angle of rotation of the ship, return the vector in the form [x, y]'''
    return [math.cos(ang), -math.sin(ang)]